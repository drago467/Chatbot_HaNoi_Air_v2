# Paper 5: Kim et al. 2023 - Effects of Gas and Steam Humidity on PM Measurements

## Citation
- **Title**: Effects of Gas and Steam Humidity on Particulate Matter Measurements Obtained Using Light-Scattering Sensors
- **Authors**: Hyunsik Kim, Jeonghwan Kim, Seungjun Roh
- **Year**: 2023
- **Journal**: Sensors (Basel)
- **DOI**: 10.3390/s23136199
- **PMCID**: PMC10347098
- **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10347098/
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings

### 1. Gaseous vs Steam Humidity
The study clearly distinguishes between two types of humidity effects on light-scattering PM sensors:
- **Gaseous humidity**: Did NOT cause errors in PM measurements
- **Steam humidity (fog)**: Resulted in significant errors in PM measurement

### 2. Mechanism Explanation
Light-scattering sensors count aerosols in solid and liquid states. Steam vapor (liquid aerosol like fog) can be detected as particles, while gaseous humidity theoretically cannot be the primary factor affecting PM concentration.

### 3. Quantitative Results
- In steam RH test, PM concentrations increased linearly with RH below 70%
- Correlation coefficients: 0.767 (PM1.0), 0.756 (PM2.5), 0.740 (PM10)
- Above RH 70%, sudden fall in measured concentrations (steam particles combining to form water drops)

### 4. Key Quotes
> "The gaseous humidity did not cause errors in the PM measurements via the light-scattering method. In contrast, steam humidity, such as that caused by fog, resulted in errors in the PM measurement."

> "RH is a concept indicating the concentration of vapor in a gaseous state in the atmosphere, and therefore, it theoretically cannot be the primary factor affecting the PM concentration in the light-scattering method, as the method counts the aerosols in solid and liquid states."

> "If the vapor is not in a gaseous state but a state of liquid aerosol (or steam), such as fog, it could be the target of light-scattering sensors."

> "Since the most representative phenomenon of steam vapor is fog, value correction should be considered for the PM data collected in a foggy environment."

### 5. Practical Implications
- Light-scattering sensors measure steam vapor aerosols as particles
- Value correction should be considered for PM data collected in foggy environments
- Distinction between gaseous and steam humidity is critical for accurate measurements

## Relevance to Edge Cases
This paper is highly relevant to the edge case of fog → measurement_artifact_pm25:
1. Clearly explains the mechanism of fog-induced measurement artifacts
2. Distinguishes between gaseous humidity (no artifact) and steam/fog (artifact)
3. Provides quantitative evidence for the artifact

## Relationships to Extract
1. **fog → measurement_artifact_pm25** (DIRECT_CAUSE)
   - Mechanism: Fog droplets (liquid aerosols) are detected as particles by light-scattering sensors
   - Conditions: Steam humidity, fog episodes
   - Confidence: HIGH
