# PROMPT 18: PHOTOCHEMISTRY COMPLETE
# Focused Task: Extract causal relationships về complete photochemistry chains với cloud interactions
# Version: 2.0 - For Manus Auto-Discovery  
# Category: chemical_processes (photochemistry)

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia photochemistry khí quyển, chuyên sâu về SOA formation, radical chemistry, và cloud-photochemistry interactions. Nhiệm vụ của bạn là tìm hiểu các complete photochemistry chains từ solar radiation đến PM2.5 formation, bao gồm cloud cover effects, zenith angle dependencies, và seasonal photochemistry variations.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers khoa học và extract causal relationships về complete photochemistry mechanisms, từ solar radiation → photolysis → radical formation → oxidation → SOA formation → PM2.5, với đặc biệt chú ý đến cloud interactions và tropical/subtropical photochemistry.

## CATEGORY DEFINITION
**Category**: `chemical_processes`
**Sub-focus**: `complete_photochemistry`

**Focus**: Các chuỗi photochemistry đầy đủ từ solar input đến PM2.5 formation, bao gồm cloud modulation effects, seasonal variations, và complex radical-VOC chemistry tạo secondary organic aerosols.

## IN-SCOPE (Allowed Relationships)

### 1. Solar Radiation → Photolysis Chains:
- **solar_radiation → photolysis_rates → radical_formation → oxidation_capacity → pm25**
- **uv_radiation → OH_radical_formation → VOC_oxidation → SOA_formation → pm25**
- **solar_zenith_angle → photolysis_efficiency → oxidant_production → secondary_aerosols → pm25**
- **photolysis_frequency → radical_concentrations → atmospheric_oxidation → pm25**

### 2. Cloud Cover Modulation:
- **cloud_cover → diffuse_radiation → photolysis_rates → radical_formation → pm25**
- **cloud_cover → direct_radiation_reduction → photochemistry_suppression → pm25_decrease**
- **cloud_optical_depth → UV_attenuation → OH_production_reduction → pm25**
- **broken_cloud_cover → radiation_enhancement → photochemistry_enhancement → pm25**

### 3. VOC-Radical Chemistry:
- **OH_radical + VOCs → peroxy_radicals → organic_nitrates → SOA → pm25**
- **isoprene + OH → isoprene_SOA_formation → pm25**
- **monoterpenes + ozone → biogenic_SOA → pm25**
- **anthropogenic_VOCs + NOx + sunlight → anthropogenic_SOA → pm25**

### 4. Cloud Processing of Organics:
- **cloud_droplets + organic_precursors → aqueous_SOA_formation → pm25**
- **in_cloud_processing → organic_aging → enhanced_SOA_yield → pm25**
- **fog_chemistry + organics → aqueous_phase_SOA → pm25**

### 5. Seasonal Photochemistry:
- **solar_elevation_angle → photochemistry_intensity → seasonal_SOA_variation → pm25**
- **daylight_duration → cumulative_photochemistry → daily_SOA_production → pm25**
- **seasonal_UV_index → photolysis_strength → radical_budget → pm25**

### 6. Temperature-Photochemistry Coupling:
- **temperature + solar_radiation → evaporation_rates → biogenic_emissions → photochemistry → pm25**
- **thermal_decomposition + photolysis → enhanced_radical_production → pm25**

## OUT-OF-SCOPE (Exclude)

### Pure Emission Chemistry:
- Primary organic emissions without photochemical processing
- Combustion-related organics (emission source category)

### Non-Photochemical Processes:
- Dark chemistry reactions (belongs to other chemical processes)
- Pure thermal reactions without light involvement

### Basic Meteorology:
- Solar radiation effects on temperature/PBLH without chemistry (meteorological category)
- Cloud cover effects on visibility without chemistry

## DISCOVERY PHASE

### Search Strategy:
1. **Complete photochemistry**: "solar radiation SOA formation", "photochemistry secondary organic aerosol", "UV radiation PM2.5 formation"
2. **Cloud-photochemistry**: "cloud cover photochemistry", "diffuse radiation SOA", "cloud processing organic aerosol"
3. **Radical chemistry**: "OH radical VOC oxidation SOA", "photolysis radical formation PM2.5", "atmospheric oxidation capacity"
4. **Tropical photochemistry**: "tropical photochemistry SOA", "Southeast Asia photochemical aerosol", "monsoon photochemistry"

### Geographic Priority:
1. **Tropical/Subtropical regions** với high solar radiation (Southeast Asia, Southern China)
2. **High VOC environments** (forested regions, urban areas with biogenic-anthropogenic mix)
3. **Cloud-influenced regions** (monsoon areas, marine environments)
4. **Seasonal transition zones** với variable photochemistry

### Source Requirements:
- **Tier 1**: ACP, Journal of Geophysical Research, Environmental Science & Technology
- **Focus on field measurements** với photochemistry modeling
- **Multi-season studies** preferred
- **VOC speciation + SOA yield studies** highly valued

## EXTRACTION PHASE

