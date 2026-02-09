# Source 6: Hien et al. 2020 - Urban Expansion and Air Pollution in Hanoi

## Citation
- **Title**: Impact of urban expansion on the air pollution landscape: A case study of Hanoi, Vietnam
- **Authors**: P.D. Hien, N.T. Men, P.M. Tan, M. Hangartner
- **Year**: 2020
- **Journal**: Science of The Total Environment, Volume 702, Article 134635
- **DOI**: https://doi.org/10.1016/j.scitotenv.2019.134635
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Citations**: 68

## Key Findings for Static Factors

### Urban Expansion - Air Pollution Relationship
**Quote 1**: "The rapid urban expansion of Hanoi over the last few decades has transformed a lot of agricultural land into urban land uses accompanying pollution by traffic, industrial, and residential emission sources."
- Source: Abstract

**Quote 2**: "The pollutant concentrations decrease from the city center outward, reflecting the history of urban expansion with the city fringe being urbanized in the 1980s and the peri-urban area having undergone development from the early 1990s."
- Source: Abstract

**Quote 3**: "As revealed by the land use regression models, the factors driving the spatial variations of pollutant concentrations across the city include the population density, the road density, and the distances of the monitoring site to the urban center and the nearest roadway."
- Source: Abstract

### Quantitative Data
- NO2 values: 5.5 to 70 µg m⁻³ (mean: 34.3 µg m⁻³)
- SO2 values: 1 to 51 µg m⁻³ (mean: 14.5 µg m⁻³)
- NO2/SO2 decrease from 70/51 µg m⁻³ in urban core to 5/1 µg m⁻³ in peri-urban area

### Driving Factors from LUR Models
1. **Population density** - positive correlation with pollution
2. **Road density** - positive correlation with pollution
3. **Distance to urban center** - negative correlation (pollution decreases with distance)
4. **Distance to nearest roadway** - negative correlation

### Traffic as Key Source
**Quote 4**: "Traffic is the most important source given the emissions from 5.2 million motorbikes and around 550,000 cars"
- Source: Discussion section

### Industrial Hot Spots
**Quote 5**: "Numerous traffic and industrial emission hot spots occur in the peri-urban area."
- Source: Highlights

### Study Context
- 176 monitoring sites across 14 districts of Hanoi
- Area covered: 921 km²
- Period: 2008 (prior to new urban expansion wave)
- Method: Passive diffusion samplers + Land Use Regression models

## Relevant for Relationships
1. **population_density → pm25** (INDIRECT_CAUSE)
   - Mechanism: Higher population density leads to more traffic, industrial, and residential emissions
   - Spatial gradient: pollution decreases from urban center outward
   - Strength: MODERATE to STRONG
   - Confidence: HIGH

2. **road_network_density → pm25** (INDIRECT_CAUSE)
   - Mechanism: Higher road density associated with more traffic emissions
   - Distance to roadway negatively correlated with pollution
   - Strength: MODERATE
   - Confidence: HIGH

3. **lulc_urban_expansion → pm25** (INDIRECT_CAUSE)
   - Mechanism: Conversion of agricultural land to urban uses brings traffic, industrial, and residential emission sources
   - Temporal pattern: pollution advances outward following urban expansion history
   - Strength: MODERATE
   - Confidence: HIGH
