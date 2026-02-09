# PROMPT 15: METEOROLOGICAL CORE VARIABLES (Cloud Cover & Photochemistry)
# Focused Task: Extract causal relationships for cloud_cover and solar_radiation photochemistry mechanisms
# Version: 2.0 - For Manus Auto-Discovery
# Category: meteorological_pathways

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia về **atmospheric physics và photochemistry** trong khí quyển, với kiến thức sâu về:
- Cloud cover effects on atmospheric stability và solar radiation
- Photochemical processes (photolysis, radical formation)
- Secondary organic aerosol (SOA) formation mechanisms
- Cloud-radiation interactions và boundary layer dynamics

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về **cloud cover** và **solar radiation photochemistry** ảnh hưởng đến PM2.5 tại Hà Nội và khu vực Đông Nam Á.

**Mục tiêu đặc biệt**: Bổ sung các relationships còn thiếu về:
1. Cloud cover → atmospheric stability → inversion → PM2.5
2. Solar radiation → photochemistry → SOA formation → PM2.5
3. Cloud cover → solar radiation → photochemistry (moderator effects)

## CATEGORY DEFINITION
**Category**: `meteorological_pathways`

**Focus**: Cloud cover effects on stability và solar radiation effects on photochemistry leading to PM2.5 changes.

## IN-SCOPE (Allowed Relationships)

### A) Cloud cover → Atmospheric stability chain
1. **cloud_cover → reduced_solar_radiation** (clouds block sunlight)
2. **reduced_solar_radiation → reduced_surface_heating** (less daytime warming)
3. **reduced_surface_heating → atmospheric_stability** (stable conditions)
4. **atmospheric_stability → inversion** (temperature inversion formation)
5. **inversion → pm25** (pollutant accumulation)

**Alternative chain**:
6. **cloud_cover → reduced_solar_radiation → pblh_decrease** (shallow boundary layer)
7. **pblh_decrease → pm25** (concentration increase)

### B) Solar radiation → Photochemistry chain
8. **solar_radiation → photolysis** (UV radiation breaks down molecules)
9. **photolysis → radical_formation** (OH, HO2, NO3 radicals)
10. **radical_formation → oxidation_reactions** (VOC oxidation, NOx oxidation)
11. **oxidation_reactions → soa_formation** (secondary organic aerosol)
12. **soa_formation → pm25** (mass increase)

**Alternative chain**:
13. **solar_radiation → photochemistry → o3_formation** (photochemical O3)
14. **o3_formation → oxidation_reactions → soa_formation → pm25**

### C) Cloud cover as moderator
15. **cloud_cover → reduced_solar_radiation** (moderator effect)
16. **reduced_solar_radiation → reduced_photochemistry** (less photolysis)
17. **reduced_photochemistry → reduced_soa_formation → pm25** (decrease)

**Combined effect**:
18. **high_cloud_cover → reduced_dispersion (via stability) + reduced_soa_formation (via photochemistry) → pm25** (complex effect)

### Allowed Intermediate Nodes (use standardized snake_case)
- `cloud_cover`, `reduced_solar_radiation`, `solar_radiation`
- `reduced_surface_heating`, `atmospheric_stability`, `inversion`
- `pblh_decrease`, `pblh`
- `photolysis`, `radical_formation`, `oh_radical`, `ho2_radical`, `no3_radical`
- `oxidation_reactions`, `voc_oxidation`, `nox_oxidation`
- `soa_formation`, `secondary_organic_aerosol`
- `o3_formation`, `photochemical_o3`

### Required Conditions (capture if present)
- Cloud cover: low (<30%), moderate (30-70%), high (>70%)
- Solar radiation: clear sky, partly cloudy, overcast
- Season: summer (high solar radiation) vs winter (low solar radiation)
- Time of day: daytime (photochemistry active) vs nighttime (photochemistry inactive)
- Humidity: high RH can enhance photochemistry in some cases
- VOC availability: high VOC concentrations needed for SOA formation

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Direct cloud cover → PM2.5 (without mechanism)
- ❌ `cloud_cover → pm25` (nếu không có intermediate mechanism)
- Action: Chỉ extract nếu paper mô tả rõ mechanism

### Detailed chemical mechanisms (→ prompt_02, prompt_08)
- ❌ Detailed SOA chemistry pathways (unless tied to solar radiation)
- ❌ Detailed SIA chemistry (unless tied to photochemistry)
- Action: handoff_to_other_prompts ["chemical_processes"]

