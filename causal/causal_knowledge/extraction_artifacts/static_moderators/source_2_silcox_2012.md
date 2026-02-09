# Source 2: Silcox et al. 2012 - Valley Topography and PM2.5

## Citation
- **Title**: Wintertime PM2.5 concentrations during persistent, multi-day cold-air pools in a mountain valley
- **Authors**: Geoffrey D. Silcox, Kerry E. Kelly, Erik T. Crosman, C. David Whiteman, Bruce L. Allen
- **Year**: 2012
- **Journal**: Atmospheric Environment, Volume 46, Pages 17-24
- **DOI**: https://doi.org/10.1016/j.atmosenv.2011.10.041
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Citations**: 139

## Key Findings for Static Factors

### Valley/Basin Topography - Cold Air Pool Mechanism
**Quote 1**: "PM2.5 concentrations were generally observed to decrease with increasing elevation and were linearly related to the pre-sunrise valley heat deficit, an instantaneous measure of atmospheric stability. Decreases of up to 30 percent were observed as elevation increased from 1300 to 1600 m."
- Source: Abstract

**Quote 2**: "Concentrations of PM2.5 can reach 100 μg m−3, exceeding the 24-h average National Ambient Air Quality Standard (NAAQS) of 35 μg m−3"
- Source: Introduction

**Quote 3**: "Under a high-pressure weather system, the subsiding warm air traps cold air in the Wasatch Front's mountain valleys. The pool of cold air is reinforced by radiational cooling during clear nights and by snow-cover and cloudiness that reduce daytime warming of the ground by reflecting much of the incoming solar radiation back to space."
- Source: Introduction

**Quote 4**: "Because vertical mixing of pollutants is suppressed in the stable atmospheric layers, PM2.5 aerosols emitted into the CAP or produced there through chemical and photochemical processes lead to high levels of PM2.5."
- Source: Introduction

**Quote 5**: "During the CAP episode of 23–30 January, concentrations of PM2.5 increased roughly linearly with time at all elevations at the rate of about 6 μg (m3 day)−1."
- Source: Abstract

### Temporal Patterns
- PM2.5 concentrations increase with valley heat deficit (CAP strength)
- Valley heat deficit and PM2.5 increase with time during multi-day CAPs
- Higher concentrations found in longest lasting CAPs

### Mechanism Explanation
1. High-pressure weather system causes subsiding warm air
2. Warm air traps cold air in mountain valleys (cold-air pool)
3. Cold air pool reinforced by:
   - Radiational cooling during clear nights
   - Snow-cover reflecting solar radiation
   - Cloudiness reducing daytime ground warming
4. Vertical mixing suppressed in stable atmospheric layers
5. PM2.5 accumulates due to suppressed dispersion

## Relevant for Relationships
1. **dem_topography_valley_basin → pm25** (MODERATOR)
   - Mechanism: Valley/basin topography creates conditions for cold-air pool formation, which traps pollutants by suppressing vertical mixing
   - PM2.5 decreases ~30% with elevation increase from 1300m to 1600m within valley
   - Accumulation rate: ~6 μg/m³/day during CAP events
   - Strength: STRONG
   - Confidence: HIGH
   - Seasonal: winter
   - Conditions: High-pressure weather, clear nights, snow cover

2. **topographic_trapping → reduced_dispersion → pm25** (MEDIATOR chain)
   - Valley topography → cold-air pool → suppressed vertical mixing → PM2.5 accumulation
   - Temporal lag: 1-3 days (multi-day events)
