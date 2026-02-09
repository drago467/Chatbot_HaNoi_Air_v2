# Variables Coverage Checklist
# Đảm bảo tất cả các biến đã được cover trong prompts

## ✅ Meteorology Variables

### Core Variables (Prompt 01):
- [x] `temperature` → Inversion, PBLH, PM2.5
- [x] `humidity` → Chemical reactions, ALW, PM2.5
- [x] `wind_speed` → Dispersion, Transport, PM2.5
- [x] `wind_direction` → Transport, PM2.5
- [x] `pblh` → PM2.5
- [x] `precipitation` → Wet deposition, PM2.5
- [x] `cloud_cover` → Solar radiation, PBLH, PM2.5
- [x] `pressure` → Atmospheric stability, Inversion, PM2.5
- [x] `solar_radiation` → PBLH, Photochemistry, PM2.5
- [x] `visibility` → Fog, PM2.5 (measurement artifact)
- [x] `dew_point` → Condensation, PM2.5
- [x] `stability_index` → Atmospheric stability, PM2.5

## ✅ Pollutants

### Primary Pollutants:
- [x] `pm25` → Target variable
- [x] `pm10` → Related to PM2.5
- [x] `co` → Indicator of traffic emissions

### Precursors (Prompt 02):
- [x] `so2` → Sulfate formation, SIA, PM2.5
- [x] `no2` → Nitrate formation, O3, SIA, PM2.5
- [x] `nox` → O3, Nitrate formation, PM2.5
- [x] `nh3` → Ammonium nitrate formation, SIA, PM2.5
- [x] `o3` → Secondary aerosols, PM2.5
- [x] `vocs` → O3, SOA formation, PM2.5
- [x] `hno3` → Ammonium nitrate formation, PM2.5
- [x] `h2o2` → Sulfate formation, PM2.5

## ✅ Processes/Phenomena

### Meteorological Processes (Prompt 01):
- [x] `inversion` → PBLH, Dispersion, PM2.5
- [x] `dispersion` → PM2.5
- [x] `atmospheric_stability` → Dispersion, PM2.5
- [x] `wet_deposition` → PM2.5
- [x] `dry_deposition` → PM2.5

### Chemical Processes (Prompt 02):
- [x] `chemical_reaction` → SIA formation, SOA formation, PM2.5
- [x] `photochemistry` → O3, SOA formation, PM2.5
- [x] `aqueous_phase_reaction` → Sulfate formation, Nitrate formation, PM2.5
- [x] `heterogeneous_reaction` → Ammonium nitrate formation, PM2.5
- [x] `sia_formation` → PM2.5
- [x] `soa_formation` → PM2.5
- [x] `sulfate_formation` → PM2.5
- [x] `nitrate_formation` → PM2.5
- [x] `ammonium_nitrate_formation` → PM2.5
- [x] `aerosol_liquid_water` → Aqueous-phase reaction, SIA formation, PM2.5

### Transport Processes (Prompt 03):
- [x] `transport` → PM2.5
- [x] `regional_transport` → PM2.5
- [x] `long_range_transport` → PM2.5
- [x] `back_trajectory` → Source identification, PM2.5

### Phenomena:
- [x] `cold_surge` → Wind pattern, Atmospheric stability, PM2.5 (Prompt 01, 03)

## ✅ Emission Sources (Prompt 04)

- [x] `traffic` → NOx, CO, PM2.5 primary, PM2.5
- [x] `industry` → SO2, NOx, Heavy metals, PM2.5
- [x] `biomass_burning` → PM2.5 primary, VOCs, NOx, PM2.5
- [x] `construction` → Resuspension, PM2.5
- [x] `power_plants` → SO2, NOx, PM2.5
- [x] `residential_heating` → PM2.5 primary, PM2.5

## ✅ Static Factors (Prompt 05)

- [x] `population_density` → Emission intensity, PM2.5
- [x] `urban_density` → Emission sources, PM2.5
- [x] `urban_land_use` → Emission patterns, PM2.5
- [x] `vegetation` → Deposition, PM2.5
- [x] `topography` → Air flow, PM2.5
- [x] `valley_bottom` → Air trapping, PM2.5
- [x] `topographic_wetness_index` → Air flow, PM2.5
- [x] `distance_to_roads` → Traffic exposure, PM2.5
- [x] `industrial_zones` → Emissions, PM2.5

## ✅ Temporal/Seasonal Patterns (Prompt 06)

### Seasonal:
- [x] `season_winter` → Weather pattern, Emission pattern, PM2.5
- [x] `season_summer` → Weather pattern, PM2.5
- [x] `season_dry` → Biomass burning, PM2.5
- [x] `season_wet` → Wet deposition, PM2.5

### Diurnal:
- [x] `time_of_day_night` → PBLH, Inversion, PM2.5
- [x] `time_of_day_morning` → PBLH, PM2.5
- [x] `time_of_day_afternoon` → PBLH, PM2.5
- [x] `time_of_day_evening` → Emission intensity, PBLH, PM2.5
- [x] `time_of_day_rush_hour` → Emission intensity, PM2.5

### Monthly/Event-based:
- [x] `month_harvest` → Biomass burning, PM2.5
- [x] `holiday_period` → Traffic pattern, PM2.5
- [x] `weekday` → Traffic pattern, PM2.5
- [x] `weekend` → Traffic pattern, PM2.5

## ✅ Edge Cases (Prompt 07)

- [x] Humidity → PM2.5 (non-linear, measurement artifact)
- [x] Wind Speed → PM2.5 (exception: transport from sources)
- [x] Precipitation → PM2.5 (exception: light rain)
- [x] Temperature → PM2.5 (exception: high temp + high emissions)
- [x] Cold Surge → PM2.5 (non-linear, delayed effect)
- [x] Wind Direction → PM2.5 (exception: clean air from sea)
- [x] Multiple factors interaction (confounding)

## Summary

### Total Variables Covered:
- **Meteorology**: 12 variables ✅
- **Pollutants**: 13 variables ✅
- **Processes**: 20+ processes ✅
- **Emission Sources**: 6 sources ✅
- **Static Factors**: 9 factors ✅
- **Temporal Patterns**: 12+ patterns ✅
- **Edge Cases**: 7+ cases ✅

### Coverage by Prompt:
- **Prompt 01**: Meteorology pathways ✅
- **Prompt 02**: Chemical processes ✅
- **Prompt 03**: Transport mechanisms ✅
- **Prompt 04**: Emission sources ✅
- **Prompt 05**: Static factors ✅
- **Prompt 06**: Seasonal patterns ✅
- **Prompt 07**: Edge cases ✅

## Notes

1. Một số biến có thể xuất hiện trong nhiều prompts (ví dụ: `humidity` xuất hiện trong Prompt 01, 02, và 07)
2. Đây là checklist để đảm bảo coverage, không phải danh sách đầy đủ tất cả các biến có thể có
3. Khi extract từ papers mới, có thể phát hiện thêm các biến mới → Cần update checklist này
