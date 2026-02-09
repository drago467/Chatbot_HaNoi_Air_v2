"""
Task 4: Condition Coverage Analysis

Analyze coverage of conditions: what percentage can be checked with current API data.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
import sys
sys.path.append(str(Path(__file__).parent))

from utils import load_merged_kg, save_json


def load_analysis_data():
    """Load condition inventory and API mapping data."""
    with open("data/analysis/condition_inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    with open("data/analysis/api_mapping_table.json", 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    return inventory, mapping


def is_field_available_in_api(field: str, mapping_data: Dict[str, Any]) -> bool:
    """Check if a field is available in API (direct, mapped, or derived)."""
    
    for mapping in mapping_data.get("mappings", []):
        if mapping.get("condition_field") == field:
            mapping_type = mapping.get("mapping_type")
            return mapping_type in ["direct", "mapped", "derived"]
    
    return False


def calculate_relationship_coverage(kg_data: Dict[str, Any], mapping_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Calculate coverage for each relationship."""
    
    relationship_coverage = []
    
    for rel in kg_data.get("relationships", []):
        rel_id = rel.get("id", "unknown")
        category = rel.get("category", "unknown")
        conditions = rel.get("conditions", [])
        
        total_conditions = len(conditions)
        checkable_conditions = sum(1 for c in conditions if c.get("checkable", False))
        
        # Count API-available conditions
        api_available_conditions = 0
        missing_fields = []
        
        for condition in conditions:
            if not condition.get("checkable", False):
                continue
            
            field = condition.get("field", "")
            if field and is_field_available_in_api(field, mapping_data):
                api_available_conditions += 1
            elif field:
                missing_fields.append(field)
        
        # Calculate coverage percentage
        coverage_percentage = round(
            (api_available_conditions / checkable_conditions * 100) if checkable_conditions > 0 else 0,
            2
        )
        
        relationship_coverage.append({
            "relationship_id": rel_id,
            "category": category,
            "total_conditions": total_conditions,
            "checkable_conditions": checkable_conditions,
            "api_available_conditions": api_available_conditions,
            "coverage_percentage": coverage_percentage,
            "missing_fields": list(set(missing_fields))
        })
    
    return relationship_coverage


