# Source 2: Wu et al. 2022

## Bibliographic Information
- **Title**: Tracing the Formation of Secondary Aerosols Influenced by Solar Radiation and Relative Humidity in Suburban Environment
- **Authors**: Yangzhou Wu, Dantong Liu, Ping Tian, Jiujiang Sheng, Quan Liu, et al.
- **Year**: 2022
- **Journal**: Journal of Geophysical Research: Atmospheres
- **Volume**: 127, Issue 17
- **DOI**: 10.1029/2022JD036913
- **Tier**: Tier-1 (Peer-reviewed AGU journal)

## Key Findings

### Mechanism: Solar Radiation → Photochemistry → SOA Formation

1. **Solar radiation drives photochemical aging**:
   - "The pronounced decrease in T/B due to the increase in tage at approximately midday was due to enhanced solar radiation"
   - Photochemical age (tage) increased with solar radiation intensity

2. **Solar radiation → OOA (Oxygenated Organic Aerosol) formation**:
   - "all OOA/BC exhibited early afternoon peaks for all air masses corresponding to times of intense solar radiation"
   - "OOA3/BC for the C3 air mass exhibited a notable midday peak during the strongest solar radiation"
   - "These results demonstrate the important role of photooxidation in OOA3 formation"

3. **Different pathways under different conditions**:
   - High solar radiation + Low RH → Photochemical oxidation pathway
   - Low solar radiation + High RH → Aqueous-like reactions pathway
   - "chemical reactions occurring during C1 and C2-C3 should be different and should consist of more aqueous-like reactions (high RH and low shortwave radiation) and photochemical oxidation (low RH and high shortwave radiation)"

4. **Secondary PM production rate**:
   - "Secondary PM production was more rapid at tage > 6 hr, particularly for C3 with higher solar radiation"
   - "C3 exhibited the most rapid enhancement of the OA oxidation state compared to C1 and C2, and this was consistent with it receiving the highest amount of solar radiation"

### Key Quotes
- "The intensity of solar radiation and the air mass transport time can determine the photochemical age of pollutants"
- "OOA3 exhibited the highest O/C ratio (0.81)" - indicating highly oxidized secondary organic aerosol
- "important role of photooxidation in OOA3 formation in C3"

### Conditions
- **Time**: Daytime (06:00-18:00)
- **Season**: Summer
- **Location**: Suburban Beijing, China

### Causal Chain Extracted
1. `solar_radiation` → `photolysis` → `photochemical_aging`
2. `photochemical_aging` → `voc_oxidation` → `ooa_formation` (secondary organic aerosol)
3. `ooa_formation` → `pm25` (mass increase)

### Cloud Cover as Moderator
- "The longer tage for C1 may also be caused by reduced solar radiation, thus decreasing the reaction rate of the VOCs"
- Reduced solar radiation (from clouds/pollution) → Slower photochemical reactions

