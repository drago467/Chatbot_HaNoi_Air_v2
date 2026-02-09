"""
Task 2: API Field Mapping

Map condition fields to API fields (OpenWeatherMap + Open-Meteo) with confidence scores.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys
sys.path.append(str(Path(__file__).parent))

from utils import load_merged_kg, save_json, get_all_conditions


# API field definitions
OPENWEATHERMAP_FIELDS = {
    # Current weather
    "temp": "temperature",
    "feels_like": "feels_like_temperature",
    "pressure": "pressure",
    "humidity": "relative_humidity",
    "dew_point": "dew_point",
    "uvi": "uv_index",
    "clouds": "cloud_cover",
    "visibility": "visibility",
    "wind_speed": "wind_speed",
    "wind_deg": "wind_direction",
    "wind_gust": "wind_gust",
    "rain": "precipitation",
    "snow": "snow",
    "solar_radiation": "solar_radiation",
    # Hourly forecast
    "pop": "precipitation_probability",
    # Daily forecast
    "temp_min": "temperature_min",
    "temp_max": "temperature_max",
    "temp_morn": "temperature_morning",
    "temp_day": "temperature_day",
    "temp_eve": "temperature_evening",
    "temp_night": "temperature_night",
}

OPEN_METEO_AQ_FIELDS = {
    "pm10": "pm10",
    "pm2_5": "pm25",
    "carbon_monoxide": "co",
    "carbon_dioxide": "co2",
    "nitrogen_dioxide": "no2",
    "sulphur_dioxide": "so2",
    "ozone": "o3",
    "methane": "ch4",
    "aerosol_optical_depth": "aerosol_optical_depth",
    "dust": "dust",
    "uv_index": "uv_index",
    "uv_index_clear_sky": "uv_index_clear_sky",
}

OPEN_METEO_WEATHER_FIELDS = {
    # Temperature
    "temperature_2m": "temperature",
    "dewpoint_2m": "dew_point",
    "apparent_temperature": "feels_like_temperature",
    # Humidity
    "relative_humidity_2m": "relative_humidity",
    "vapour_pressure_deficit": "vapour_pressure_deficit",
    # Precipitation
    "precipitation": "precipitation",
    "rain": "rain",
    "precipitation_probability": "precipitation_probability",
    # Wind
    "wind_speed_10m": "wind_speed",
    "wind_direction_10m": "wind_direction",
    "wind_gusts_10m": "wind_gust",
    # Pressure
    "pressure_msl": "pressure",
    "surface_pressure": "surface_pressure",
    # Cloud & Visibility
    "cloud_cover": "cloud_cover",
    "visibility": "visibility",
    # Radiation
    "shortwave_radiation": "solar_radiation",
    "direct_radiation": "direct_radiation",
    "diffuse_radiation": "diffuse_radiation",
    # Atmospheric
    "cape": "atmospheric_stability",
    "lifted_index": "stability_index",
    "boundary_layer_height": "boundary_layer_height",
    "is_day": "time_of_day",
    "sunshine_duration": "sunshine_duration",
}

OPENWEATHERMAP_AIR_POLLUTION_FIELDS = {
    "pm2_5": "pm25",
    "pm10": "pm10",
    "co": "co",
    "no": "no",  # Nitrogen Monoxide - QUAN TRỌNG cho NOx
    "no2": "no2",
    "so2": "so2",
    "o3": "o3",
    "nh3": "nh3",  # Ammonia - QUAN TRỌNG
    "aqi": "aqi",
}


def create_field_mapping_rules() -> Dict[str, Dict[str, Any]]:
    """Create mapping rules for condition fields to API fields."""
    
    # Direct mappings (exact match or obvious synonyms)
    direct_mappings = {
        "temperature": {
            "api_source": "openweathermap",
            "api_field": "temp",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: Celsius (metric) or Kelvin (standard)"
        },
        "relative_humidity": {
            "api_source": "openweathermap",
            "api_field": "humidity",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: %"
        },
        "wind_speed": {
            "api_source": "openweathermap",
            "api_field": "wind_speed",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: m/s (metric)"
        },
        "wind_direction": {
            "api_source": "openweathermap",
            "api_field": "wind_deg",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "wind_deg is in degrees (0-360)"
        },
        "pressure": {
            "api_source": "open_meteo_weather",
            "api_field": "pressure_msl",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to pressure_msl (Mean Sea Level Pressure) from Open-Meteo. More accurate than OpenWeatherMap pressure."
        },
        "cloud_cover": {
            "api_source": "openweathermap",
            "api_field": "clouds",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "clouds is cloud cover percentage (0-100)"
        },
        "precipitation_occurrence": {
            "api_source": "open_meteo_weather",
            "api_field": "precipitation_probability",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "unit_conversion": {"from": "%", "to": "boolean", "method": "threshold", "threshold": 0},
            "notes": "Mapped to precipitation_probability (%). Can convert to boolean: >0% = occurrence. More accurate than derived from rain.1h > 0."
        },
        "precipitation_intensity_mmph": {
            "api_source": "openweathermap",
            "api_field": "rain",
            "mapping_type": "derived",
            "confidence": 0.8,
            "unit_conversion": {"from": "mm", "to": "mm/h", "factor": 1.0},
            "notes": "Derived from rain.1h (mm) or snow.1h (mm), represents intensity"
        },
        "accumulated_precipitation_mm": {
            "api_source": "openweathermap",
            "api_field": "rain",
            "mapping_type": "derived",
            "confidence": 0.7,
            "unit_conversion": None,
            "notes": "Can be derived from daily precipitation or sum of hourly rain"
        },
        "precipitation": {
            "api_source": "openweathermap",
            "api_field": "rain",
            "mapping_type": "mapped",
            "confidence": 0.8,
            "unit_conversion": None,
            "notes": "Legacy field, maps to rain.1h"
        },
        "solar_radiation": {
            "api_source": "open_meteo_weather",
            "api_field": "shortwave_radiation",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to shortwave_radiation from Open-Meteo (free, verified for Vietnam). OpenWeatherMap solar_radiation requires subscription."
        },
        "uv_index": {
            "api_source": "openweathermap",
            "api_field": "uvi",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: UV index (0-11+)"
        },
        "dew_point": {
            "api_source": "openweathermap",
            "api_field": "dew_point",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: Celsius"
        },
        "visibility": {
            "api_source": "openweathermap",
            "api_field": "visibility",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: meters"
        },
        # Air quality fields
        "pm25_concentration": {
            "api_source": "open_meteo",
            "api_field": "pm2_5",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to pm2_5, unit: µg/m³"
        },
        "pm25": {
            "api_source": "open_meteo",
            "api_field": "pm2_5",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: µg/m³"
        },
        "pm10": {
            "api_source": "open_meteo",
            "api_field": "pm10",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping, unit: µg/m³"
        },
        "so2_concentration": {
            "api_source": "open_meteo",
            "api_field": "sulphur_dioxide",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to sulphur_dioxide, unit: µg/m³"
        },
        "no2_concentration": {
            "api_source": "open_meteo",
            "api_field": "nitrogen_dioxide",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to nitrogen_dioxide, unit: µg/m³"
        },
        "o3_concentration": {
            "api_source": "open_meteo",
            "api_field": "ozone",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to ozone, unit: µg/m³"
        },
        "co_concentration": {
            "api_source": "open_meteo",
            "api_field": "carbon_monoxide",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to carbon_monoxide, unit: µg/m³"
        },
        # Temporal fields
        "hour": {
            "api_source": "derived",
            "api_field": "dt",
            "mapping_type": "derived",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Derived from timestamp (dt field in API response)"
        },
        "time_of_day": {
            "api_source": "open_meteo_weather",
            "api_field": "is_day",
            "mapping_type": "mapped",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Mapped to is_day (0/1) from Open-Meteo. More accurate than derived from timestamp."
        },
        "month": {
            "api_source": "derived",
            "api_field": "dt",
            "mapping_type": "derived",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Derived from timestamp"
        },
        "season": {
            "api_source": "derived",
            "api_field": "dt",
            "mapping_type": "derived",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Derived from month and location (Hanoi: Nov-Feb = winter, Mar-May = spring, etc.)"
        },
        # Open-Meteo Weather API mappings (ưu tiên vì miễn phí và đầy đủ hơn)
        "atmospheric_stability": {
            "api_source": "open_meteo_weather",
            "api_field": "cape",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "unit_conversion": None,
            "notes": "Mapped to CAPE (Convective Available Potential Energy) from Open-Meteo. Can also use lifted_index as alternative."
        },
        "stability_index": {
            "api_source": "open_meteo_weather",
            "api_field": "lifted_index",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping to Lifted Index from Open-Meteo, unit: K"
        },
        "dust_event": {
            "api_source": "open_meteo_air_quality",
            "api_field": "dust",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "unit_conversion": {"from": "µg/m³", "to": "boolean", "method": "threshold", "threshold": 0},
            "notes": "Mapped to dust concentration. Can convert to boolean event: >0 µg/m³ = dust event"
        },
        "nh3_concentration": {
            "api_source": "openweathermap_air_pollution",
            "api_field": "nh3",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping to NH3 (Ammonia) from OpenWeatherMap Air Pollution API, unit: µg/m³. Only available in OpenWeatherMap, not in Open-Meteo."
        },
        "no_concentration": {
            "api_source": "openweathermap_air_pollution",
            "api_field": "no",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping to NO (Nitrogen Monoxide) from OpenWeatherMap Air Pollution API, unit: µg/m³. Important for NOx regime analysis."
        },
    }
    
    # Missing fields (not available in API, need estimation)
    missing_fields = {
        "boundary_layer_height": {
            "api_source": "open_meteo_weather",
            "api_field": "boundary_layer_height",
            "mapping_type": "direct",
            "confidence": 1.0,
            "unit_conversion": None,
            "notes": "Direct mapping from Open-Meteo Weather API (hourly variable), unit: meters, verified for Vietnam"
        },
        "aerosol_ph": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": True,
            "estimation_method": "ph_estimation",
            "notes": "Can estimate from SO2, NO2, NH3 concentrations and RH"
        },
        "aerosol_liquid_water": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": True,
            "estimation_method": "alw_estimation",
            "notes": "Can estimate from RH, temperature, and PM2.5 composition"
        },
        "inversion": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": True,
            "estimation_method": "stability_index",
            "notes": "Can estimate from temperature gradient, wind speed, cloud cover"
        },
        "precursor_availability": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": False,
            "estimation_method": None,
            "notes": "Qualitative field, cannot be directly measured or estimated"
        },
        "particle_type": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": False,
            "estimation_method": None,
            "notes": "Qualitative field, cannot be directly measured"
        },
        "geographic_region": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": False,
            "estimation_method": None,
            "notes": "Static field, determined by location"
        },
        "cold_surge_phase": {
            "api_source": None,
            "api_field": None,
            "mapping_type": "missing",
            "confidence": 0.0,
            "estimation_feasible": True,
            "estimation_method": "meteorological_pattern",
            "notes": "Can estimate from wind direction, temperature, pressure patterns"
        },
    }
    
    return {**direct_mappings, **missing_fields}


def map_conditions_to_api() -> Dict[str, Any]:
    """Map all condition fields to API fields."""
    
    print("Loading condition inventory...")
    with open("data/analysis/condition_inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    print("Creating field mapping rules...")
    mapping_rules = create_field_mapping_rules()
    
    # Get all unique fields from conditions
    all_fields = set()
    for field_info in inventory.get("field_frequency", []):
        all_fields.add(field_info["field"])
    
    # Create mappings for all fields
    mappings = []
    unmapped_fields = []
    
    for field in sorted(all_fields):
        if field in mapping_rules:
            mapping = mapping_rules[field].copy()
            mapping["condition_field"] = field
            mappings.append(mapping)
        else:
            # Try to infer mapping
            inferred = infer_mapping(field)
            if inferred:
                inferred["condition_field"] = field
                mappings.append(inferred)
            else:
                unmapped_fields.append(field)
                # Add as missing
                mappings.append({
                    "condition_field": field,
                    "api_source": None,
                    "api_field": None,
                    "mapping_type": "missing",
                    "confidence": 0.0,
                    "estimation_feasible": None,
                    "notes": f"Field not found in mapping rules, needs manual review"
                })
    
    # Calculate coverage statistics
    direct_count = sum(1 for m in mappings if m.get("mapping_type") == "direct")
    mapped_count = sum(1 for m in mappings if m.get("mapping_type") == "mapped")
    derived_count = sum(1 for m in mappings if m.get("mapping_type") == "derived")
    missing_count = sum(1 for m in mappings if m.get("mapping_type") == "missing")
    total_mapped = direct_count + mapped_count + derived_count
    total_fields = len(mappings)
    coverage_percentage = round(total_mapped / total_fields * 100, 2) if total_fields > 0 else 0
    
    result = {
        "mappings": mappings,
        "coverage_stats": {
            "direct_mapping": direct_count,
            "mapped": mapped_count,
            "derived": derived_count,
            "missing": missing_count,
            "total_fields": total_fields,
            "coverage_percentage": coverage_percentage
        },
        "unmapped_fields": unmapped_fields,
        "api_sources": {
            "openweathermap": sum(1 for m in mappings if m.get("api_source") == "openweathermap"),
            "openweathermap_air_pollution": sum(1 for m in mappings if m.get("api_source") == "openweathermap_air_pollution"),
            "open_meteo": sum(1 for m in mappings if m.get("api_source") == "open_meteo"),
            "open_meteo_air_quality": sum(1 for m in mappings if m.get("api_source") == "open_meteo_air_quality"),
            "open_meteo_weather": sum(1 for m in mappings if m.get("api_source") == "open_meteo_weather"),
            "derived": sum(1 for m in mappings if m.get("api_source") == "derived"),
            "missing": sum(1 for m in mappings if m.get("api_source") is None)
        }
    }
    
    return result


def infer_mapping(field: str) -> Optional[Dict[str, Any]]:
    """Try to infer API mapping for a field based on name patterns."""
    
    field_lower = field.lower()
    
    # Pattern matching
    if "pm25" in field_lower or "pm2.5" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "pm2_5",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern"
        }
    elif "pm10" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "pm10",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern"
        }
    elif "so2" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "sulphur_dioxide",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern"
        }
    elif "no2" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "nitrogen_dioxide",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern"
        }
    elif "o3" in field_lower or "ozone" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "ozone",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern"
        }
    elif "co" in field_lower and "concentration" in field_lower:
        return {
            "api_source": "open_meteo",
            "api_field": "carbon_monoxide",
            "mapping_type": "mapped",
            "confidence": 0.8,
            "notes": "Inferred from field name pattern"
        }
    elif "nh3" in field_lower or "ammonia" in field_lower:
        return {
            "api_source": "openweathermap_air_pollution",
            "api_field": "nh3",
            "mapping_type": "mapped",
            "confidence": 0.9,
            "notes": "Inferred from field name pattern - NH3 only available in OpenWeatherMap Air Pollution API"
        }
    elif ("nox" in field_lower or ("no" in field_lower and "no2" not in field_lower)) and ("regime" in field_lower or "presence" in field_lower):
        return {
            "api_source": "openweathermap_air_pollution",
            "api_field": "no",
            "mapping_type": "mapped",
            "confidence": 0.8,
            "notes": "Inferred from field name pattern - NO (Nitrogen Monoxide) is component of NOx, only available in OpenWeatherMap Air Pollution API"
        }
    
    return None


def generate_mapping_report(mapping_data: Dict[str, Any]) -> str:
    """Generate markdown report from mapping data."""
    
    stats = mapping_data["coverage_stats"]
    api_sources = mapping_data["api_sources"]
    
    report = f"""# API Mapping Report

