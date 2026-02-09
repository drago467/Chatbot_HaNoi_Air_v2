"""
Task 6: Generate Comprehensive Report

Aggregate all analysis results and generate comprehensive markdown report with recommendations for Phase 2.
"""

import json
from pathlib import Path
from typing import Dict, Any
import sys
sys.path.append(str(Path(__file__).parent))

from utils import load_merged_kg


def load_all_analysis_data():
    """Load all analysis results."""
    with open("data/analysis/condition_inventory.json", 'r', encoding='utf-8') as f:
        condition_inventory = json.load(f)
    
    with open("data/analysis/api_mapping_table.json", 'r', encoding='utf-8') as f:
        api_mapping = json.load(f)
    
    with open("data/analysis/gap_analysis.json", 'r', encoding='utf-8') as f:
        gap_analysis = json.load(f)
    
    with open("data/analysis/coverage_analysis.json", 'r', encoding='utf-8') as f:
        coverage_analysis = json.load(f)
    
    with open("data/analysis/field_taxonomy.json", 'r', encoding='utf-8') as f:
        field_taxonomy = json.load(f)
    
    kg_data = load_merged_kg()
    
    return {
        "condition_inventory": condition_inventory,
        "api_mapping": api_mapping,
        "gap_analysis": gap_analysis,
        "coverage_analysis": coverage_analysis,
        "field_taxonomy": field_taxonomy,
        "kg_data": kg_data
    }