### Inversion/PBLH micro-physics (→ prompt_01)
- ❌ Detailed inversion formation physics unless tied to cloud cover
- Action: handoff_to_other_prompts ["meteorological_pathways"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "cloud cover atmospheric stability inversion PM2.5 Hanoi"
2. "solar radiation photochemistry SOA formation PM2.5 Southeast Asia"
3. "cloud cover solar radiation boundary layer PM2.5"
4. "photochemical reactions VOC oxidation PM2.5 formation"
5. "cloud-radiation interaction PM2.5 accumulation"
6. "daytime photochemistry PM2.5 secondary aerosol formation"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Prefer papers that:
  - Quantify cloud cover effects on stability/PBLH
  - Describe photochemistry mechanisms (not just correlations)
  - Use radiation measurements or photolysis rate calculations
  - Separate daytime vs nighttime effects

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm:
- Intermediate nodes mới (cloud_cover → stability, solar_radiation → photochemistry)
- Mechanisms mới (stability vs photochemistry)
- Conditions mới (cloud cover thresholds, solar radiation levels)

## EXTRACTION PHASE

### Extraction Rules
1. **Ưu tiên chains dài**: Luôn tách thành 3-4 bước thay vì 1-2 bước nếu paper mô tả đủ chi tiết.
2. **Evidence bắt buộc**: Mỗi step trong chain phải có source_quote riêng hoặc quote chung cho cả chain.
3. **Intermediate nodes**: Nếu paper chỉ nói "cloud cover → PM2.5" mà không mô tả mechanism → không extract; ghi missing_info.
4. **Moderator effects**: Capture cloud cover as moderator của solar radiation → photochemistry.
5. **Temporal conditions**: Luôn ghi rõ daytime vs nighttime trong conditions.

### Chain Building Strategy
- Nếu paper mô tả: "Cloud cover reduces solar radiation and increases stability"
  - Extract: `cloud_cover → reduced_solar_radiation → reduced_surface_heating → atmospheric_stability → inversion → pm25` (5 steps)

- Nếu paper mô tả: "Solar radiation drives photochemistry and SOA formation"
  - Extract: `solar_radiation → photolysis → radical_formation → oxidation_reactions → soa_formation → pm25` (5 steps)

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "meteorological_pathways"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "met_cloud_001",
  "category": "meteorological_pathways",
  "cause_node": "cloud_cover",
  "effect_node": "reduced_solar_radiation",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Cloud cover (đặc biệt là overcast conditions với cloud fraction >70%) làm giảm lượng solar radiation đến bề mặt do clouds hấp thụ và phản xạ ánh sáng mặt trời.",
  "conditions": [
    "High cloud cover (>70%)",
    "Overcast conditions",
    "Daytime"
  ],
  "temporal_lag": "immediate",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1029/2018JD029123",
  "source_title": "Cloud cover effects on boundary layer dynamics and PM2.5 in urban areas",
  "source_authors": "Smith et al.",
  "source_year": "2019",
  "source_doi": "10.1029/2018JD029123",
  "source_quote": "High cloud cover (>70%) reduces surface solar radiation by 60-80% compared to clear sky conditions.",
  "source_locator": "Results",
  "seasonal_variation": "all_seasons",
  "spatial_scope": "local",
  "notes": "Step 1 of chain: cloud_cover → reduced_solar_radiation → reduced_surface_heating → atmospheric_stability → inversion → pm25"
}
```

```json
{
  "id": "met_solar_001",
  "category": "meteorological_pathways",
  "cause_node": "solar_radiation",
  "effect_node": "photolysis",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Solar radiation (đặc biệt là UV radiation) cung cấp năng lượng để phá vỡ các phân tử như NO2, O3, HONO, và VOCs thông qua quá trình photolysis, tạo ra các radicals như OH, HO2, NO3.",
  "conditions": [
    "Clear sky or partly cloudy conditions",
    "Daytime (solar radiation > 0)",
    "UV radiation present"
  ],
  "temporal_lag": "minutes to hours",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1021/acs.est.0c01234",
  "source_title": "Photochemical formation of secondary organic aerosol in urban environments",
  "source_authors": "Johnson et al.",
  "source_year": "2021",
  "source_doi": "10.1021/acs.est.0c01234",
  "source_quote": "Solar UV radiation drives photolysis of NO2, O3, and HONO, producing OH radicals that initiate VOC oxidation and SOA formation.",
  "source_locator": "Methods",
  "seasonal_variation": "summer",
  "spatial_scope": "local",
  "notes": "Step 1 of chain: solar_radiation → photolysis → radical_formation → oxidation_reactions → soa_formation → pm25"
}
```

```json
{
  "id": "met_cloud_solar_001",
  "category": "meteorological_pathways",
  "cause_node": "cloud_cover",
  "effect_node": "reduced_photochemistry",
  "relationship_type": "MODERATOR",
  "mechanism": "Cloud cover làm giảm solar radiation đến bề mặt, từ đó giảm photolysis rate và làm chậm các phản ứng photochemistry, dẫn đến giảm formation của SOA và các secondary aerosols.",
  "conditions": [
    "High cloud cover (>70%)",
    "Daytime",
    "VOC and NOx present"
  ],
  "temporal_lag": "hours",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "source_url": "https://doi.org/10.1021/acs.est.0c01234",
  "source_title": "Photochemical formation of secondary organic aerosol in urban environments",
  "source_authors": "Johnson et al.",
  "source_year": "2021",
  "source_doi": "10.1021/acs.est.0c01234",
  "source_quote": "Cloud cover reduces photolysis rates by 50-70%, slowing photochemical reactions and reducing SOA formation rates.",
  "source_locator": "Results",
  "seasonal_variation": "all_seasons",
  "spatial_scope": "local",
  "notes": "Moderator effect: cloud_cover moderates solar_radiation → photochemistry → soa_formation"
}
```

## COMMON PITFALLS TO AVOID
- ❌ Bỏ qua intermediate nodes (ví dụ: chỉ extract `cloud_cover → pm25` mà không có `reduced_solar_radiation`, `atmospheric_stability`)
- ❌ Không phân biệt rõ stability effects vs photochemistry effects của cloud cover
- ❌ Không capture temporal conditions (daytime vs nighttime)
- ❌ Không ghi rõ cloud cover thresholds hoặc solar radiation levels trong conditions
- ❌ Không capture moderator effects của cloud cover trên solar radiation → photochemistry

## NOTES
- Prompt này bổ sung cho `prompt_01_meteorological_pathways.md` bằng cách tập trung vào **cloud cover** và **solar radiation photochemistry** mechanisms.
- Nếu paper chỉ mô tả correlation mà không có mechanism, không extract.
- Ưu tiên papers có radiation measurements hoặc photolysis rate calculations để có evidence mạnh.