## Executive Summary

- **Total Fields Mapped**: {stats['total_fields']}
- **Coverage**: {stats['coverage_percentage']}%
- **Direct Mappings**: {stats['direct_mapping']}
- **Mapped (with transformation)**: {stats['mapped']}
- **Derived**: {stats['derived']}
- **Missing**: {stats['missing']}

---

## Coverage by API Source

- **OpenWeatherMap One Call**: {api_sources.get('openweathermap', 0)} fields
- **OpenWeatherMap Air Pollution**: {api_sources.get('openweathermap_air_pollution', 0)} fields
- **Open-Meteo Air Quality**: {api_sources.get('open_meteo_air_quality', 0)} fields
- **Open-Meteo Weather**: {api_sources.get('open_meteo_weather', 0)} fields
- **Open-Meteo (legacy)**: {api_sources.get('open_meteo', 0)} fields
- **Derived**: {api_sources.get('derived', 0)} fields
- **Missing**: {api_sources.get('missing', 0)} fields

---

## Mapping Types Breakdown

| Type | Count | Percentage |
|------|-------|------------|
| Direct | {stats['direct_mapping']} | {round(stats['direct_mapping'] / stats['total_fields'] * 100, 2)}% |
| Mapped | {stats['mapped']} | {round(stats['mapped'] / stats['total_fields'] * 100, 2)}% |
| Derived | {stats['derived']} | {round(stats['derived'] / stats['total_fields'] * 100, 2)}% |
| Missing | {stats['missing']} | {round(stats['missing'] / stats['total_fields'] * 100, 2)}% |

