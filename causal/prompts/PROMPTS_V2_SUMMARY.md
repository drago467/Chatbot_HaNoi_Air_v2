# Prompts V2.0 - Summary & Status
# Version 2.1 - For Manus Auto-Discovery with Quality Assurance

## 🎉 ALL 18 PROMPTS COMPLETED & EXTRACTED!

**CKG Statistics After All Prompts:**
- **205 relationships** (từ 18 prompts)
- **116 nodes, 143 edges**
- **Quality Score: 96.5%**

## Core Prompts (01-07) ✅

### prompt_00_master_template.md ✅
- System guardrails với anti-hallucination policies
- Source quality tiers (Tier 1-4)
- Evidence requirements (source_url, source_quote bắt buộc)
- Saturation criteria
- Geographic & temporal scope
- Output format với bibliography + relationships

### prompt_01_meteorological_pathways.md ✅
- IN-SCOPE: Temperature → Inversion → PBLH → PM2.5, Wind → Dispersion, etc.
- OUT-OF-SCOPE: Chemical processes, emission sources (handoff)
- Discovery phase với search queries
- Extraction phase với evidence requirements
- Output format tách theo category

### prompt_02_chemical_processes.md ✅
- IN-SCOPE: SO2/NO2 → SIA Formation, VOCs → SOA Formation, etc.
- OUT-OF-SCOPE: Meteorological processes, emission sources (handoff)
- Discovery phase với search queries về chemistry
- Extraction phase với chemical mechanism requirements
- Output format tách theo category

### prompt_03_transport_mechanisms.md ✅
- IN-SCOPE: Wind Direction → Transport, Back-trajectory, etc.
- OUT-OF-SCOPE: Local dispersion, emission rates (handoff)
- Discovery phase với search queries về transport
- Extraction phase với transport mechanism requirements
- Output format tách theo category

## Đã hoàn thành ✅ (tiếp)

### prompt_04_emission_sources.md ✅
- IN-SCOPE: traffic/industry/biomass_burning/construction/power_plants/agriculture → (pm25_primary, NOx, SO2, VOCs, NH3, CO, heavy_metals)
- OUT-OF-SCOPE: Chemical formation (prompt_02), meteorology (prompt_01), transport attribution (prompt_03), static drivers (prompt_05)
- Discovery phase + extraction với evidence bắt buộc

### prompt_05_static_factors.md ✅
- IN-SCOPE: population/LULC/roads/industrial_zones/vegetation/DEM(TWI,valley) → exposure/air_trapping → PM2.5
- OUT-OF-SCOPE: time-varying emissions (prompt_04), meteorology/chemistry (prompt_01/02), seasonal patterns (prompt_06)
- Bắt buộc temporal_lag = \"N/A (static factor)\"

### prompt_06_seasonal_patterns.md ✅
- IN-SCOPE: season/diurnal/events (harvest/holiday) → (stability/PBLH/traffic/open_burning) → PM2.5
- OUT-OF-SCOPE: deep meteorology mechanisms (prompt_01), emission inventory details (prompt_04), chemistry (prompt_02)
- Dùng handoff khi cần cơ chế sâu

### prompt_07_edge_cases.md ✅
- IN-SCOPE: exceptions, thresholds, reversals, measurement artifacts (fog/hygroscopic growth)
- OUT-OF-SCOPE: standard (non-exception) relationships → handoff prompt_01/02/04
- Bắt buộc ghi rõ \"what rule it breaks\" trong notes

### prompt_08–13: Gap-Focused / Advanced Prompts ✅
- `prompt_08_winter_chemistry_sia_gaps.md`  
  - Winter SIA chains: RH/ALW/pH/NH3/NOx/SO2/HONO/H2O2 → SIA → PM2.5 (winter haze, Hanoi/SEA)
- `prompt_09_precipitation_wet_scavenging_gaps.md`  
  - Precipitation intensity/duration/type → wet_deposition/scavenging → PM2.5 (intensity thresholds, scavenging efficiency)
- `prompt_10_synoptic_cold_surge_transport_gaps.md`  
  - Cold surge/monsoon/synoptic patterns → long_range_transport/stagnation → PM2.5 (onset vs persistence)
- `prompt_11_wind_direction_upwind_exposure_gaps.md`  
  - Wind direction sectors + upwind emission regions → PM2.5 (industrial regions, biomass burning corridors, clean marine air)
