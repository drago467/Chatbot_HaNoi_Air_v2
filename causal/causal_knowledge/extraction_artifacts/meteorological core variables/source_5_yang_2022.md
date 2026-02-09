# Source 5: Yang et al. 2022

## Bibliographic Information
- **Title**: Impacts of aerosol–photolysis interaction and aerosol–radiation feedback on surface-layer ozone in North China during multi-pollutant air pollution episodes
- **Authors**: Hao Yang, Lei Chen, Hong Liao, Jia Zhu, Wenjie Wang, and Xin Li
- **Year**: 2022
- **Journal**: Atmospheric Chemistry and Physics
- **Volume**: 22
- **Pages**: 4101-4116
- **DOI**: https://doi.org/10.5194/acp-22-4101-2022
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings

### Mechanism: Aerosol/Cloud → Reduced Solar Radiation → Reduced Photolysis → Reduced O3/SOA Formation

This paper quantifies the impacts of aerosol-photolysis interaction (API) and aerosol-radiation feedback (ARF) on surface-layer ozone, providing key insights into how reduced solar radiation affects photochemistry.

1. **Aerosols reduce solar radiation at surface**: "API and ARF reduced the daytime shortwave radiative fluxes at the surface by 92.4–102.9 W m−2"

2. **Reduced solar radiation → Reduced photolysis rates**: "Aerosols were simulated to reduce the daytime near-surface photolysis rates of J[NO2] and J[O1D] by 1.8 × 10−3–2.0 × 10−3 and 5.7 × 10−6–6.4 × 10−6 s−1, respectively"

3. **Reduced photolysis → Reduced O3 production**: "API was simulated to change daytime surface-layer O3 concentrations by −8.5 ppb to −11.4 ppb"

4. **Reduced solar radiation → Reduced PBLH**: "the stabilized atmosphere decreased the daytime planetary boundary layer height and 10 m wind speed by 129.0–249.0 m and 0.05–0.15 m s−1, respectively"

5. **Key process for API effect**: "the weakened O3 chemical production made the greatest contribution to API effect"

### Key Quotes
- "Aerosols can influence O3 by altering photolysis rates (defined as aerosol–photolysis interaction (API))"
- "aerosols reduced the net ozone production rate by 25% by reducing the photolysis frequencies"
- "the reduction in O3 by API is larger than that by ARF"
- "future PM2.5 reductions may lead to O3 increases due to the weakened aerosol–radiation interactions"

### Causal Chain Extracted (applicable to cloud cover effects)
1. `cloud_cover` / `aerosol` → `reduced_solar_radiation` (scattering and absorption)
2. `reduced_solar_radiation` → `reduced_photolysis_rates` (J[NO2], J[O1D])
3. `reduced_photolysis_rates` → `reduced_oh_radical_formation`
4. `reduced_oh_radical` → `reduced_voc_oxidation` → `reduced_soa_formation`
5. `reduced_soa_formation` → `reduced_pm25` (secondary component)

### Conditions
- **Time**: Daytime (photolysis requires solar radiation)
- **Season**: Summer (high solar radiation periods)
- **Location**: North China Plain

### Implications for Cloud Cover Effects
Since cloud cover also reduces solar radiation reaching the surface, the same mechanisms apply:
- High cloud cover → Reduced photolysis rates → Reduced photochemical O3 and SOA formation
- This represents a moderator effect of cloud cover on the solar radiation → photochemistry pathway

