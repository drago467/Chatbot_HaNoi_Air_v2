# Source 1: Mukherjee et al. 2020 - Near-road PM2.5

## Citation
- **Title**: Influence of roadway emissions on near-road PM2.5: Monitoring data analysis and implications
- **Authors**: Anondo Mukherjee, Michael C. McCarthy, Steven G. Brown, ShihMing Huang, Karin Landsberg, Douglas S. Eisinger
- **Year**: 2020
- **Journal**: Transportation Research Part D: Transport and Environment, Volume 86
- **DOI**: https://doi.org/10.1016/j.trd.2020.102442
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings for Static Factors

### Distance to Road - PM2.5 Decay
**Quote 1**: "Incremental PM2.5 decreased 75% between 5 m and 30 m from the roadway."
- Source: Highlights section

**Quote 2**: "Annual average PM2.5 increments, the difference between near-road and background PM2.5, were between 0.1 ± 0.2 µg/m3 and 2.0 ± 0.2 µg/m3 for sites without noted confounding factor(s). The highest PM2.5 increment from monitors 10 or more meters from the roadway was 1.4 ± 0.2 µg/m3."
- Source: Abstract

**Quote 3**: "the PM2.5 increment is estimated to fall ~ 50% between 10 m and 30 m from the roadway"
- Source: Section 4.1

### Distance to Road - Statistical Significance
**Quote 4**: "Distance to road was the variable with the highest relative importance and had the lowest p value"
- Source: Section 3.2, Table 4
- p value = 0.00032 (statistically significant at 99% confidence)
- R² = 0.34 for distance to road vs IDW increment

### Mechanism
- Motor vehicle emissions contribute to PM2.5 through direct emission and precursor gas conversion
- Traffic-related PM2.5 includes: exhaust emissions, brake wear, tire wear, re-suspended road dust
- Factors affecting traffic contribution: traffic mix and volume, vehicle age, vehicle speed, meteorological conditions, local topography, built environment

### Traffic Volume (FE-AADT)
- FE-AADT (Fuel-Equivalent AADT) showed correlation with PM2.5 increment
- R² = 0.12 for FE-AADT vs IDW increment
- p value = 0.127 (not statistically significant alone)

### Combined Model (GAM)
- Overall adjusted R² = 0.63 using distance to road, percent upwind, and FE-AADT
- Distance to road: relative importance = 1
- Percent upwind: relative importance = 0.23
- FE-AADT: relative importance = 0.19

## Relevant for Relationships
1. **distance_to_major_road → pm25** (INDIRECT_CAUSE)
   - Mechanism: PM2.5 concentration decreases with distance due to dilution and dispersion of traffic emissions
   - Decay pattern: ~75% decrease between 5m and 30m; ~50% decrease between 10m and 30m
   - Strength: STRONG
   - Confidence: HIGH

2. **road_network_density → pm25** (INDIRECT_CAUSE)
   - Mechanism: Higher traffic volume (AADT) associated with higher PM2.5 increments
   - Strength: MODERATE
   - Confidence: MEDIUM (R² = 0.12)
