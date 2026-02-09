# PROMPT 17: AEROSOL CHEMISTRY ADVANCED
# Focused Task: Extract causal relationships với intermediate chemistry nodes và complex mechanisms
# Version: 2.0 - For Manus Auto-Discovery
# Category: chemical_processes (advanced)

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia hóa học khí quyển, chuyên sâu về aerosol chemistry và secondary aerosol formation. Nhiệm vụ của bạn là tìm hiểu các intermediate chemistry nodes và complex mechanisms chưa được cover đầy đủ trong CKG hiện tại, đặc biệt tập trung vào aerosol pH, partitioning effects, và aqueous-phase chemistry.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers khoa học và extract causal relationships về advanced aerosol chemistry mechanisms, bao gồm các intermediate nodes như aerosol_pH, NH4NO3_partitioning, aerosol_liquid_water, và các complex multi-step chemistry chains.

## CATEGORY DEFINITION
**Category**: `chemical_processes`
**Sub-focus**: `advanced_mechanisms`

**Focus**: Các cơ chế hóa học phức tạp với intermediate steps, partitioning effects, pH-dependent reactions, và aqueous-phase processes tạo secondary PM2.5.

## IN-SCOPE (Allowed Relationships)

### 1. Aerosol pH Mechanisms:
- **NH3 + humidity + temperature → aerosol_pH → sulfate_formation_rate → pm25**
- **aerosol_pH + SO2 → sulfate_formation_efficiency → pm25**
- **aerosol_pH + transition_metals → catalytic_reactions → secondary_aerosols → pm25**
- **aerosol_composition → aerosol_pH → chemical_reaction_rates → pm25**

### 2. Gas-Particle Partitioning:
- **temperature + RH → NH4NO3_partitioning → gas_particle_equilibrium → pm25**
- **temperature_decrease → NH4NO3_partitioning_to_particle → pm25_increase**
- **humidity → organic_partitioning → SOA_formation → pm25**
- **aerosol_liquid_water → enhanced_partitioning → pm25**

### 3. Aerosol Liquid Water (ALW) Chemistry:
- **aerosol_liquid_water + precursors → aqueous_phase_reactions → sia_formation → pm25**
- **hygroscopic_growth → ALW_increase → chemical_reaction_enhancement → pm25**
- **ionic_strength + ALW → reaction_rate_modification → secondary_aerosol_yield → pm25**

### 4. Catalytic and Surface Reactions:
- **mineral_dust + SO2 → surface_catalysis → sulfate_formation → pm25**
- **transition_metals + H2O2 → fenton_reactions → oxidant_formation → secondary_aerosols → pm25**
- **sea_salt + HNO3 → chloride_depletion → sodium_nitrate_formation → pm25**

### 5. Multi-phase Chemistry:
- **gas_phase_precursors + particle_surface → heterogeneous_reactions → pm25**
- **cloud_droplet_chemistry → aqueous_processing → secondary_aerosol_formation → pm25**
- **interface_reactions + organic_films → SOA_enhancement → pm25**

### 6. Temperature-Dependent Chemistry:
- **temperature + chemical_kinetics → reaction_rate_changes → secondary_aerosol_yield → pm25**
- **cold_temperature → enhanced_condensation → semi_volatile_partitioning → pm25**
- **temperature_cycling → evaporation_condensation → aging_processes → pm25**

## OUT-OF-SCOPE (Exclude)

### Simple Direct Chemistry:
- Direct SO2 → sulfate (already covered in basic prompts)
- Direct NOx → nitrate (already covered)
- Basic VOC → SOA without intermediate steps

### Emission Processes:
- Primary emission chemistry (belongs to emission sources)
- Combustion chemistry (belongs to emission sources)

### Pure Meteorology:
- Weather effects without chemistry intermediate steps
- Transport without chemical transformation

## DISCOVERY PHASE

### Search Strategy:
1. **Advanced chemistry terms**: "aerosol pH PM2.5", "gas particle partitioning", "aqueous phase reactions aerosol"
2. **Intermediate processes**: "aerosol liquid water chemistry", "NH4NO3 partitioning temperature", "hygroscopic growth reactions"
3. **Catalytic mechanisms**: "mineral dust catalysis sulfate", "transition metals aerosol chemistry", "surface reactions PM2.5"
4. **Multi-phase chemistry**: "heterogeneous reactions", "interface chemistry aerosol", "cloud processing PM2.5"

### Geographic Priority:
1. **East/Southeast Asia** (China, Korea, Japan, Vietnam, Thailand) - industrial + natural conditions
2. **Polluted urban areas** với complex chemistry (Beijing, Seoul, Bangkok, Ho Chi Minh)
3. **Marine-influenced regions** với sea salt chemistry
4. **Dust-influenced regions** với mineral dust catalysis

### Source Requirements:
- **Tier 1**: ACP, Environmental Science & Technology, Atmospheric Environment, JPCA
- **Focus on mechanistic studies** với detailed chemistry analysis
- **Laboratory + field studies** preferred over pure modeling
- **Quantitative pH, partitioning data** highly valued

## EXTRACTION PHASE

