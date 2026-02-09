"""
Task 5: Field Taxonomy & Normalization

Create canonical taxonomy for all fields (condition fields + API fields) and identify synonyms.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict
import sys
sys.path.append(str(Path(__file__).parent))

from utils import save_json


def load_analysis_data():
    """Load condition inventory and API mapping data."""
    with open("data/analysis/condition_inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    with open("data/analysis/api_mapping_table.json", 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    return inventory, mapping


def identify_synonyms(fields: List[str]) -> Dict[str, List[str]]:
    """Identify synonym groups based on field name patterns."""
    
    synonym_groups = defaultdict(list)
    processed = set()
    
    # Common synonym patterns
    synonym_patterns = {
        "relative_humidity": ["humidity", "rh", "relative_humidity"],
        "temperature": ["temp", "temperature"],
        "wind_speed": ["wind_speed", "ws", "wind"],
        "wind_direction": ["wind_direction", "wind_deg", "wd"],
        "pm25": ["pm25", "pm2.5", "pm2_5", "pm25_concentration"],
        "pm10": ["pm10", "pm10_concentration"],
        "so2": ["so2", "so2_concentration", "sulphur_dioxide"],
        "no2": ["no2", "no2_concentration", "nitrogen_dioxide"],
        "o3": ["o3", "o3_concentration", "ozone"],
        "co": ["co", "co_concentration", "carbon_monoxide"],
        "cloud_cover": ["cloud_cover", "clouds"],
        "precipitation": ["precipitation", "rain", "precip"],
        "boundary_layer_height": ["boundary_layer_height", "pbl", "pblh", "planetary_boundary_layer"],
        "aerosol_liquid_water": ["aerosol_liquid_water", "alw", "aerosol_water_content", "awc"],
        "aerosol_ph": ["aerosol_ph", "ph", "aerosol_pH"],
        "solar_radiation": ["solar_radiation", "solar_rad", "radiation"],
        "uv_index": ["uv_index", "uvi", "uv"],
    }
    
    # Build reverse mapping
    field_to_canonical = {}
    for canonical, aliases in synonym_patterns.items():
        for alias in aliases:
            field_to_canonical[alias.lower()] = canonical
    
    # Group fields by canonical
    for field in fields:
        if field.lower() in processed:
            continue
        
        field_lower = field.lower()
        canonical = field_to_canonical.get(field_lower, field)
        
        if canonical not in synonym_groups:
            synonym_groups[canonical] = []
        
        if field not in synonym_groups[canonical]:
            synonym_groups[canonical].append(field)
        
        processed.add(field_lower)
    
    # Also check for partial matches
    for field in fields:
        if field.lower() in processed:
            continue
        
        # Check if field contains known terms
        for canonical, aliases in synonym_patterns.items():
            for alias in aliases:
                if alias.lower() in field.lower() and field.lower() != alias.lower():
                    if canonical not in synonym_groups:
                        synonym_groups[canonical] = []
                    if field not in synonym_groups[canonical]:
                        synonym_groups[canonical].append(field)
                    processed.add(field.lower())
                    break
    
    return dict(synonym_groups)


def categorize_field(field: str) -> str:
    """Categorize field into domain category."""
    
    field_lower = field.lower()
    
    # Pollutants
    if any(term in field_lower for term in ["pm", "so2", "no2", "o3", "co", "nh3", "voc", "nox"]):
        return "pollutants"
    
    # Meteorology
    if any(term in field_lower for term in ["temperature", "humidity", "wind", "pressure", "cloud", "precipitation", "solar", "uv", "dew"]):
        return "meteorology"
    
    # Aerosol properties
    if any(term in field_lower for term in ["aerosol", "ph", "liquid_water", "alw", "particle"]):
        return "aerosol_properties"
    
    # Atmospheric structure
    if any(term in field_lower for term in ["boundary_layer", "pbl", "inversion", "stability"]):
        return "atmospheric_structure"
    
    # Temporal
    if any(term in field_lower for term in ["time", "hour", "month", "season", "day"]):
        return "temporal"
    
    # Spatial
    if any(term in field_lower for term in ["geographic", "region", "location", "site"]):
        return "spatial"
    
    # Processes
    if any(term in field_lower for term in ["formation", "reaction", "oxidation", "deposition", "transport"]):
        return "processes"
    
    # Events
    if any(term in field_lower for term in ["cold_surge", "monsoon", "event", "episode"]):
        return "events"
    
    # Sources
    if any(term in field_lower for term in ["emission", "source", "traffic", "industry"]):
        return "sources"
    
    # Qualitative
    if any(term in field_lower for term in ["precursor", "availability", "type", "catalysis"]):
        return "qualitative"
    
    return "other"


def get_field_unit(field: str, mapping_info: Dict[str, Any] = None) -> str:
    """Get unit for a field."""
    
    field_lower = field.lower()
    
    # Common units
    if "temperature" in field_lower:
        return "°C"
    elif "humidity" in field_lower:
        return "%"
    elif "wind_speed" in field_lower:
        return "m/s"
    elif "wind_direction" in field_lower:
        return "degrees"
    elif "pressure" in field_lower:
        return "hPa"
    elif "pm" in field_lower or "concentration" in field_lower:
        return "µg/m³"
    elif "precipitation" in field_lower:
        if "intensity" in field_lower:
            return "mm/h"
        else:
            return "mm"
    elif "ph" in field_lower:
        return "pH units"
    elif "cloud" in field_lower:
        return "%"
    elif "uv" in field_lower or "radiation" in field_lower:
        return "varies"
    elif "boundary_layer" in field_lower or "pbl" in field_lower:
        return "m"
    elif "hour" in field_lower or "time" in field_lower:
        return "hour"
    elif "month" in field_lower:
        return "month"
    else:
        return "varies"


def build_field_taxonomy() -> Dict[str, Any]:
    """Build comprehensive field taxonomy."""
    
    print("Loading analysis data...")
    inventory, mapping = load_analysis_data()
    
    # Get all condition fields
    condition_fields = set()
    for field_info in inventory.get("field_frequency", []):
        condition_fields.add(field_info["field"])
    
    # Get API fields from mapping
    api_fields = set()
    for mapping_info in mapping.get("mappings", []):
        api_field = mapping_info.get("api_field")
        api_source = mapping_info.get("api_source")
        if api_field and api_source:
            api_fields.add(f"{api_source}.{api_field}")
    
    # Identify synonyms
    print("Identifying synonyms...")
    all_fields = list(condition_fields)
    synonym_groups = identify_synonyms(all_fields)
    
    # Build canonical fields list
    print("Building canonical fields...")
    canonical_fields = []
    
    # Process synonym groups
    for canonical, aliases in synonym_groups.items():
        # Use the most common alias as canonical if it exists
        if aliases:
            # Find the alias that appears most frequently
            alias_frequencies = {}
            for alias in aliases:
                for field_info in inventory.get("field_frequency", []):
                    if field_info["field"] == alias:
                        alias_frequencies[alias] = field_info["frequency"]
                        break
            
            if alias_frequencies:
                most_common = max(alias_frequencies.items(), key=lambda x: x[1])[0]
                canonical_name = most_common
            else:
                canonical_name = canonical
        else:
            canonical_name = canonical
        
        # Get mapping info
        mapping_info = None
        for m in mapping.get("mappings", []):
            if m.get("condition_field") == canonical_name or m.get("condition_field") in aliases:
                mapping_info = m
                break
        
        category = categorize_field(canonical_name)
        unit = get_field_unit(canonical_name, mapping_info)
        
        # Build API mapping
        api_mapping = {}
        if mapping_info:
            api_source = mapping_info.get("api_source")
            api_field = mapping_info.get("api_field")
            if api_source and api_field:
                api_mapping[api_source] = api_field
        
        canonical_fields.append({
            "canonical": canonical_name,
            "aliases": [a for a in aliases if a != canonical_name],
            "category": category,
            "unit": unit,
            "api_mapping": api_mapping if api_mapping else None,
            "mapping_type": mapping_info.get("mapping_type") if mapping_info else "unknown",
            "description": get_field_description(canonical_name)
        })
    
    # Add fields that don't have synonyms
    processed_fields = set()
    for group in synonym_groups.values():
        processed_fields.update(group)
    
    for field in condition_fields:
        if field not in processed_fields:
            mapping_info = None
            for m in mapping.get("mappings", []):
                if m.get("condition_field") == field:
                    mapping_info = m
                    break
            
            category = categorize_field(field)
            unit = get_field_unit(field, mapping_info)
            
            api_mapping = {}
            if mapping_info:
                api_source = mapping_info.get("api_source")
                api_field = mapping_info.get("api_field")
                if api_source and api_field:
                    api_mapping[api_source] = api_field
            
            canonical_fields.append({
                "canonical": field,
                "aliases": [],
                "category": category,
                "unit": unit,
                "api_mapping": api_mapping if api_mapping else None,
                "mapping_type": mapping_info.get("mapping_type") if mapping_info else "unknown",
                "description": get_field_description(field)
            })
    
    # Sort by category then canonical name
    canonical_fields.sort(key=lambda x: (x["category"], x["canonical"]))
    
    result = {
        "canonical_fields": canonical_fields,
        "synonym_groups": synonym_groups,
        "summary": {
            "total_canonical_fields": len(canonical_fields),
            "total_synonym_groups": len(synonym_groups),
            "categories": list(set(f["category"] for f in canonical_fields))
        }
    }
    
    return result


def get_field_description(field: str) -> str:
    """Get description for a field."""
    
    descriptions = {
        "relative_humidity": "Fraction of water vapor in air relative to saturation, expressed as percentage",
        "temperature": "Air temperature at surface level",
        "wind_speed": "Horizontal wind velocity affecting pollutant dispersion and transport",
        "wind_direction": "Direction from which wind blows, determining pollution source regions",
        "pressure": "Atmospheric pressure at surface level",
        "cloud_cover": "Percentage of sky covered by clouds",
        "precipitation": "Amount of precipitation (rain, snow, etc.)",
        "pm25": "Particulate matter with diameter less than 2.5 micrometers",
        "pm10": "Particulate matter with diameter less than 10 micrometers",
        "so2_concentration": "Sulfur dioxide concentration in air",
        "no2_concentration": "Nitrogen dioxide concentration in air",
        "o3_concentration": "Ozone concentration in air",
        "boundary_layer_height": "Height of planetary boundary layer, affecting vertical mixing",
        "aerosol_ph": "Acidity of aerosol particles, affecting chemical reactions",
        "aerosol_liquid_water": "Liquid water content in aerosol particles",
    }
    
    # Try exact match
    if field in descriptions:
        return descriptions[field]
    
    # Try partial match
    field_lower = field.lower()
    for key, desc in descriptions.items():
        if key.lower() in field_lower or field_lower in key.lower():
            return desc
    
    return f"Field: {field}"


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 5: Field Taxonomy & Normalization")
    print("=" * 60)
    
    # Build taxonomy
    taxonomy = build_field_taxonomy()
    
    # Save JSON
    output_json = "data/analysis/field_taxonomy.json"
    print(f"\nSaving field taxonomy to {output_json}...")
    save_json(taxonomy, output_json)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 5 Complete!")
    print("=" * 60)
    summary = taxonomy["summary"]
    print(f"\nSummary:")
    print(f"  - Total canonical fields: {summary['total_canonical_fields']}")
    print(f"  - Synonym groups: {summary['total_synonym_groups']}")
    print(f"  - Categories: {', '.join(summary['categories'])}")


if __name__ == "__main__":
    main()
