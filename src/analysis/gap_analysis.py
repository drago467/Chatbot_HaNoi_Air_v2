"""
Task 3: Gap Analysis

Identify missing variables, assess estimation feasibility, prioritize estimation needs.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
import sys
sys.path.append(str(Path(__file__).parent))

from utils import load_merged_kg, save_json, get_all_conditions


def load_analysis_data():
    """Load condition inventory and API mapping data."""
    with open("data/analysis/condition_inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    with open("data/analysis/api_mapping_table.json", 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    return inventory, mapping


def assess_estimation_feasibility(field: str, mapping_info: Dict[str, Any]) -> str:
    """Assess estimation feasibility: high, medium, low."""
    
    estimation_feasible = mapping_info.get("estimation_feasible")
    estimation_method = mapping_info.get("estimation_method")
    
    if estimation_feasible is False:
        return "low"
    
    if estimation_feasible is True:
        # High feasibility: well-established methods
        high_feasibility_methods = [
            "temperature_gradient",
            "stability_index",
            "ph_estimation",
            "alw_estimation",
            "meteorological_pattern"
        ]
        if estimation_method in high_feasibility_methods:
            return "high"
        else:
            return "medium"
    
    # Check field patterns
    field_lower = field.lower()
    
    # High feasibility patterns
    if any(term in field_lower for term in ["boundary_layer", "pbl", "inversion", "stability"]):
        return "high"
    if any(term in field_lower for term in ["ph", "liquid_water", "alw"]):
        return "high"
    if any(term in field_lower for term in ["cold_surge", "monsoon"]):
        return "medium"
    
    # Low feasibility: qualitative or complex
    if any(term in field_lower for term in ["precursor", "particle_type", "geographic", "region"]):
        return "low"
    
    return "medium"  # Default to medium if unknown


def calculate_impact_score(field: str, frequency: int, checkable_count: int, 
                          total_count: int, feasibility: str) -> float:
    """Calculate impact score: frequency × checkable_rate × criticality_weight."""
    
    checkable_rate = checkable_count / total_count if total_count > 0 else 0
    
    # Criticality weights based on frequency
    if frequency >= 20:
        criticality_weight = 1.0
    elif frequency >= 10:
        criticality_weight = 0.8
    elif frequency >= 5:
        criticality_weight = 0.6
    else:
        criticality_weight = 0.4
    
    # Feasibility weight
    feasibility_weights = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.3
    }
    feasibility_weight = feasibility_weights.get(feasibility, 0.5)
    
    # Normalize frequency (log scale to prevent very high frequencies from dominating)
    import math
    normalized_frequency = math.log10(frequency + 1) / math.log10(100)  # Normalize to 0-1 for frequencies up to 100
    
    impact_score = normalized_frequency * checkable_rate * criticality_weight * feasibility_weight
    
    return round(impact_score, 3)


def get_relationships_using_field(field: str, kg_data: Dict[str, Any]) -> List[str]:
    """Get list of relationship IDs that use this field."""
    relationship_ids = []
    
    for rel in kg_data.get("relationships", []):
        for condition in rel.get("conditions", []):
            if condition.get("field") == field:
                relationship_ids.append(rel.get("id", "unknown"))
                break
    
    return list(set(relationship_ids))


def perform_gap_analysis() -> Dict[str, Any]:
    """Perform comprehensive gap analysis."""
    
    print("Loading analysis data...")
    inventory, mapping = load_analysis_data()
    kg_data = load_merged_kg()
    
    print("Identifying missing fields...")
    
    # Get missing fields from mapping
    missing_mappings = [m for m in mapping["mappings"] if m.get("mapping_type") == "missing"]
    
    # Get field frequency data
    field_frequency_map = {}
    for field_info in inventory.get("field_frequency", []):
        field_frequency_map[field_info["field"]] = {
            "frequency": field_info["frequency"],
            "checkable_count": field_info["checkable_count"],
            "non_checkable_count": field_info["non_checkable_count"]
        }
    
    # Analyze each missing field
    missing_fields_analysis = []
    
    for mapping_info in missing_mappings:
        field = mapping_info.get("condition_field", "")
        if not field:
            continue
        
        # Get frequency data
        freq_data = field_frequency_map.get(field, {
            "frequency": 0,
            "checkable_count": 0,
            "non_checkable_count": 0
        })
        
        frequency = freq_data["frequency"]
        checkable_count = freq_data["checkable_count"]
        total_count = frequency
        
        # Determine criticality
        if frequency >= 20 and checkable_count >= 15:
            criticality = "critical"
        elif frequency >= 10 and checkable_count >= 7:
            criticality = "important"
        else:
            criticality = "optional"
        
        # Assess feasibility
        feasibility = assess_estimation_feasibility(field, mapping_info)
        
        # Calculate impact score
        impact_score = calculate_impact_score(
            field, frequency, checkable_count, total_count, feasibility
        )
        
        # Get relationships affected
        relationships_affected = get_relationships_using_field(field, kg_data)
        
        # Build estimation methods list
        estimation_methods = []
        estimation_method = mapping_info.get("estimation_method")
        if estimation_method:
            estimation_methods.append({
                "method": estimation_method,
                "confidence": 0.7 if feasibility == "high" else 0.5 if feasibility == "medium" else 0.3,
                "required_fields": get_required_fields_for_estimation(field, estimation_method),
                "notes": mapping_info.get("notes", "")
            })
        else:
            # Suggest estimation methods based on field
            suggested = suggest_estimation_methods(field)
            estimation_methods.extend(suggested)
        
        missing_fields_analysis.append({
            "field": field,
            "frequency": frequency,
            "checkable_count": checkable_count,
            "non_checkable_count": freq_data["non_checkable_count"],
            "checkable_rate": round(checkable_count / total_count, 3) if total_count > 0 else 0,
            "criticality": criticality,
            "estimation_feasibility": feasibility,
            "impact_score": impact_score,
            "estimation_methods": estimation_methods,
            "relationships_affected": relationships_affected,
            "relationships_affected_count": len(relationships_affected),
            "notes": mapping_info.get("notes", "")
        })
    
    # Sort by impact score
    missing_fields_analysis.sort(key=lambda x: x["impact_score"], reverse=True)
    
    # Calculate summary statistics
    total_missing = len(missing_fields_analysis)
    critical_missing = sum(1 for f in missing_fields_analysis if f["criticality"] == "critical")
    important_missing = sum(1 for f in missing_fields_analysis if f["criticality"] == "important")
    optional_missing = sum(1 for f in missing_fields_analysis if f["criticality"] == "optional")
    
    high_feasibility = sum(1 for f in missing_fields_analysis if f["estimation_feasibility"] == "high")
    medium_feasibility = sum(1 for f in missing_fields_analysis if f["estimation_feasibility"] == "medium")
    low_feasibility = sum(1 for f in missing_fields_analysis if f["estimation_feasibility"] == "low")
    
    result = {
        "missing_fields": missing_fields_analysis,
        "summary": {
            "total_missing": total_missing,
            "critical_missing": critical_missing,
            "important_missing": important_missing,
            "optional_missing": optional_missing,
            "high_feasibility": high_feasibility,
            "medium_feasibility": medium_feasibility,
            "low_feasibility": low_feasibility
        },
        "top_10_priority": missing_fields_analysis[:10]
    }
    
    return result


def get_required_fields_for_estimation(field: str, method: str) -> List[str]:
    """Get required API fields for estimation method."""
    
    method_requirements = {
        "temperature_gradient": ["temperature", "pressure"],
        "stability_index": ["temperature", "wind_speed", "cloud_cover"],
        "ph_estimation": ["so2_concentration", "no2_concentration", "relative_humidity"],
        "alw_estimation": ["relative_humidity", "temperature", "pm25"],
        "meteorological_pattern": ["wind_direction", "temperature", "pressure"]
    }
    
    return method_requirements.get(method, [])


def suggest_estimation_methods(field: str) -> List[Dict[str, Any]]:
    """Suggest estimation methods for a field based on name patterns."""
    
    field_lower = field.lower()
    suggestions = []
    
    if "boundary_layer" in field_lower or "pbl" in field_lower:
        suggestions.append({
            "method": "temperature_gradient",
            "confidence": 0.7,
            "required_fields": ["temperature", "pressure"],
            "notes": "Estimate from temperature lapse rate"
        })
        suggestions.append({
            "method": "stability_index",
            "confidence": 0.6,
            "required_fields": ["temperature", "wind_speed", "cloud_cover"],
            "notes": "Estimate from atmospheric stability"
        })
    
    elif "ph" in field_lower:
        suggestions.append({
            "method": "ph_estimation",
            "confidence": 0.7,
            "required_fields": ["so2_concentration", "no2_concentration", "relative_humidity"],
            "notes": "Estimate from precursor concentrations and RH"
        })
    
    elif "liquid_water" in field_lower or "alw" in field_lower:
        suggestions.append({
            "method": "alw_estimation",
            "confidence": 0.7,
            "required_fields": ["relative_humidity", "temperature", "pm25"],
            "notes": "Estimate from RH, temperature, and PM2.5 composition"
        })
    
    elif "inversion" in field_lower:
        suggestions.append({
            "method": "stability_index",
            "confidence": 0.6,
            "required_fields": ["temperature", "wind_speed", "cloud_cover"],
            "notes": "Estimate from temperature gradient and stability"
        })
    
    elif "cold_surge" in field_lower:
        suggestions.append({
            "method": "meteorological_pattern",
            "confidence": 0.6,
            "required_fields": ["wind_direction", "temperature", "pressure"],
            "notes": "Estimate from wind direction, temperature, and pressure patterns"
        })
    
    return suggestions


def generate_gap_analysis_report(gap_data: Dict[str, Any]) -> str:
    """Generate markdown report from gap analysis."""
    
    summary = gap_data["summary"]
    top_10 = gap_data["top_10_priority"]
    
    report = f"""# Gap Analysis Report

