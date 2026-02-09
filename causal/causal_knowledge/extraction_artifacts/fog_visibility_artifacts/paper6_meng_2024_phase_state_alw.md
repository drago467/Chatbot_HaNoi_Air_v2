# Paper 6: Meng et al. 2024 - Particle Phase State and Aerosol Liquid Water

## Citation
- **Title**: Particle phase state and aerosol liquid water greatly impact secondary aerosol formation: insights into phase transition and its role in haze events
- **Authors**: Xiangxinyue Meng, Zhijun Wu, Jingchuan Chen, Yanting Qiu, Taomou Zong, Mijung Song, Jiyi Lee, and Min Hu
- **Year**: 2024
- **Journal**: Atmospheric Chemistry and Physics
- **DOI**: 10.5194/acp-24-2399-2024
- **URL**: https://acp.copernicus.org/articles/24/2399/2024/
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings

### 1. Particle Phase State
Particles predominantly exist in a semi-solid or solid state during clean winter days with ambient relative humidity (RH) below 30%. A non-liquid to liquid phase transition occurs when the ALW mass fraction exceeds 15% (dry mass) at transition RH thresholds of 40%-60%.

### 2. Accelerated SIA Formation During Haze
During haze episodes, the transformation rates of sulfate and nitrate aerosols rapidly increase through phase transition and increased ALW:
- Sulfate: 48% increase
- Nitrate: 11% increase
This results in noticeable increases in secondary inorganic aerosols (SIA).

### 3. Positive Feedback Loop
The presence of abundant ALW, favored by elevated RH and higher proportion of SIA, facilitates:
- Partitioning of water-soluble compounds from gas to particle phase
- Heterogeneous and aqueous processes in liquid particles
- Substantial increase in secondary organic aerosol (SOA) formation
- Elevated aerosol oxidation

### 4. Hygroscopicity Enhancement
The overall hygroscopicity parameters exhibit a substantial enhancement with a mean value of 23%.

### 5. Key Quotes
> "The particle phase state is crucial for reactive gas uptake, heterogeneous, and multiphase chemical reactions, thereby impacting secondary aerosol formation."

> "During haze episodes, the transformation rates of sulfate and nitrate aerosols rapidly increase through phase transition and increased ALW by 48% and 11%, respectively."

> "These results highlight phase transition as a key factor initiating the positive feedback loops between ALW and secondary aerosol formation during haze episodes over the North China Plain."

## Relevance to Edge Cases
This paper is highly relevant to the edge case of fog/high ALW → accelerated_aqueous_phase_reaction:
1. Explains the mechanism of phase transition enabling rapid SIA formation
2. Quantifies the increase in sulfate (48%) and nitrate (11%) formation rates
3. Shows the positive feedback loop between ALW and secondary aerosol formation

## Relationships to Extract
1. **aerosol_liquid_water → accelerated_aqueous_phase_reaction → sia_formation → pm25** (INDIRECT_CAUSE)
   - Mechanism: Phase transition from semi-solid to liquid enables heterogeneous and aqueous chemistry
   - Conditions: RH > 40-60%, ALW mass fraction > 15%
   - Confidence: HIGH