---

## Field Mappings

### Direct Mappings

"""
    
    direct_mappings = [m for m in mapping_data["mappings"] if m.get("mapping_type") == "direct"]
    for mapping in sorted(direct_mappings, key=lambda x: x.get("condition_field", "")):
        field = mapping.get("condition_field", "")
        api_field = mapping.get("api_field", "")
        api_source = mapping.get("api_source", "")
        notes = mapping.get("notes", "")
        report += f"- **{field}** → `{api_source}.{api_field}` - {notes}\n"
    
    report += "\n### Mapped (with transformation)\n\n"
    mapped_fields = [m for m in mapping_data["mappings"] if m.get("mapping_type") == "mapped"]
    for mapping in sorted(mapped_fields, key=lambda x: x.get("condition_field", "")):
        field = mapping.get("condition_field", "")
        api_field = mapping.get("api_field", "")
        api_source = mapping.get("api_source", "")
        notes = mapping.get("notes", "")
        report += f"- **{field}** → `{api_source}.{api_field}` - {notes}\n"
    
    report += "\n### Derived Fields\n\n"
    derived_fields = [m for m in mapping_data["mappings"] if m.get("mapping_type") == "derived"]
    for mapping in sorted(derived_fields, key=lambda x: x.get("condition_field", "")):
        field = mapping.get("condition_field", "")
        api_field = mapping.get("api_field", "")
        api_source = mapping.get("api_source", "")
        notes = mapping.get("notes", "")
        report += f"- **{field}** → `{api_source}.{api_field}` - {notes}\n"
    
    report += "\n### Missing Fields (Need Estimation)\n\n"
    missing_fields = [m for m in mapping_data["mappings"] if m.get("mapping_type") == "missing"]
    for mapping in sorted(missing_fields, key=lambda x: x.get("condition_field", "")):
        field = mapping.get("condition_field", "")
        estimation_feasible = mapping.get("estimation_feasible")
        estimation_method = mapping.get("estimation_method", "N/A")
        notes = mapping.get("notes", "")
        
        feasible_str = "Yes" if estimation_feasible else "No" if estimation_feasible is False else "Unknown"
        report += f"- **{field}** - Estimation feasible: {feasible_str}, Method: {estimation_method} - {notes}\n"
    
    if mapping_data.get("unmapped_fields"):
        report += "\n### Unmapped Fields (Need Manual Review)\n\n"
        for field in sorted(mapping_data["unmapped_fields"]):
            report += f"- **{field}**\n"
    
    report += "\n---\n\n## Recommendations\n\n"
    report += "1. **High Priority for Estimation**: Fields with high frequency and estimation_feasible=True\n"
    report += "2. **Manual Review Needed**: Unmapped fields and fields with low confidence\n"
    report += "3. **Phase 2 Focus**: Missing fields with estimation_feasible=True should be prioritized for estimation strategy research\n"
    
    return report


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 2: API Field Mapping")
    print("=" * 60)
    
    # Map conditions to API
    mapping_data = map_conditions_to_api()
    
    # Save JSON
    output_json = "data/analysis/api_mapping_table.json"
    print(f"\nSaving mapping table to {output_json}...")
    save_json(mapping_data, output_json)
    print("[OK] Saved!")
    
    # Generate report
    report = generate_mapping_report(mapping_data)
    output_report = "docs/analysis/api_mapping_report.md"
    print(f"\nSaving report to {output_report}...")
    Path(output_report).parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[OK] Saved!")
    
    print("\n" + "=" * 60)
    print("Task 2 Complete!")
    print("=" * 60)
    stats = mapping_data["coverage_stats"]
    print(f"\nSummary:")
    print(f"  - Total fields: {stats['total_fields']}")
    print(f"  - Coverage: {stats['coverage_percentage']}%")
    print(f"  - Direct: {stats['direct_mapping']}, Mapped: {stats['mapped']}, Derived: {stats['derived']}, Missing: {stats['missing']}")


if __name__ == "__main__":
    main()