def generate_comprehensive_report(data: Dict[str, Any]) -> str:
    """Generate comprehensive Phase 1 report."""
    
    condition_inv = data["condition_inventory"]
    api_mapping = data["api_mapping"]
    gap_analysis = data["gap_analysis"]
    coverage_analysis = data["coverage_analysis"]
    field_taxonomy = data["field_taxonomy"]
    kg_data = data["kg_data"]
    
    report = f"""# Phase 1: Data Analysis & Mapping - Comprehensive Report

**Generated**: {Path(__file__).stat().st_mtime if Path(__file__).exists() else 'N/A'}  
**Knowledge Graph**: {kg_data.get('schema_version', 'unknown')}  
**Total Relationships**: {kg_data.get('relationship_count_valid', 0)}  
**Total Sources**: {kg_data.get('source_count', 0)}

---

## Executive Summary

Phase 1 analysis has been completed to understand the coverage of API data for evaluating conditions in the causal knowledge graph. Key findings:

- **Total Conditions Analyzed**: {condition_inv['total_conditions']}
- **Checkable Conditions**: {condition_inv['checkable_count']} ({condition_inv['checkable_percentage']}%)
- **API Coverage**: {api_mapping['coverage_stats']['coverage_percentage']}%
- **Overall Condition Coverage**: {coverage_analysis['overall_coverage']}%
- **Missing Fields**: {gap_analysis['summary']['total_missing']}
- **Critical Missing Fields**: {gap_analysis['summary']['critical_missing']}

---

## 1. Condition Inventory Summary

### Statistics

- **Total Conditions**: {condition_inv['total_conditions']}
- **Checkable**: {condition_inv['checkable_count']} ({condition_inv['checkable_percentage']}%)
- **Non-checkable**: {condition_inv['non_checkable_count']}
- **Unique Fields**: {condition_inv['summary']['unique_fields']}
- **Unique Types**: {condition_inv['summary']['unique_types']}

### Distribution by Type

"""
    
    # Condition types
    by_type_sorted = sorted(condition_inv['by_type'].items(), key=lambda x: x[1], reverse=True)
    for cond_type, count in by_type_sorted:
        percentage = round(count / condition_inv['total_conditions'] * 100, 2)
        report += f"- **{cond_type}**: {count} ({percentage}%)\n"
    
    report += "\n### Top 10 Fields by Frequency\n\n"
    report += "| Field | Frequency | Checkable | Non-checkable |\n"
    report += "|-------|-----------|-----------|---------------|\n"
    
    for field_info in condition_inv['field_frequency'][:10]:
        field = field_info['field']
        freq = field_info['frequency']
        checkable = field_info['checkable_count']
        non_checkable = field_info['non_checkable_count']
        report += f"| {field} | {freq} | {checkable} | {non_checkable} |\n"
    
    report += "\n---\n\n## 2. API Mapping Summary\n\n"
    
    stats = api_mapping['coverage_stats']
    report += f"""
### Coverage Statistics

- **Total Fields**: {stats['total_fields']}
- **Coverage**: {stats['coverage_percentage']}%
- **Direct Mappings**: {stats['direct_mapping']}
- **Mapped (with transformation)**: {stats['mapped']}
- **Derived**: {stats['derived']}
- **Missing**: {stats['missing']}

### Coverage by API Source

- **OpenWeatherMap**: {api_mapping['api_sources']['openweathermap']} fields
- **Open-Meteo**: {api_mapping['api_sources']['open_meteo']} fields
- **Derived**: {api_mapping['api_sources']['derived']} fields
- **Missing**: {api_mapping['api_sources']['missing']} fields

---

## 3. Gap Analysis Summary

### Missing Fields Overview

- **Total Missing**: {gap_analysis['summary']['total_missing']}
- **Critical**: {gap_analysis['summary']['critical_missing']}
- **Important**: {gap_analysis['summary']['important_missing']}
- **Optional**: {gap_analysis['summary']['optional_missing']}

### Estimation Feasibility

- **High Feasibility**: {gap_analysis['summary']['high_feasibility']} fields
- **Medium Feasibility**: {gap_analysis['summary']['medium_feasibility']} fields
- **Low Feasibility**: {gap_analysis['summary']['low_feasibility']} fields

### Top 5 Priority Fields for Estimation

"""
    
    for i, field_info in enumerate(gap_analysis['top_10_priority'][:5], 1):
        field = field_info['field']
        freq = field_info['frequency']
        checkable = field_info['checkable_count']
        criticality = field_info['criticality']
        feasibility = field_info['estimation_feasibility']
        impact = field_info['impact_score']
        rel_count = field_info['relationships_affected_count']
        
        report += f"{i}. **{field}**\n"
        report += f"   - Frequency: {freq}, Checkable: {checkable}, Criticality: {criticality}\n"
        report += f"   - Feasibility: {feasibility}, Impact Score: {impact}\n"
        report += f"   - Relationships Affected: {rel_count}\n"
        if field_info['estimation_methods']:
            report += f"   - Estimation Methods: {', '.join([m['method'] for m in field_info['estimation_methods']])}\n"
        report += "\n"
    
    report += "\n---\n\n## 4. Condition Coverage Analysis\n\n"
    
    cov_summary = coverage_analysis['summary']
    report += f"""
### Overall Coverage

- **Overall Coverage**: {cov_summary['overall_coverage_percentage']}%
- **Total Relationships**: {cov_summary['total_relationships']}
- **Total Checkable Conditions**: {cov_summary['total_checkable_conditions']}
- **API-Available Conditions**: {cov_summary['total_api_available_conditions']}
- **Low Coverage Relationships**: {cov_summary['low_coverage_count']} (< {cov_summary['low_coverage_threshold']}%)

### Coverage by Category

| Category | Relationships | Avg Coverage | Checkable | API-Available |
|----------|---------------|--------------|-----------|---------------|
"""
    
    sorted_categories = sorted(
        coverage_analysis['category_stats'].items(),
        key=lambda x: x[1]['avg_coverage']
    )
    
    for category, stats in sorted_categories:
        report += f"| {category} | {stats['relationships_count']} | {stats['avg_coverage']}% | {stats['checkable_conditions']} | {stats['api_available_conditions']} |\n"
    
    report += "\n---\n\n## 5. Field Taxonomy Summary\n\n"
    
    tax_summary = field_taxonomy['summary']
    report += f"""
- **Total Canonical Fields**: {tax_summary['total_canonical_fields']}
- **Synonym Groups**: {tax_summary['total_synonym_groups']}
- **Categories**: {len(tax_summary['categories'])}

### Categories

"""
    
    for category in sorted(tax_summary['categories']):
        count = sum(1 for f in field_taxonomy['canonical_fields'] if f['category'] == category)
        report += f"- **{category}**: {count} fields\n"
    
    report += "\n---\n\n## 6. Key Findings\n\n"
    
    report += "### Strengths\n\n"
    report += "1. **Good Coverage for Basic Meteorology**: Temperature, humidity, wind, pressure have high coverage\n"
    report += "2. **Air Quality Data Available**: PM2.5, PM10, SO2, NO2, O3, CO available from Open-Meteo\n"
    report += "3. **Temporal Fields Derivable**: Hour, month, season can be derived from timestamps\n"
    report += f"4. **{condition_inv['checkable_percentage']}% Conditions are Checkable**: Most conditions can be evaluated with real data\n\n"
    
    report += "### Gaps & Challenges\n\n"
    report += "1. **Missing Critical Fields**: Aerosol pH, aerosol liquid water are missing but critical\n"
    report += "2. **Low Coverage for Chemical Processes**: Many chemical relationships require estimated variables\n"
    report += "3. **Qualitative Fields**: Precursor availability, particle type cannot be directly measured\n"
    report += f"4. **{stats.get('missing', 0)} Missing Fields**: Need estimation strategies for {gap_analysis['summary']['high_feasibility']} high-feasibility fields\n\n"
    
    report += "---\n\n## 7. Recommendations for Phase 2\n\n"
    
    report += "### High Priority Estimation Tasks\n\n"
    
    high_priority = [
        f for f in gap_analysis['missing_fields']
        if f['criticality'] == 'critical' and f['estimation_feasibility'] == 'high'
    ]
    
    if high_priority:
        report += "Focus on these critical fields with high estimation feasibility:\n\n"
        for field_info in sorted(high_priority, key=lambda x: x['impact_score'], reverse=True)[:5]:
            field = field_info['field']
            methods = field_info['estimation_methods']
            report += f"1. **{field}** (Impact: {field_info['impact_score']})\n"
            report += f"   - Affects {field_info['relationships_affected_count']} relationships\n"
            if methods:
                for method in methods[:2]:  # Top 2 methods
                    report += f"   - Method: {method['method']} (Confidence: {method['confidence']})\n"
                    report += f"   - Required fields: {', '.join(method['required_fields'])}\n"
            report += "\n"
    else:
        report += "No critical high-feasibility fields identified. Focus on important fields with medium-high feasibility.\n\n"
    
    report += "\n### Medium Priority Estimation Tasks\n\n"
    
    medium_priority = [
        f for f in gap_analysis['missing_fields']
        if f['criticality'] == 'important' and f['estimation_feasibility'] in ['high', 'medium']
    ]
    
    if medium_priority:
        report += "These important fields should be addressed after high priority:\n\n"
        for field_info in sorted(medium_priority, key=lambda x: x['impact_score'], reverse=True)[:5]:
            field = field_info['field']
            report += f"- **{field}** (Impact: {field_info['impact_score']}, Feasibility: {field_info['estimation_feasibility']})\n"
    
    report += "\n### Research Tasks for Manus\n\n"
    report += "1. **Estimation Methods Research**: Use Manus to research estimation formulas from literature for:\n"
    report += "   - Aerosol pH estimation\n"
    report += "   - Aerosol liquid water estimation\n"
    report += "   - Inversion detection methods\n"
    report += "   - Cold surge phase identification\n\n"
    
    report += "2. **Validation**: Validate estimation methods against known data or literature values\n\n"
    
    report += "3. **Confidence Scoring**: Develop confidence scoring system for estimated values\n\n"
    
    report += "### Implementation Priorities\n\n"
    report += "1. **Phase 2.1**: Research estimation methods for top 5 high-priority fields\n"
    report += "2. **Phase 2.2**: Implement estimation models with confidence scoring\n"
    report += "3. **Phase 2.3**: Integrate estimation into condition evaluator\n"
    report += "4. **Phase 2.4**: Test and validate estimation accuracy\n\n"
    
    report += "---\n\n## 8. Next Steps\n\n"
    report += "### Immediate Actions\n\n"
    report += "1. Review this comprehensive report\n"
    report += "2. Prioritize estimation tasks based on impact scores\n"
    report += "3. Begin Phase 2: Estimation Strategy Research\n\n"
    
    report += "### Phase 2 Preparation\n\n"
    report += "1. Prepare prompts for Manus to research estimation methods\n"
    report += "2. Identify validation datasets if available\n"
    report += "3. Design estimation pipeline architecture\n"
    report += "4. Plan confidence scoring system\n\n"
    
    report += "---\n\n## Appendix: Data Files Generated\n\n"
    report += "- `data/analysis/condition_inventory.json` - Complete condition inventory\n"
    report += "- `data/analysis/api_mapping_table.json` - API field mappings\n"
    report += "- `data/analysis/gap_analysis.json` - Missing fields analysis\n"
    report += "- `data/analysis/coverage_analysis.json` - Coverage statistics\n"
    report += "- `data/analysis/field_taxonomy.json` - Field taxonomy and synonyms\n"
    report += "- `docs/analysis/condition_inventory_report.md` - Condition inventory report\n"
    report += "- `docs/analysis/api_mapping_report.md` - API mapping report\n"
    report += "- `docs/analysis/gap_analysis_report.md` - Gap analysis report\n"
    report += "- `docs/analysis/coverage_analysis_report.md` - Coverage analysis report\n"
    
    return report


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 6: Generate Comprehensive Report")
    print("=" * 60)
    
    # Load all analysis data
    print("Loading all analysis data...")
    data = load_all_analysis_data()
    
    # Generate report
    print("Generating comprehensive report...")
    report = generate_comprehensive_report(data)
    
    # Save report
    output_report = "docs/analysis/phase1_comprehensive_report.md"
    print(f"\nSaving comprehensive report to {output_report}...")
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 6 Complete!")
    print("=" * 60)
    print("\nPhase 1 Analysis Complete!")
    print("\nAll reports generated:")
    print("  - Condition Inventory Report")
    print("  - API Mapping Report")
    print("  - Gap Analysis Report")
    print("  - Coverage Analysis Report")
    print("  - Comprehensive Report (Phase 1)")


if __name__ == "__main__":
    main()
