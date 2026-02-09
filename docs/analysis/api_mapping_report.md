# API Mapping Report

## Executive Summary

- **Total Fields Mapped**: 117
- **Coverage**: 26.5%
- **Direct Mappings**: 7
- **Mapped (with transformation)**: 19
- **Derived**: 5
- **Missing**: 86

---

## Coverage by API Source

- **OpenWeatherMap One Call**: 9 fields
- **OpenWeatherMap Air Pollution**: 3 fields
- **Open-Meteo Air Quality**: 1 fields
- **Open-Meteo Weather**: 6 fields
- **Open-Meteo (legacy)**: 9 fields
- **Derived**: 3 fields
- **Missing**: 86 fields

---

## Mapping Types Breakdown

| Type | Count | Percentage |
|------|-------|------------|
| Direct | 7 | 5.98% |
| Mapped | 19 | 16.24% |
| Derived | 5 | 4.27% |
| Missing | 86 | 73.5% |

---

## Field Mappings

### Direct Mappings

- **boundary_layer_height** → `open_meteo_weather.boundary_layer_height` - Direct mapping from Open-Meteo Weather API (hourly variable), unit: meters, verified for Vietnam
- **nh3_concentration** → `openweathermap_air_pollution.nh3` - Direct mapping to NH3 (Ammonia) from OpenWeatherMap Air Pollution API, unit: µg/m³. Only available in OpenWeatherMap, not in Open-Meteo.
- **relative_humidity** → `openweathermap.humidity` - Direct mapping, unit: %
- **stability_index** → `open_meteo_weather.lifted_index` - Direct mapping to Lifted Index from Open-Meteo, unit: K
- **temperature** → `openweathermap.temp` - Direct mapping, unit: Celsius (metric) or Kelvin (standard)
- **visibility** → `openweathermap.visibility` - Direct mapping, unit: meters
- **wind_speed** → `openweathermap.wind_speed` - Direct mapping, unit: m/s (metric)

### Mapped (with transformation)

- **atmospheric_stability** → `open_meteo_weather.cape` - Mapped to CAPE (Convective Available Potential Energy) from Open-Meteo. Can also use lifted_index as alternative.
- **cloud_cover** → `openweathermap.clouds` - clouds is cloud cover percentage (0-100)
- **dust_event** → `open_meteo_air_quality.dust` - Mapped to dust concentration. Can convert to boolean event: >0 µg/m³ = dust event
- **no2_concentration** → `open_meteo.nitrogen_dioxide` - Mapped to nitrogen_dioxide, unit: µg/m³
- **nox_presence** → `openweathermap_air_pollution.no` - Inferred from field name pattern - NO (Nitrogen Monoxide) is component of NOx, only available in OpenWeatherMap Air Pollution API
- **nox_regime** → `openweathermap_air_pollution.no` - Inferred from field name pattern - NO (Nitrogen Monoxide) is component of NOx, only available in OpenWeatherMap Air Pollution API
- **oh_radical_concentration** → `open_meteo.carbon_monoxide` - Inferred from field name pattern
- **ox_concentration** → `open_meteo.carbon_monoxide` - Inferred from field name pattern
- **pm25_concentration** → `open_meteo.pm2_5` - Mapped to pm2_5, unit: µg/m³
- **pm25_initial** → `open_meteo.pm2_5` - Inferred from field name pattern
- **pm25_reduction_near_road** → `open_meteo.pm2_5` - Inferred from field name pattern
- **pm25_residence_time** → `open_meteo.pm2_5` - Inferred from field name pattern
- **precipitation_occurrence** → `open_meteo_weather.precipitation_probability` - Mapped to precipitation_probability (%). Can convert to boolean: >0% = occurrence. More accurate than derived from rain.1h > 0.
- **so2_concentration** → `open_meteo.sulphur_dioxide` - Mapped to sulphur_dioxide, unit: µg/m³
- **solar_radiation** → `open_meteo_weather.shortwave_radiation` - Mapped to shortwave_radiation from Open-Meteo (free, verified for Vietnam). OpenWeatherMap solar_radiation requires subscription.
- **time_of_day** → `open_meteo_weather.is_day` - Mapped to is_day (0/1) from Open-Meteo. More accurate than derived from timestamp.
- **uv_index** → `openweathermap.uvi` - Direct mapping, unit: UV index (0-11+)
- **voc_concentration** → `open_meteo.carbon_monoxide` - Inferred from field name pattern
- **wind_direction** → `openweathermap.wind_deg` - wind_deg is in degrees (0-360)

### Derived Fields

- **accumulated_precipitation_mm** → `openweathermap.rain` - Can be derived from daily precipitation or sum of hourly rain
- **hour** → `derived.dt` - Derived from timestamp (dt field in API response)
- **month** → `derived.dt` - Derived from timestamp
- **precipitation_intensity_mmph** → `openweathermap.rain` - Derived from rain.1h (mm) or snow.1h (mm), represents intensity
- **season** → `derived.dt` - Derived from month and location (Hanoi: Nov-Feb = winter, Mar-May = spring, etc.)

### Missing Fields (Need Estimation)