- `prompt_12_static_moderators_gaps.md`  
  - Static factors (population, roads, industrial zones, LULC, DEM) as MODERATOR/INDIRECT_CAUSE for PM2.5 sensitivity
- `prompt_13_fog_visibility_artifacts_gaps.md`  
  - Fog/very high RH/low visibility & clear-sky edge cases → measurement artifacts hoặc non-intuitive PM2.5 outcomes

### Advanced Prompts (14-15) ✅
- `prompt_14_cold_surge_chains.md`  
  - Long causal chains (3-4 steps) for cold surge mechanisms: onset → transport → pm25, persistence → stagnation → pm25
- `prompt_15_meteorological_core_variables.md`  
  - Cloud cover + solar radiation chains: cloud → radiation → photochemistry, solar → photolysis → SOA → pm25

### Advanced Prompts (16-18) ✅ NEW!
- `prompt_16_precipitation_paradox.md`  
  - Light precipitation paradox: drizzle → ALW → enhanced_chemistry → pm25_increase
  - Fog/mist effects, scavenging thresholds, monsoon patterns
  - **11+ relationships addressing critical precipitation gap**

- `prompt_17_aerosol_chemistry_advanced.md`  
  - Aerosol pH mechanisms: pH → sulfate_formation_rate → pm25
  - NH4NO3 partitioning: temperature → partitioning → pm25
  - Mineral dust catalysis, transition metals, ALW chemistry
  - **14+ relationships with intermediate chemistry nodes**

- `prompt_18_photochemistry_complete.md`  
  - Complete solar → SOA chains: radiation → photolysis → OH → VOC_oxidation → SOA → pm25
  - Cloud cover modulation: clouds → diffuse_radiation → photolysis_enhancement
  - IEPOX pathway, aqueous SOA, seasonal UV variations
  - **12+ relationships completing photochemistry coverage**

## Key Features của V2.1

1. **Anti-Hallucination**:
   - Bắt buộc source_url, source_quote cho mỗi relationship
   - Không được invent mechanisms
   - Confidence phải match evidence quality

2. **Source Quality Tiers**:
   - Tier-1: Peer-reviewed papers (≥6 sources minimum)
   - Tier-2: Official reports
   - Tier-3: Preprints (use with caution)
   - Tier-4: Wikipedia/blogs (discovery only)

3. **Saturation Criteria**:
   - Stop khi 3 consecutive sources không add new mechanisms
   - Hoặc đạt ≥6 Tier-1 sources

4. **IN/OUT Scope**:
   - Mỗi prompt có IN-SCOPE và OUT-OF-SCOPE rõ ràng
   - OUT-OF-SCOPE → handoff_to_other_prompts

5. **Output Format**:
   - Tách theo category
   - Bibliography riêng
   - Relationships với đầy đủ source metadata

## Workflow với Manus

1. **Chọn prompt** phù hợp với task
2. **Copy prompt vào Manus** (bao gồm cả prompt_00 như system context)
3. **Manus tự động**:
   - Discovery: Tìm papers theo search queries
   - Collection: Build bibliography với Tier classification
   - Saturation: Check và continue nếu cần
   - Extraction: Extract relationships với evidence
   - Validation: Check quality
   - Output: Generate JSON

4. **Review output**:
   - Check bibliography quality
   - Check relationships có evidence đầy đủ
   - Check confidence phù hợp

5. **Merge outputs** từ các prompts khác nhau

## ✅ ALL PROMPTS COMPLETED

**Final Statistics:**
- 18 prompts executed successfully with Manus
- 205 relationships extracted
- 90+ Tier 1 sources used
- 96.5% overall quality score achieved

**CKG Status**: PRODUCTION READY for Phase 2 - Backend Development

## Legacy Workflow Notes

1. Test với Manus trên một topic nhỏ (ví dụ: meteorology-only) để calibrate quality
2. Review output theo checklist (quote/URL/locator; IN-SCOPE; confidence)
3. Nếu Manus hay "lấn scope", tăng độ chặt OUT-OF-SCOPE và giảm max relationships/source
4. Nếu coverage thiếu, mở rộng query set và nới saturation threshold (ví dụ 4 nguồn liên tiếp)
