# Chain Completeness Analysis

## Current Chain Distribution

| Chain Length | Count |
|--------------|-------|
| 1-step | 61 |
| 2-step | 39 |
| 3-step | 41 |
| 4-step | 39 |
| 5-step | 28 |
| 6-step | 23 |

## Extension Opportunities

### Short Chains to Extend (26 opportunities)

**1. temperature → PM2.5**
- Current: 2-step chain
- Path: temperature → temperature_inversion → pm25
- Potential intermediates: temperature_inversion, ammonium_nitrate_formation, pm25

**2. temperature_inversion → PM2.5**
- Current: 2-step chain
- Path: temperature_inversion → pblh_decrease → pm25
- Potential intermediates: pm25, pblh_decrease

**3. pblh → PM2.5**
- Current: 2-step chain
- Path: pblh → local_accumulation → pm25
- Potential intermediates: pm25, local_accumulation

**4. atmospheric_dispersion → PM2.5**
- Current: 2-step chain
- Path: atmospheric_dispersion → local_accumulation → pm25
- Potential intermediates: local_accumulation, pollution_episode

**5. atmospheric_dispersion → PM2.5**
- Current: 2-step chain
- Path: atmospheric_dispersion → pollution_episode → pm25
- Potential intermediates: local_accumulation, pollution_episode

**6. precipitation → PM2.5**
- Current: 2-step chain
- Path: precipitation → wet_deposition → pm25
- Potential intermediates: wet_deposition, pm25, nitrate

**7. relative_humidity → PM2.5**
- Current: 2-step chain
- Path: relative_humidity → aerosol_liquid_water → pm25
- Potential intermediates: pm25, aerosol_liquid_water

**8. solar_radiation → PM2.5**
- Current: 2-step chain
- Path: solar_radiation → pblh → pm25
- Potential intermediates: pblh, pm25, solar_heating

**9. temperature → PM2.5**
- Current: 3-step chain
- Path: temperature → temperature_inversion → pblh_decrease → pm25
- Potential intermediates: temperature_inversion, ammonium_nitrate_formation, pm25

**10. temperature → PM2.5**
- Current: 3-step chain
- Path: temperature → ammonium_nitrate_formation → sia_formation → pm25
- Potential intermediates: temperature_inversion, ammonium_nitrate_formation, pm25

**11. temperature_inversion → PM2.5**
- Current: 3-step chain
- Path: temperature_inversion → pblh_decrease → atmospheric_mixing → pm25
- Potential intermediates: pm25, pblh_decrease

**12. pblh → PM2.5**
- Current: 3-step chain
- Path: pblh → local_accumulation → secondary_aerosol_formation → pm25
- Potential intermediates: pm25, local_accumulation

**13. wind_speed → PM2.5**
- Current: 3-step chain
- Path: wind_speed → atmospheric_dispersion → local_accumulation → pm25
- Potential intermediates: atmospheric_dispersion, pm25

**14. wind_speed → PM2.5**
- Current: 3-step chain
- Path: wind_speed → atmospheric_dispersion → pollution_episode → pm25
- Potential intermediates: atmospheric_dispersion, pm25

**15. atmospheric_dispersion → PM2.5**
- Current: 3-step chain
- Path: atmospheric_dispersion → local_accumulation → secondary_aerosol_formation → pm25
- Potential intermediates: local_accumulation, pollution_episode

**16. atmospheric_dispersion → PM2.5**
- Current: 3-step chain
- Path: atmospheric_dispersion → pollution_episode → cold_surge_persistence → pm25
- Potential intermediates: local_accumulation, pollution_episode

**17. cold_surge_onset → PM2.5**
- Current: 3-step chain
- Path: cold_surge_onset → atmospheric_transport → regional_transport → pm25
- Potential intermediates: atmospheric_transport, pm25, o3

**18. temperature → PM2.5**
- Current: 1-step chain
- Path: temperature → pm25
- Potential intermediates: temperature_inversion, ammonium_nitrate_formation, pm25

**19. temperature_inversion → PM2.5**
- Current: 1-step chain
- Path: temperature_inversion → pm25
- Potential intermediates: pm25, pblh_decrease

**20. pblh → PM2.5**
- Current: 1-step chain
- Path: pblh → pm25
- Potential intermediates: pm25, local_accumulation

## Complex Mechanism Analysis

### Cold_surge
- Short chains found: 4
- Sample paths:
  - cold_surge_onset → atmospheric_transport → regional_transport → pm25
  - cold_surge_onset → pm25
  - cold_surge_onset → atmospheric_dispersion → local_accumulation → pm25
  - cold_surge_onset → atmospheric_dispersion → pollution_episode → pm25

### Photochemistry
- Short chains found: 3
- Sample paths:
  - solar_radiation → pblh → pm25
  - solar_radiation → pblh → local_accumulation → pm25
  - solar_radiation → pm25

### Winter_chemistry
- Short chains found: 1
- Sample paths:
  - nh3 → sia_formation → pm25

### Precipitation
- Short chains found: 2
- Sample paths:
  - precipitation → wet_deposition → pm25
  - precipitation → pm25