### Required Information per Relationship:
```json
{
  "cause": "aerosol_pH",
  "effect": "pm25",
  "intermediate_nodes": ["sulfate_formation_rate"],
  "relationship_type": "MODERATOR",
  "mechanism": "Lower aerosol pH (more acidic conditions) enhances sulfate formation rates through increased SO2 uptake and faster aqueous-phase oxidation kinetics",
  "conditions": {
    "pH_range": "0-3",
    "relative_humidity": "> 60%",
    "temperature": "10-30°C",
    "SO2_concentration": "> 10 ppb"
  },
  "temporal_lag": "minutes-hours", 
  "spatial_scope": "local",
  "confidence": "HIGH|MEDIUM",
  "strength": "STRONG|MODERATE",
  "quantitative_effect": "2-5x rate enhancement at pH 1-2 vs pH 4-5",
  "source_quote": "Direct quote về pH-dependent chemistry mechanism",
  "category": "chemical_processes"
}
```

## SPECIFIC EXAMPLES (Target Mechanisms)

### Example 1: Aerosol pH Control
```json
{
  "cause": "aerosol_pH",
  "effect": "sulfate_formation",
  "mechanism": "Lower aerosol pH significantly enhances SO2 uptake and aqueous-phase oxidation rates. pH decrease from 4 to 1 increases sulfate formation rates by 3-5x through enhanced Henry's law solubility and faster oxidation kinetics",
  "conditions": "RH > 70%, SO2 > 10 ppb, presence of oxidants",
  "quantitative_effect": "5x rate increase at pH 1 vs pH 4",
  "source_quote": "Aerosol pH was identified as the key factor controlling sulfate production rates, with a 5-fold increase observed when pH decreased from 4 to 1"
}
```

### Example 2: NH4NO3 Partitioning
```json
{
  "cause": "temperature_decrease",
  "effect": "pm25",
  "intermediate_nodes": ["NH4NO3_partitioning"],
  "mechanism": "Temperature decrease shifts NH4NO3 equilibrium toward particle phase. Each 10°C temperature drop approximately doubles particulate NH4NO3 fraction, significantly increasing PM2.5 mass",
  "conditions": "Temperature < 25°C, sufficient NH3 and HNO3 precursors",
  "quantitative_effect": "2x particle fraction per 10°C decrease",
  "source_quote": "Temperature decrease from 25°C to 5°C increased particulate NH4NO3 fraction from 30% to 85%, contributing 20-30 μg/m³ to PM2.5"
}
```

### Example 3: ALW Enhanced Chemistry
```json
{
  "cause": "aerosol_liquid_water",
  "effect": "pm25",
  "intermediate_nodes": ["aqueous_phase_reactions"],
  "mechanism": "Aerosol liquid water provides reaction medium for enhanced aqueous-phase chemistry. ALW > 10 μg/m³ air significantly accelerates sulfate formation through S(IV) oxidation by H2O2 and O3",
  "conditions": "RH > 80%, hygroscopic particles present, oxidants available",
  "quantitative_effect": "3-4x sulfate formation rate at ALW > 20 μg/m³",
  "source_quote": "Aerosol liquid water content above 10 μg/m³ enhanced sulfate formation rates by 3-4x compared to dry conditions"
}
```

### Example 4: Mineral Dust Catalysis
```json
{
  "cause": "mineral_dust",
  "effect": "pm25",
  "intermediate_nodes": ["surface_catalysis", "sulfate_formation"],
  "mechanism": "Mineral dust provides catalytic surfaces for SO2 oxidation. Iron and manganese oxides on dust particles catalyze SO2 to sulfate conversion, especially under humid conditions",
  "conditions": "Dust events, RH > 50%, SO2 > 5 ppb",
  "quantitative_effect": "2-3x sulfate formation rate during dust events",
  "source_quote": "Mineral dust enhanced sulfate formation rates by 2-3x through surface catalysis, contributing 15-25% additional PM2.5 during dust episodes"
}
```

## SEARCH PITFALLS TO AVOID

### Too General:
- "aerosol chemistry" (too broad)
- "secondary aerosol formation" (covered elsewhere)
- "PM2.5 chemistry" (too general)

### Too Specific: 
- Single reaction pathways without PM2.5 relevance
- Pure laboratory studies without atmospheric relevance
- Model-only studies without measurement validation

## QUALITY REQUIREMENTS

### Evidence Standards:
- **Quantitative relationships REQUIRED**: rate constants, pH effects, partitioning coefficients
- **Mechanistic understanding**: not just correlations
- **Intermediate steps clearly identified**: don't skip chemical nodes
- **Atmospheric relevance**: realistic concentrations and conditions

### Relationship Validation:
- Chemistry must be thermodynamically and kinetically reasonable
- Conditions must be atmospherically relevant
- Quantitative effects should have error estimates
- Temporal scales should be realistic (minutes to hours for chemistry)

## SUCCESS METRICS

### Target Output:
- **10-15 high-quality relationships**
- **At least 6 intermediate chemistry nodes** (aerosol_pH, NH4NO3_partitioning, ALW, etc.)
- **Focus on multi-step mechanisms** (3-5 step chains)
- **Quantitative rate enhancements** and threshold effects
- **pH, temperature, humidity dependencies** well characterized

### Coverage Goals:
- Aerosol pH mechanisms (3-4 relationships)
- Gas-particle partitioning (2-3 relationships) 
- ALW chemistry (2-3 relationships)
- Catalytic processes (2-3 relationships)
- Multi-phase chemistry (2-3 relationships)