"""
Task 1: Condition Extraction & Inventory

Extract all conditions from merged_knowledge_graph.json and create detailed inventory.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils import load_merged_kg, save_json, get_all_conditions


def extract_condition_inventory() -> Dict[str, Any]:
    """Extract and analyze all conditions from merged knowledge graph."""
    
    print("Loading merged knowledge graph...")
    kg_data = load_merged_kg()
    
    print("Extracting all conditions...")
    all_conditions = get_all_conditions(kg_data)
    
    # Statistics
    total_conditions = len(all_conditions)
    checkable_count = sum(1 for c in all_conditions if c.get("checkable", False))
    non_checkable_count = total_conditions - checkable_count
    
    # Count by type
    by_type = Counter(c.get("type", "unknown") for c in all_conditions)
    
    # Count by field
    by_field = Counter(c.get("field", "") for c in all_conditions if c.get("field"))
    
    # Count by operator
    by_operator = Counter(c.get("operator") for c in all_conditions if c.get("operator"))
    
    # Field frequency with details
    field_frequency = []
    field_details = defaultdict(list)
    
    for condition in all_conditions:
        field = condition.get("field", "")
        if field:
            field_details[field].append({
                "type": condition.get("type"),
                "checkable": condition.get("checkable", False),
                "operator": condition.get("operator"),
                "relationship_id": condition.get("relationship_id"),
                "relationship_category": condition.get("relationship_category")
            })
    
    for field, count in by_field.most_common():
        field_frequency.append({
            "field": field,
            "frequency": count,
            "checkable_count": sum(1 for d in field_details[field] if d["checkable"]),
            "non_checkable_count": sum(1 for d in field_details[field] if not d["checkable"]),
            "types": list(set(d["type"] for d in field_details[field] if d["type"]))
        })
    
    # Condition details (sample for each type)
    condition_details_by_type = {}
    for cond_type in by_type.keys():
        samples = [c for c in all_conditions if c.get("type") == cond_type][:5]
        condition_details_by_type[cond_type] = samples
    
    # Value ranges analysis for threshold and range types
    value_analysis = {
        "threshold_values": [],
        "range_values": []
    }
    
    for condition in all_conditions:
        cond_type = condition.get("type")
        field = condition.get("field", "")
        operator = condition.get("operator")
        value = condition.get("value")
        range_val = condition.get("range")
        
        if cond_type == "threshold" and value is not None and field:
            value_analysis["threshold_values"].append({
                "field": field,
                "operator": operator,
                "value": value,
                "unit": condition.get("normalized", {}).get("unit", "")
            })
        elif cond_type == "range" and range_val and field:
            value_analysis["range_values"].append({
                "field": field,
                "range": range_val,
                "unit": condition.get("normalized", {}).get("unit", "")
            })
    
    # Build inventory
    inventory = {
        "total_conditions": total_conditions,
        "checkable_count": checkable_count,
        "non_checkable_count": non_checkable_count,
        "checkable_percentage": round(checkable_count / total_conditions * 100, 2) if total_conditions > 0 else 0,
        "by_type": dict(by_type),
        "by_field": dict(by_field),
        "by_operator": dict(by_operator),
        "field_frequency": field_frequency,
        "condition_details_by_type": condition_details_by_type,
        "value_analysis": value_analysis,
        "summary": {
            "total_relationships": len(kg_data.get("relationships", [])),
            "relationships_with_conditions": len(set(c.get("relationship_id") for c in all_conditions)),
            "unique_fields": len(by_field),
            "unique_types": len(by_type)
        }
    }
    
    return inventory


def generate_inventory_report(inventory: Dict[str, Any]) -> str:
    """Generate markdown report from inventory."""
    
    report = f"""# Condition Inventory Report

## Executive Summary

