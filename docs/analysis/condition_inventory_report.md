# Condition Inventory Report

## Executive Summary

- **Total Conditions**: 732
- **Checkable Conditions**: 529 (72.27%)
- **Non-checkable Conditions**: 203
- **Total Relationships**: 255
- **Relationships with Conditions**: 255
- **Unique Fields**: 117
- **Unique Condition Types**: 9

---

## Distribution by Type

- **categorical**: 265 (36.2%)
- **threshold**: 164 (22.4%)
- **qualitative**: 125 (17.08%)
- **month**: 71 (9.7%)
- **season**: 37 (5.05%)
- **time_of_day**: 29 (3.96%)
- **range**: 18 (2.46%)
- **compound**: 17 (2.32%)
- **time_range**: 6 (0.82%)

---

## Top 20 Fields by Frequency

| Field | Frequency | Checkable | Non-checkable | Types |
|-------|-----------|-----------|---------------|-------|
| month | 74 | 74 | 0 | month, compound |
| precursor_availability | 60 | 15 | 45 | qualitative, categorical |
| geographic_region | 60 | 58 | 2 | categorical |
| cold_surge_phase | 49 | 49 | 0 | categorical |
| relative_humidity | 45 | 39 | 6 | range, qualitative, threshold |
| wind_speed | 38 | 38 | 0 | range, threshold |
| season | 37 | 37 | 0 | season |
| time_of_day | 29 | 29 | 0 | time_of_day |
| wind_direction | 24 | 23 | 1 | qualitative, categorical |
| aerosol_ph | 20 | 15 | 5 | range, qualitative, threshold |
| aerosol_liquid_water | 14 | 3 | 11 | range, qualitative, threshold, categorical |
| boundary_layer_height | 14 | 11 | 3 | qualitative, threshold |
| precipitation_occurrence | 14 | 14 | 0 | threshold, categorical |
| cloud_cover | 13 | 13 | 0 | range, threshold, categorical |
| temperature | 12 | 9 | 3 | qualitative, threshold |
| hour | 9 | 9 | 0 | time_range, compound |
| inversion_type | 8 | 3 | 5 | categorical |
| synoptic_pattern | 8 | 4 | 4 | categorical |
| accumulated_precipitation_mm | 8 | 7 | 1 | range, qualitative, threshold |
| monsoon_cycle_duration | 7 | 0 | 7 | qualitative |

---

## Operator Distribution

- **==**: 213 (45.32%)
- **in**: 99 (21.06%)
- **>**: 79 (16.81%)
- **<**: 65 (13.83%)
- **>=**: 8 (1.7%)
- **<=**: 6 (1.28%)

---

## Checkable vs Non-checkable Breakdown

- **Checkable**: 529 conditions (72.27%)
- **Non-checkable**: 203 conditions (27.730000000000004%)

---

## Insights

### Top 10 Checkable Fields

| Field | Checkable Count | Total Count | Checkable Rate |
|-------|-----------------|-------------|---------------|
| month | 74 | 74 | 100.0% |
| geographic_region | 58 | 60 | 96.67% |
| cold_surge_phase | 49 | 49 | 100.0% |
| relative_humidity | 39 | 45 | 86.67% |
| wind_speed | 38 | 38 | 100.0% |
| season | 37 | 37 | 100.0% |
| time_of_day | 29 | 29 | 100.0% |
| wind_direction | 23 | 24 | 95.83% |
| precursor_availability | 15 | 60 | 25.0% |
| aerosol_ph | 15 | 20 | 75.0% |

### Patterns

- Most common condition types: threshold, range, qualitative
- Fields with highest frequency indicate key variables in causal relationships
- Checkable rate indicates how many conditions can be evaluated with real data
