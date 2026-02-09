# Condition Coverage Analysis Report

## Executive Summary

- **Total Relationships**: 255
- **Total Conditions**: 732
- **Checkable Conditions**: 529
- **API-Available Conditions**: 326
- **Overall Coverage**: 61.63%

---

## Coverage by Category

| Category | Relationships | Avg Coverage | Checkable | API-Available |
|----------|---------------|--------------|-----------|---------------|
| photochemical_formation | 3 | 100.0% | 3 | 3 |
| positive_feedback | 4 | 100.0% | 2 | 2 |
| meteorological_patterns | 4 | 100.0% | 4 | 4 |
| meteorological_pathways | 56 | 80.0% | 115 | 92 |
| seasonal_patterns | 15 | 77.27% | 22 | 17 |
| measurement_artifact | 2 | 66.67% | 3 | 2 |
| diurnal_patterns | 9 | 63.64% | 11 | 7 |
| event_patterns | 7 | 60.0% | 5 | 3 |
| chemical_processes | 47 | 58.33% | 72 | 42 |
| edge_cases | 6 | 56.25% | 16 | 9 |
| transport_mechanisms | 76 | 55.3% | 217 | 120 |
| emission_sources | 17 | 48.84% | 43 | 21 |
| accelerated_chemistry | 3 | 40.0% | 5 | 2 |
| static_factors | 6 | 18.18% | 11 | 2 |

---

## Relationships with Low Coverage (< 50%)

Total: 61 relationships

| Relationship ID | Category | Coverage | Checkable | API-Available | Missing Fields |
|-----------------|----------|----------|-----------|---------------|----------------|
| adv_chem_007 | chemical_processes | 0.0% | 1 | 0 | aerosol_ph |
| adv_chem_008 | chemical_processes | 0.0% | 1 | 0 | aerosol_ph |
| chem_002 | chemical_processes | 0.0% | 2 | 0 | aerosol_ph, precursor_availability |
| chem_005 | chemical_processes | 0.0% | 1 | 0 | precursor_availability |
| chem_008 | chemical_processes | 0.0% | 2 | 0 | precursor_availability |
| chem_009 | chemical_processes | 0.0% | 2 | 0 | precursor_availability, compound_meteorological |
| industry_pm25_001 | emission_sources | 0.0% | 1 | 0 | geographic_region |
| industry_so2_001 | emission_sources | 0.0% | 2 | 0 | fuel_type, geographic_region |
| industry_nox_001 | emission_sources | 0.0% | 2 | 0 | equipment_type, geographic_region |
| power_plants_nox_001 | emission_sources | 0.0% | 1 | 0 | source_type |
| edge_fog_004 | accelerated_chemistry | 0.0% | 1 | 0 | aerosol_liquid_water |
| photo_001 | chemical_processes | 0.0% | 1 | 0 | solar_zenith_angle |
| photo_003 | chemical_processes | 0.0% | 1 | 0 | aerosol_ph |
| photo_010 | chemical_processes | 0.0% | 1 | 0 | aerosol_ph |
| precip_paradox_007 | meteorological_pathways | 0.0% | 1 | 0 | fog_duration_hours |
| precip_paradox_008 | meteorological_pathways | 0.0% | 1 | 0 | fog_indicator |
| met_rain_008 | meteorological_pathways | 0.0% | 3 | 0 | precipitation_type |
| SP002 | seasonal_patterns | 0.0% | 1 | 0 | cold_surge_phase |
| SP014 | event_patterns | 0.0% | 1 | 0 | event_lag_hours |
| SP024 | diurnal_patterns | 0.0% | 1 | 0 | geographic_region |

---

## Coverage Distribution

| Coverage Range | Number of Relationships |
|----------------|-------------------------|
| 0-25% | 53 |
| 25-50% | 27 |
| 50-75% | 73 |
| 75-100% | 102 |

---

## Improvement Opportunities

### Most Common Missing Fields in Low Coverage Relationships

| Field | Frequency |
|-------|-----------|
| aerosol_ph | 5 |
| precursor_availability | 4 |
| geographic_region | 4 |
| compound_meteorological | 1 |
| fuel_type | 1 |
| equipment_type | 1 |
| source_type | 1 |
| aerosol_liquid_water | 1 |
| solar_zenith_angle | 1 |
| fog_duration_hours | 1 |

### Recommendations

1. **High Priority**: Focus on estimating fields that appear frequently in low coverage relationships
2. **Category Focus**: Prioritize categories with lowest average coverage
3. **Phase 2**: Use gap analysis results to prioritize estimation strategy research