## Executive Summary

- **Total Missing Fields**: {summary['total_missing']}
- **Critical Missing**: {summary['critical_missing']}
- **Important Missing**: {summary['important_missing']}
- **Optional Missing**: {summary['optional_missing']}

### Estimation Feasibility

- **High Feasibility**: {summary['high_feasibility']} fields
- **Medium Feasibility**: {summary['medium_feasibility']} fields
- **Low Feasibility**: {summary['low_feasibility']} fields

---

## Top 10 Priority Fields for Estimation

| Rank | Field | Frequency | Checkable | Criticality | Feasibility | Impact Score | Relationships Affected |
|------|-------|-----------|-----------|-------------|-------------|--------------|----------------------|
"""
    
    for i, field_info in enumerate(top_10, 1):
        field = field_info["field"]
        freq = field_info["frequency"]
        checkable = field_info["checkable_count"]
        criticality = field_info["criticality"]
        feasibility = field_info["estimation_feasibility"]
        impact = field_info["impact_score"]
        rel_count = field_info["relationships_affected_count"]
        
        report += f"| {i} | {field} | {freq} | {checkable} | {criticality} | {feasibility} | {impact} | {rel_count} |\n"
    
    report += "\n---\n\n## Detailed Missing Fields Analysis\n\n"
    
    # Group by criticality
    for criticality in ["critical", "important", "optional"]:
        fields_in_category = [f for f in gap_data["missing_fields"] if f["criticality"] == criticality]
        if not fields_in_category:
            continue
        
        report += f"### {criticality.capitalize()} Priority Fields\n\n"
        report += "| Field | Frequency | Checkable | Feasibility | Impact Score | Estimation Methods |\n"
        report += "|-------|-----------|-----------|-------------|--------------|---------------------|\n"
        
        for field_info in sorted(fields_in_category, key=lambda x: x["impact_score"], reverse=True):
            field = field_info["field"]
            freq = field_info["frequency"]
            checkable = field_info["checkable_count"]
            feasibility = field_info["estimation_feasibility"]
            impact = field_info["impact_score"]
            methods = ", ".join([m["method"] for m in field_info["estimation_methods"]]) or "None"
            
            report += f"| {field} | {freq} | {checkable} | {feasibility} | {impact} | {methods} |\n"
        
        report += "\n"
    
    report += "---\n\n## Recommendations for Phase 2\n\n"
    report += "### High Priority (Critical + High Feasibility)\n\n"
    
    high_priority = [
        f for f in gap_data["missing_fields"]
        if f["criticality"] == "critical" and f["estimation_feasibility"] == "high"
    ]
    
    for field_info in sorted(high_priority, key=lambda x: x["impact_score"], reverse=True):
        field = field_info["field"]
        methods = field_info["estimation_methods"]
        report += f"1. **{field}** (Impact: {field_info['impact_score']})\n"
        for method in methods:
            report += f"   - Method: {method['method']} (Confidence: {method['confidence']})\n"
            report += f"   - Required fields: {', '.join(method['required_fields'])}\n"
        report += "\n"
    
    report += "\n### Medium Priority (Important + Medium/High Feasibility)\n\n"
    medium_priority = [
        f for f in gap_data["missing_fields"]
        if f["criticality"] == "important" and f["estimation_feasibility"] in ["high", "medium"]
    ]
    
    for field_info in sorted(medium_priority, key=lambda x: x["impact_score"], reverse=True)[:5]:
        field = field_info["field"]
        methods = field_info["estimation_methods"]
        report += f"- **{field}** (Impact: {field_info['impact_score']}) - {methods[0]['method'] if methods else 'No method'}\n"
    
    return report


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 3: Gap Analysis")
    print("=" * 60)
    
    # Perform gap analysis
    gap_data = perform_gap_analysis()
    
    # Save JSON
    output_json = "data/analysis/gap_analysis.json"
    print(f"\nSaving gap analysis to {output_json}...")
    save_json(gap_data, output_json)
    print("[OK] Saved!")
    
    # Generate report
    report = generate_gap_analysis_report(gap_data)
    output_report = "docs/analysis/gap_analysis_report.md"
    print(f"\nSaving report to {output_report}...")
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 3 Complete!")
    print("=" * 60)
    summary = gap_data["summary"]
    print(f"\nSummary:")
    print(f"  - Total missing: {summary['total_missing']}")
    print(f"  - Critical: {summary['critical_missing']}, Important: {summary['important_missing']}, Optional: {summary['optional_missing']}")
    print(f"  - High feasibility: {summary['high_feasibility']}, Medium: {summary['medium_feasibility']}, Low: {summary['low_feasibility']}")


if __name__ == "__main__":
    main()