- **aerosol_liquid_water** - Estimation feasible: Yes, Method: alw_estimation - Can estimate from RH, temperature, and PM2.5 composition
- **aerosol_ph** - Estimation feasible: Yes, Method: ph_estimation - Can estimate from SO2, NO2, NH3 concentrations and RH
- **air_mass_origin** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **air_mass_trajectory** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **atmospheric_layer** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **burning_practice** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **burning_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **cap_event** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **catalysis** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **circulation_pattern** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **city_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **cloud_base_height** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **cloud_liquid_water** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **cloud_water_content** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **cold_surge_phase** - Estimation feasible: Yes, Method: meteorological_pattern - Can estimate from wind direction, temperature, pressure patterns
- **compound_meteorological** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **condensation_sink** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **distance_to_major_road_m** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **distance_to_road_m** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **dry_deposition_efficiency** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **elevation_gradient** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **emission_regime** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **emission_source** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **emissions** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **enso_phase** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **equipment_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **event_lag_days** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **event_lag_hours** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **event_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **fog_duration_hours** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **fog_indicator** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **fuel_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **geographic_region** - Estimation feasible: No, Method: None - Static field, determined by location
- **industrial_zone_presence** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **inversion** - Estimation feasible: Yes, Method: stability_index - Can estimate from temperature gradient, wind speed, cloud cover
- **inversion_presence** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **inversion_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **land_use_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **latitude** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **local_emission_source** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **monsoon_cycle_duration** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **monsoon_regime** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **oc_ratio** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **oh_radical_availability** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **oxidation_products** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **particle_size_um** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **particle_type** - Estimation feasible: No, Method: None - Qualitative field, cannot be directly measured
- **photolysis_rate** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **pollution_level** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **precipitation_duration_hours** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **precipitation_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **precursor_availability** - Estimation feasible: No, Method: None - Qualitative field, cannot be directly measured or estimated
- **regional_pollution_status** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **secondary_aerosol_production** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **sensor_humidity_control** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **sensor_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **site_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **sky_condition** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **soa_formation_rate** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **solar_zenith_angle** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **source_location** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **source_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **spatial_scale** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **sulfate_presence** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **surface_cooling_rate** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **surface_heating** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **synoptic_pattern** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **temporal_scale** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **topography** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **topography_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **transport_distance** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **turbulence** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **upwind_air_quality** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **upwind_source** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **urban_density_class** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **urban_zone_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **uv_radiation** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **uv_wavelength** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **vegetation_type** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **vertical_mixing** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **vertical_motion** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **visibility_condition** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **water_vapor** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **wind_direction_source** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **wind_direction_source_alignment** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review
- **year** - Estimation feasible: Unknown, Method: N/A - Field not found in mapping rules, needs manual review

### Unmapped Fields (Need Manual Review)

- **air_mass_origin**
- **air_mass_trajectory**
- **atmospheric_layer**
- **burning_practice**
- **burning_type**
- **cap_event**
- **catalysis**
- **circulation_pattern**
- **city_type**
- **cloud_base_height**
- **cloud_liquid_water**
- **cloud_water_content**
- **compound_meteorological**
- **condensation_sink**
- **distance_to_major_road_m**
- **distance_to_road_m**
- **dry_deposition_efficiency**
- **elevation_gradient**
- **emission_regime**
- **emission_source**
- **emissions**
- **enso_phase**
- **equipment_type**
- **event_lag_days**
- **event_lag_hours**
- **event_type**
- **fog_duration_hours**
- **fog_indicator**
- **fuel_type**
- **industrial_zone_presence**
- **inversion_presence**
- **inversion_type**
- **land_use_type**
- **latitude**
- **local_emission_source**
- **monsoon_cycle_duration**
- **monsoon_regime**
- **oc_ratio**
- **oh_radical_availability**
- **oxidation_products**
- **particle_size_um**
- **photolysis_rate**
- **pollution_level**
- **precipitation_duration_hours**
- **precipitation_type**
- **regional_pollution_status**
- **secondary_aerosol_production**
- **sensor_humidity_control**
- **sensor_type**
- **site_type**
- **sky_condition**
- **soa_formation_rate**
- **solar_zenith_angle**
- **source_location**
- **source_type**
- **spatial_scale**
- **sulfate_presence**
- **surface_cooling_rate**
- **surface_heating**
- **synoptic_pattern**
- **temporal_scale**
- **topography**
- **topography_type**
- **transport_distance**
- **turbulence**
- **upwind_air_quality**
- **upwind_source**
- **urban_density_class**
- **urban_zone_type**
- **uv_radiation**
- **uv_wavelength**
- **vegetation_type**
- **vertical_mixing**
- **vertical_motion**
- **visibility_condition**
- **water_vapor**
- **wind_direction_source**
- **wind_direction_source_alignment**
- **year**

---

## Recommendations

1. **High Priority for Estimation**: Fields with high frequency and estimation_feasible=True
2. **Manual Review Needed**: Unmapped fields and fields with low confidence
3. **Phase 2 Focus**: Missing fields with estimation_feasible=True should be prioritized for estimation strategy research
