# Source 5: Han et al. 2020 - Industrial Land Use and PM2.5

## Citation
- **Title**: Spatial distribution characteristics of PM2.5 and PM10 in Xi'an City predicted by land use regression models
- **Authors**: Li Han, Jingyuan Zhao, Yuejing Gao, Zhaolin Gu, Kai Xin, Jianxin Zhang
- **Year**: 2020
- **Journal**: Sustainable Cities and Society, Volume 61, Article 102329
- **DOI**: https://doi.org/10.1016/j.scs.2020.102329
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Citations**: 121

## Key Findings for Static Factors

### Industrial Land Use - PM2.5 Relationship
**Quote 1**: "Spatial distribution of PM2.5 and PM10 related to industrial land use."
- Source: Highlights

**Quote 2**: "The spatial distribution of pollutants is closely related to the layout of industrial land and the location of enterprises that generate air pollution emissions."
- Source: Abstract

**Quote 3**: "Outside the Qinling and Li Mountains, the concentrations of PM2.5 and PM10 were closely related to the layout of industrial land use and the locations of air-polluting enterprises."
- Source: Results section (from page content)

**Quote 4**: "A large amount of industrial land existed in the HIDZ southwest of the main urban district... leading to significantly higher concentrations of PM2.5 and PM10 in these areas compared with other areas."
- Source: Results section

### Vegetation/Green Space Effect
**Quote 5**: "Green space can mitigate pollution, and the contribution of traffic emission is less than that of industrial emission."
- Source: Abstract

**Quote 6**: "The concentrations of PM2.5 and PM10 in the Qinling Mountains south of Xi'an and Li Mountains east of Xi'an were significantly lower than those in other areas, which was attributed to the fact that the reduction of pollutant emission sources and increase in vegetation have a mitigating effect on the concentrations of PM2.5 and PM10."
- Source: Results section

### Model Performance
- PM2.5 model: R² = 0.713, RMSE = 8.355 μg/m³
- PM10 model: R² = 0.681, RMSE = 14.842 μg/m³
- Variables included: area of green space, road length, numbers of pollutant discharging enterprises, restaurants, bus stations

### Supporting Evidence from Other Studies Cited
- "Huang et al. (2015) confirmed that the accumulation of PM2.5 in Xi'an was closely related to industrial production"
- "Wang et al. (2014) reported that as high as 58% of the concentrations of PM2.5 in Xi'an in the heavy pollution months were caused by industrial activities"
- "Song et al. (2015) revealed that transportation and industrial emissions were the main sources of PM2.5 in Xi'an"

## Relevant for Relationships
1. **industrial_zones_proximity → pm25** (INDIRECT_CAUSE)
   - Mechanism: Industrial land use and air-polluting enterprises emit PM2.5 directly, leading to higher concentrations in nearby areas
   - Areas with industrial zones have significantly higher PM2.5 concentrations
   - Strength: STRONG
   - Confidence: HIGH
   - Spatial scope: local

2. **lulc_vegetation → pm25** (INDIRECT_CAUSE - decrease)
   - Mechanism: Green space and vegetation mitigate PM2.5 pollution through deposition and reduced emission sources
   - Mountain areas with vegetation show significantly lower PM2.5
   - Strength: MODERATE
   - Confidence: HIGH