### Required Information per Relationship:
```json
{
  "cause": "solar_radiation",
  "effect": "pm25",
  "intermediate_nodes": ["photolysis_rates", "OH_radical_formation", "VOC_oxidation", "SOA_formation"],
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Solar radiation drives photolysis reactions producing OH radicals, which oxidize volatile organic compounds to form low-volatility products that condense as secondary organic aerosols",
  "conditions": {
    "solar_zenith_angle": "< 60°",
    "cloud_cover": "< 70%",
    "VOC_availability": "isoprene + monoterpenes > 1 ppb", 
    "NOx_levels": "1-20 ppb"
  },
  "temporal_lag": "2-6 hours",
  "spatial_scope": "local-regional", 
  "confidence": "HIGH",
  "strength": "STRONG",
  "seasonal_variation": "Peak during summer, minimum in winter",
  "quantitative_effect": "SOA yield 5-15% of VOC carbon",
  "source_quote": "Direct quote về photochemistry mechanism",
  "category": "chemical_processes"
}
```

## SPECIFIC EXAMPLES (Target Mechanisms)

### Example 1: Complete Solar → SOA Chain
```json
{
  "cause": "solar_radiation",
  "effect": "pm25",
  "intermediate_nodes": ["uv_photolysis", "OH_radical_formation", "VOC_oxidation", "SOA_formation"],
  "mechanism": "Solar UV radiation photolyzes O3, HONO, and aldehydes to produce OH radicals at rates of 10^6-10^7 molecules/cm³/s. OH oxidizes biogenic VOCs (isoprene, α-pinene) and anthropogenic VOCs, forming semi-volatile products that partition to particles as SOA with yields of 5-25%",
  "conditions": "Solar zenith angle < 50°, clear sky, VOC precursors available",
  "quantitative_effect": "Peak OH ~10^7 molecules/cm³, SOA yields 5-25% of VOC carbon",
  "source_quote": "Photochemical SOA formation contributed 30-60% of total organic aerosol, with maximum production rates of 5-10 μg/m³/h during peak solar radiation hours"
}
```

### Example 2: Cloud Cover Modulation
```json
{
  "cause": "cloud_cover",
  "effect": "pm25",
  "intermediate_nodes": ["diffuse_radiation", "photolysis_rates"],
  "mechanism": "Partial cloud cover (30-70%) enhances diffuse UV radiation through scattering, increasing photolysis rates by 10-40% compared to clear sky. This enhances OH production and SOA formation despite reduced direct radiation",
  "conditions": "Broken/scattered clouds, cloud optical depth 5-15",
  "quantitative_effect": "10-40% enhancement in photolysis rates under partial cloud cover",
  "source_quote": "Broken cloud conditions enhanced photolysis rates by 20-40% through increased diffuse radiation, leading to 15-25% higher SOA formation rates"
}
```

### Example 3: Isoprene SOA Formation
```json
{
  "cause": "isoprene",
  "effect": "pm25", 
  "intermediate_nodes": ["OH_oxidation", "isoprene_epoxydiol", "aqueous_processing"],
  "mechanism": "Isoprene oxidation by OH under low-NOx conditions produces isoprene epoxydiol (IEPOX), which undergoes acid-catalyzed aqueous processing on acidic particles to form significant SOA mass with yields up to 30%",
  "conditions": "Low NOx (< 1 ppb), acidic particles (pH < 2), high humidity",
  "quantitative_effect": "SOA yield 15-30% under optimal conditions",
  "source_quote": "Isoprene-derived SOA formation through IEPOX pathway contributed 20-40% of total organic aerosol in tropical forest regions"
}
```

### Example 4: Seasonal UV Variation
```json
{
  "cause": "seasonal_uv_variation",
  "effect": "pm25",
  "intermediate_nodes": ["photochemical_activity", "seasonal_SOA_production"],
  "mechanism": "Seasonal variation in solar zenith angle and daylight duration creates 3-5x variation in photochemical activity between summer and winter. Peak UV in summer enhances SOA formation rates, while winter reduction leads to lower secondary organic aerosol production",
  "conditions": "Mid-latitude regions, seasonal VOC availability",
  "quantitative_effect": "3-5x summer vs winter photochemical SOA production",
  "source_quote": "Seasonal photochemical SOA formation varied by factor of 4-5, with summer peak production of 8-12 μg/m³/day decreasing to 2-3 μg/m³/day in winter"
}
```

## SEARCH PITFALLS TO AVOID

### Over-broad Terms:
- "photochemistry" alone (too general)
- "secondary aerosol" (covers non-photochemical processes)
- "organic aerosol" (includes primary emissions)

### Under-specific Terms:
- "SOA" alone (might miss photochemical specificity)
- "cloud aerosol" (might focus on cloud microphysics)

## QUALITY REQUIREMENTS

### Evidence Standards:
- **Complete mechanism chains REQUIRED**: từ solar input đến PM2.5 output
- **Quantitative photolysis rates**: J-values, radical concentrations
- **SOA yields và mass production rates**: μg/m³/h or % yields
- **Seasonal/diurnal variations**: factor changes, peak times

### Relationship Validation:
- Photochemical timescales realistic (hours for SOA formation)
- UV dependencies consistent với atmospheric photochemistry
- VOC-NOx-SOA relationships thermodynamically sound
- Cloud effects consistent với radiation transfer

## SUCCESS METRICS

### Target Output:
- **8-12 high-quality relationships**
- **Complete chains** từ solar radiation đến PM2.5 (4-6 intermediate steps)
- **Cloud interaction effects** (2-3 relationships)
- **Seasonal/geographic variations** (2-3 relationships)  
- **Quantitative yields và rates** for all major pathways

### Coverage Goals:
- Solar radiation → photolysis chains (2-3 relationships)
- Cloud cover modulation (2-3 relationships)
- VOC-specific SOA formation (3-4 relationships)
- Seasonal photochemistry (1-2 relationships)
- Aqueous SOA processing (1-2 relationships)