"""Common utilities for Phase 1 analysis scripts."""

import json
from pathlib import Path
from typing import Dict, Any, List


def load_merged_kg(file_path: str = "causal/causal_knowledge/extracted_relationships/merged_knowledge_graph.json") -> Dict[str, Any]:
    """Load merged knowledge graph JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """Save data to JSON file with pretty formatting."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_all_conditions(kg_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all conditions from all relationships."""
    conditions = []
    
    for rel in kg_data.get("relationships", []):
        rel_id = rel.get("id", "unknown")
        rel_category = rel.get("category", "unknown")
        
        for condition in rel.get("conditions", []):
            condition["relationship_id"] = rel_id
            condition["relationship_category"] = rel_category
            conditions.append(condition)
    
    return conditions