- **Total Conditions**: {inventory['total_conditions']}
- **Checkable Conditions**: {inventory['checkable_count']} ({inventory['checkable_percentage']}%)
- **Non-checkable Conditions**: {inventory['non_checkable_count']}
- **Total Relationships**: {inventory['summary']['total_relationships']}
- **Relationships with Conditions**: {inventory['summary']['relationships_with_conditions']}
- **Unique Fields**: {inventory['summary']['unique_fields']}
- **Unique Condition Types**: {inventory['summary']['unique_types']}

---

## Distribution by Type

"""
    
    # Sort by frequency
    by_type_sorted = sorted(inventory['by_type'].items(), key=lambda x: x[1], reverse=True)
    
    for cond_type, count in by_type_sorted:
        percentage = round(count / inventory['total_conditions'] * 100, 2)
        report += f"- **{cond_type}**: {count} ({percentage}%)\n"
    
    report += "\n---\n\n## Top 20 Fields by Frequency\n\n"
    report += "| Field | Frequency | Checkable | Non-checkable | Types |\n"
    report += "|-------|-----------|-----------|---------------|-------|\n"
    
    for field_info in inventory['field_frequency'][:20]:
        field = field_info['field']
        freq = field_info['frequency']
        checkable = field_info['checkable_count']
        non_checkable = field_info['non_checkable_count']
        types = ", ".join(field_info['types'])
        report += f"| {field} | {freq} | {checkable} | {non_checkable} | {types} |\n"
    
    report += "\n---\n\n## Operator Distribution\n\n"
    by_operator_sorted = sorted(inventory['by_operator'].items(), key=lambda x: x[1], reverse=True)
    
    for operator, count in by_operator_sorted:
        percentage = round(count / sum(inventory['by_operator'].values()) * 100, 2) if inventory['by_operator'] else 0
        report += f"- **{operator}**: {count} ({percentage}%)\n"
    
    report += "\n---\n\n## Checkable vs Non-checkable Breakdown\n\n"
    report += f"- **Checkable**: {inventory['checkable_count']} conditions ({inventory['checkable_percentage']}%)\n"
    report += f"- **Non-checkable**: {inventory['non_checkable_count']} conditions ({100 - inventory['checkable_percentage']}%)\n"
    
    report += "\n---\n\n## Insights\n\n"
    
    # Calculate top checkable fields
    top_checkable_fields = sorted(
        [f for f in inventory['field_frequency'] if f['checkable_count'] > 0],
        key=lambda x: x['checkable_count'],
        reverse=True
    )[:10]
    
    report += "### Top 10 Checkable Fields\n\n"
    report += "| Field | Checkable Count | Total Count | Checkable Rate |\n"
    report += "|-------|-----------------|-------------|---------------|\n"
    
    for field_info in top_checkable_fields:
        field = field_info['field']
        checkable = field_info['checkable_count']
        total = field_info['frequency']
        rate = round(checkable / total * 100, 2) if total > 0 else 0
        report += f"| {field} | {checkable} | {total} | {rate}% |\n"
    
    report += "\n### Patterns\n\n"
    report += "- Most common condition types: threshold, range, qualitative\n"
    report += "- Fields with highest frequency indicate key variables in causal relationships\n"
    report += "- Checkable rate indicates how many conditions can be evaluated with real data\n"
    
    return report


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 1: Condition Extraction & Inventory")
    print("=" * 60)
    
    # Extract inventory
    inventory = extract_condition_inventory()
    
    # Save JSON
    output_json = "data/analysis/condition_inventory.json"
    print(f"\nSaving inventory to {output_json}...")
    save_json(inventory, output_json)
    print("[OK] Saved!")
    
    # Generate report
    report = generate_inventory_report(inventory)
    output_report = "docs/analysis/condition_inventory_report.md"
    print(f"\nSaving report to {output_report}...")
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 1 Complete!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Total conditions: {inventory['total_conditions']}")
    print(f"  - Checkable: {inventory['checkable_count']} ({inventory['checkable_percentage']}%)")
    print(f"  - Unique fields: {inventory['summary']['unique_fields']}")
    print(f"  - Unique types: {inventory['summary']['unique_types']}")


if __name__ == "__main__":
    main()