def calculate_category_stats(relationship_coverage: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Calculate coverage statistics by category."""
    
    category_stats = defaultdict(lambda: {
        "relationships": [],
        "total_conditions_sum": 0,
        "checkable_conditions_sum": 0,
        "api_available_conditions_sum": 0
    })
    
    for rel_cov in relationship_coverage:
        category = rel_cov["category"]
        category_stats[category]["relationships"].append(rel_cov)
        category_stats[category]["total_conditions_sum"] += rel_cov["total_conditions"]
        category_stats[category]["checkable_conditions_sum"] += rel_cov["checkable_conditions"]
        category_stats[category]["api_available_conditions_sum"] += rel_cov["api_available_conditions"]
    
    # Calculate averages
    result = {}
    for category, stats in category_stats.items():
        rel_count = len(stats["relationships"])
        avg_coverage = round(
            (stats["api_available_conditions_sum"] / stats["checkable_conditions_sum"] * 100)
            if stats["checkable_conditions_sum"] > 0 else 0,
            2
        )
        
        result[category] = {
            "relationships_count": rel_count,
            "avg_coverage": avg_coverage,
            "total_conditions": stats["total_conditions_sum"],
            "checkable_conditions": stats["checkable_conditions_sum"],
            "api_available_conditions": stats["api_available_conditions_sum"]
        }
    
    return result


def perform_coverage_analysis() -> Dict[str, Any]:
    """Perform comprehensive coverage analysis."""
    
    print("Loading data...")
    inventory, mapping = load_analysis_data()
    kg_data = load_merged_kg()
    
    print("Calculating relationship coverage...")
    relationship_coverage = calculate_relationship_coverage(kg_data, mapping)
    
    print("Calculating category statistics...")
    category_stats = calculate_category_stats(relationship_coverage)
    
    # Calculate overall coverage
    total_checkable = sum(r["checkable_conditions"] for r in relationship_coverage)
    total_api_available = sum(r["api_available_conditions"] for r in relationship_coverage)
    overall_coverage = round(
        (total_api_available / total_checkable * 100) if total_checkable > 0 else 0,
        2
    )
    
    # Identify relationships with low coverage
    low_coverage_threshold = 50.0
    low_coverage_relationships = [
        r for r in relationship_coverage
        if r["coverage_percentage"] < low_coverage_threshold and r["checkable_conditions"] > 0
    ]
    low_coverage_relationships.sort(key=lambda x: x["coverage_percentage"])
    
    result = {
        "relationship_coverage": relationship_coverage,
        "category_stats": category_stats,
        "overall_coverage": overall_coverage,
        "summary": {
            "total_relationships": len(relationship_coverage),
            "total_conditions": sum(r["total_conditions"] for r in relationship_coverage),
            "total_checkable_conditions": total_checkable,
            "total_api_available_conditions": total_api_available,
            "overall_coverage_percentage": overall_coverage,
            "low_coverage_count": len(low_coverage_relationships),
            "low_coverage_threshold": low_coverage_threshold
        },
        "low_coverage_relationships": low_coverage_relationships[:20]  # Top 20
    }
    
    return result


def generate_coverage_report(coverage_data: Dict[str, Any]) -> str:
    """Generate markdown report from coverage analysis."""
    
    summary = coverage_data["summary"]
    category_stats = coverage_data["category_stats"]
    low_coverage = coverage_data["low_coverage_relationships"]
    
    report = f"""# Condition Coverage Analysis Report

## Executive Summary

- **Total Relationships**: {summary['total_relationships']}
- **Total Conditions**: {summary['total_conditions']}
- **Checkable Conditions**: {summary['total_checkable_conditions']}
- **API-Available Conditions**: {summary['total_api_available_conditions']}
- **Overall Coverage**: {summary['overall_coverage_percentage']}%

---

## Coverage by Category

| Category | Relationships | Avg Coverage | Checkable | API-Available |
|----------|---------------|--------------|-----------|---------------|
"""
    
    # Sort categories by average coverage
    sorted_categories = sorted(
        category_stats.items(),
        key=lambda x: x[1]["avg_coverage"],
        reverse=True
    )
    
    for category, stats in sorted_categories:
        report += f"| {category} | {stats['relationships_count']} | {stats['avg_coverage']}% | {stats['checkable_conditions']} | {stats['api_available_conditions']} |\n"
    
    report += "\n---\n\n## Relationships with Low Coverage (< 50%)\n\n"
    report += f"Total: {summary['low_coverage_count']} relationships\n\n"
    report += "| Relationship ID | Category | Coverage | Checkable | API-Available | Missing Fields |\n"
    report += "|-----------------|----------|----------|-----------|---------------|----------------|\n"
    
    for rel in low_coverage[:20]:
        rel_id = rel["relationship_id"]
        category = rel["category"]
        coverage = rel["coverage_percentage"]
        checkable = rel["checkable_conditions"]
        api_available = rel["api_available_conditions"]
        missing = ", ".join(rel["missing_fields"][:3])  # Show first 3
        if len(rel["missing_fields"]) > 3:
            missing += f" (+{len(rel['missing_fields']) - 3} more)"
        
        report += f"| {rel_id} | {category} | {coverage}% | {checkable} | {api_available} | {missing} |\n"
    
    report += "\n---\n\n## Coverage Distribution\n\n"
    
    # Calculate distribution
    coverage_ranges = {
        "0-25%": 0,
        "25-50%": 0,
        "50-75%": 0,
        "75-100%": 0
    }
    
    for rel in coverage_data["relationship_coverage"]:
        coverage = rel["coverage_percentage"]
        if coverage == 0:
            coverage_ranges["0-25%"] += 1
        elif coverage < 25:
            coverage_ranges["0-25%"] += 1
        elif coverage < 50:
            coverage_ranges["25-50%"] += 1
        elif coverage < 75:
            coverage_ranges["50-75%"] += 1
        else:
            coverage_ranges["75-100%"] += 1
    
    report += "| Coverage Range | Number of Relationships |\n"
    report += "|----------------|-------------------------|\n"
    for range_name, count in coverage_ranges.items():
        report += f"| {range_name} | {count} |\n"
    
    report += "\n---\n\n## Improvement Opportunities\n\n"
    
    # Find most common missing fields in low coverage relationships
    missing_field_counts = defaultdict(int)
    for rel in low_coverage:
        for field in rel["missing_fields"]:
            missing_field_counts[field] += 1
    
    if missing_field_counts:
        report += "### Most Common Missing Fields in Low Coverage Relationships\n\n"
        report += "| Field | Frequency |\n"
        report += "|-------|-----------|\n"
        
        sorted_missing = sorted(missing_field_counts.items(), key=lambda x: x[1], reverse=True)
        for field, count in sorted_missing[:10]:
            report += f"| {field} | {count} |\n"
    
    report += "\n### Recommendations\n\n"
    report += "1. **High Priority**: Focus on estimating fields that appear frequently in low coverage relationships\n"
    report += "2. **Category Focus**: Prioritize categories with lowest average coverage\n"
    report += "3. **Phase 2**: Use gap analysis results to prioritize estimation strategy research\n"
    
    return report


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 4: Condition Coverage Analysis")
    print("=" * 60)
    
    # Perform coverage analysis
    coverage_data = perform_coverage_analysis()
    
    # Save JSON
    output_json = "data/analysis/coverage_analysis.json"
    print(f"\nSaving coverage analysis to {output_json}...")
    save_json(coverage_data, output_json)
    print("[OK] Saved!")
    
    # Generate report
    report = generate_coverage_report(coverage_data)
    output_report = "docs/analysis/coverage_analysis_report.md"
    print(f"\nSaving report to {output_report}...")
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 4 Complete!")
    print("=" * 60)
    summary = coverage_data["summary"]
    print(f"\nSummary:")
    print(f"  - Overall coverage: {summary['overall_coverage_percentage']}%")
    print(f"  - Total relationships: {summary['total_relationships']}")
    print(f"  - Low coverage relationships: {summary['low_coverage_count']}")


if __name__ == "__main__":
    main()
