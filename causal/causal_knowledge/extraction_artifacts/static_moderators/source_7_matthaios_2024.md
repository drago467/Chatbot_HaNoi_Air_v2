# Source 7: Matthaios et al. 2024 - Road Proximity and Traffic-Related PM2.5

## Citation
- **Title**: The effects of urban green space and road proximity to indoor traffic-related PM2.5, NO2, and BC exposure in inner-city schools
- **Authors**: V. N. Matthaios, I. Holland, C. M. Kang, J. E. Hart, M. Hauptman, J. M. Wolfson, J. M. Gaffin, W. Phipatanakul, D. R. Gold, P. Koutrakis
- **Year**: 2024
- **Journal**: Journal of Exposure Science & Environmental Epidemiology, Volume 34, Pages 745-752
- **DOI**: https://doi.org/10.1038/s41370-024-00669-8
- **Tier**: Tier-1 (Peer-reviewed journal, Nature Publishing Group)
- **Citations**: 16

## Key Findings for Static Factors

### Road Proximity - Distance Decay of PM2.5
**Quote 1**: "It is evident that all traffic-related pollutants follow a linear decay with distance. The sharpest decrease with distance is for T-PM2.5 followed by NO2, while BC has a smoother decrease with distance."
- Source: Results section

**Quote 2**: "Schools that are more than 3 km away from roadways experience (on average) a 63%, 35%, and 22% decrease in T-PM2.5, NO2, and BC compared to those that are close to major roadways."
- Source: Results section

**Quote 3**: "The analysis showed linear decays of indoor traffic-related PM2.5, NO2, and BC by 60%, 35%, and 22%, respectively for schools located at a greater distance from major roads."
- Source: Abstract/Results

### Urban Green Space - PM2.5 Reduction
**Quote 4**: "The results further showed that surrounding school greenness at 270 m buffer was significantly associated (p < 0.05) with lower indoor traffic-related PM2.5: −0.068 (95% CI: −0.124, −0.013)"
- Source: Abstract

**Quote 5**: "These associations were stronger for surrounding greenness at a greater distance from the schools (buffer 1230 m) PM2.5: −0.101 (95% CI: −0.156, −0.046)"
- Source: Abstract

### Study Details
- 74 schools in Boston, USA
- Measured indoor PM2.5, NO2, and BC
- Used NDVI (Normalized Difference Vegetation Index) for greenness

### Mechanism
- Traffic-related PM2.5 decreases linearly with distance from roads
- Green space reduces traffic-related PM2.5 through:
  - Physical barrier effect
  - Deposition on vegetation surfaces
  - Dispersion enhancement

## Relevant for Relationships
1. **road_network_proximity → pm25** (INDIRECT_CAUSE)
   - Mechanism: Traffic emissions from roads are the direct source; PM2.5 concentrations decay linearly with distance from major roads
   - Quantification: 60-63% decrease in traffic-related PM2.5 at >3km from roadways
   - Relationship type: INDIRECT_CAUSE (mediated through traffic emissions)
   - Strength: STRONG
   - Confidence: HIGH
   - Spatial scope: local (within 3km of roads)

2. **lulc_vegetation → pm25** (INDIRECT_CAUSE - decrease)
   - Mechanism: Urban greenness reduces traffic-related PM2.5 through deposition and dispersion
   - Quantification: Significant negative association (coefficient -0.068 to -0.101)
   - Effect stronger at larger buffer distances (1230m > 270m)
   - Strength: MODERATE
   - Confidence: HIGH
