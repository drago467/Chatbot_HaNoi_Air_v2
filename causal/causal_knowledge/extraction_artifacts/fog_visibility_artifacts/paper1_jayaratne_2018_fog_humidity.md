# Paper 1: Jayaratne et al. 2018 - Fog and Humidity Effects on PM Sensors

## Citation
- **Title**: The influence of humidity on the performance of a low-cost air particle mass sensor and the effect of atmospheric fog
- **Authors**: Rohan Jayaratne, Xiaoting Liu, Phong Thai, Matthew Dunbabin, and Lidia Morawska
- **Year**: 2018
- **Journal**: Atmospheric Measurement Techniques
- **DOI**: 10.5194/amt-11-4883-2018
- **URL**: https://amt.copernicus.org/articles/11/4883/2018/
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings

### 1. Humidity Effect on PM Sensors
- **Threshold**: RH > 75% causes significant measurement artifacts
- **Mechanism**: Hygroscopic growth of particles containing salts (NaCl, ammonium sulfate, ammonium nitrate)
- **Deliquescence points**: NaCl ~74%, ammonium sulfate ~79%
- **Effect**: PM2.5 readings increased from 9 µg/m³ at RH 78% to 16 µg/m³ at RH 89% (almost 80% increase)

### 2. Fog Effect on PM Measurements
- **During fog episodes**:
  - Total PNC increased by 28%
  - PNC larger than 2.5 µm increased by over 50%
  - PM10 concentration by PMS1003 was 46% greater than TEOM (with dryer)
- **Mechanism**: Fog droplets are detected as particles by optical sensors without drying facilities

### 3. Key Quotes
> "We found significant increases in particle number and mass concentrations at relative humidity above about 75%."

> "During a period of fog, the total PNC increased by 28%, while the PNC larger than 2.5 µm increased by over 50%."

> "The PM10 concentration reported by the PMS1003 was 46% greater than that on the standard monitor with a charcoal dryer at the inlet."

> "In circumstances where the relative humidity approaches 100%, there is the possibility of mist or fog droplets that are detected as particles."

> "While there is a causal link between particle pollution and adverse health effects, the presence of water on the particles is not harmful to humans."

### 4. Important Notes
- Low-cost optical sensors (PMS1003, DustTrak) do NOT have drying facilities
- Standard TEOM has charcoal heater at inlet to remove liquids
- No simple correction factor can be derived for humidity effects
- Hysteresis effect observed: PM2.5 did not decrease until RH dropped to ~50%

## Relationships to Extract
1. **fog → measurement_artifact_pm25** (DIRECT_CAUSE)
2. **very_high_relative_humidity → measurement_artifact_pm25** (DIRECT_CAUSE)
3. **humidity → hygroscopic_growth → measurement_artifact_pm25** (INDIRECT_CAUSE)
