# PROMPT 10: SYNOPTIC PATTERNS & COLD SURGE TRANSPORT
# Focused Task: Extract causal chains cold surge/monsoon/synoptic → transport/stagnation → PM2.5 (Hanoi/SEA)
# Version: 2.0 - For Manus Auto-Discovery
# Category: transport_mechanisms

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia **synoptic meteorology & regional transport** cho khu vực Đông Á/Đông Nam Á, quen thuộc với:
- East Asian Winter Monsoon (EAWM), Northeast monsoon
- cold surge onset vs persistence
- synoptic patterns như blocking high, upper-level ridge/low.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về **cơ chế synoptic và cold surge** (gió mùa Đông Bắc, EAWM, ridge/low-pressure patterns) gây tăng/giảm PM2.5 tại Hà Nội và khu vực Đông Nam Á.

Mục tiêu: chuyển các kết luận “cold surge → PM2.5 tăng” thành **chuỗi cơ chế 2–4 bước** (transport → stagnation → mixing changes → PM2.5).

## CATEGORY DEFINITION
**Category**: `transport_mechanisms`

**Focus**: Synoptic drivers controlling regional transport and local stagnation of PM2.5 and/or precursors.

## IN-SCOPE (Allowed Relationships)

### A) Cold surge onset: regional transport chain
1. **cold_surge_onset → long_range_transport**
2. **long_range_transport → pm25** (increase; mark regional scope if from China)
3. **cold_surge_onset → change_air_mass_trajectory → pm25**

### B) Cold surge persistence: stagnation chain
4. **cold_surge_persistence → stagnation**
5. **stagnation → reduced_dispersion/mixing → pm25**

### C) Monsoon / synoptic forcing (seasonal synoptic patterns)
6. **east_asian_winter_monsoon → long_range_transport → pm25**
7. **upper_level_ridge_low_pressure_system → synoptic_stagnation → pm25**
8. **blocking_high / anticyclone → stagnation → pm25**

### Allowed Intermediate Nodes
- `long_range_transport`, `regional_transport`, `change_air_mass_trajectory`
- `stagnation`, `synoptic_stagnation`, `reduced_dispersion`, `reduced_vertical_mixing`
- `synoptic_forcing`, `blocking_high`, `anticyclone`

### Required Conditions (capture if present)
- phase: onset vs persistence
- season window (Oct–Mar)
- wind sector/trajectory evidence
- geographic source region (eastern China, Red River Delta, etc.)

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Meteorology micro-physics (→ prompt_01)
- ❌ detailed inversion/PBLH physics unless the paper’s primary contribution is synoptic transport/stagnation
- Action: handoff_to_other_prompts ["meteorological_pathways"]

### Emissions details (→ prompt_04)
- ❌ source inventory; emission factor breakdown
- Action: handoff_to_other_prompts ["emission_sources"]

### Chemical pathways of SIA (→ prompt_02 / prompt_08)
- ❌ detailed aq-phase chemistry not tied to synoptic transport/stagnation
- Action: handoff_to_other_prompts ["chemical_processes"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "cold surge onset persistence PM2.5 Hanoi mechanism transport stagnation"
2. "East Asian winter monsoon PM2.5 Hanoi long-range transport"
3. "synoptic meteorological mechanisms transboundary air pollution Hanoi"
4. "air mass trajectory analysis PM2.5 Hanoi winter"
5. "blocking high stagnation PM2.5 Southeast Asia"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Prefer papers that explicitly separate onset vs persistence and quantify impacts

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm mắt xích (transport/stagnation/mixing) hoặc điều kiện synoptic/trajectory mới.

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract IN-SCOPE synoptic/transport/stagnation mechanisms.
2. Evidence bắt buộc: quote + URL/DOI + locator cho mỗi relationship.
3. Nếu paper chỉ nói “winter monsoon correlates with PM2.5” mà không nêu transport/stagnation mechanism → không đưa vào relationships; ghi missing_info.
4. Ưu tiên split chain:
   - `cold_surge_onset → long_range_transport`
   - `long_range_transport → pm25`
   - `cold_surge_persistence → stagnation`
   - `stagnation → pm25`

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "transport_mechanisms"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "trans_cold_001",
  "category": "transport_mechanisms",
  "cause_node": "cold_surge_onset",
  "effect_node": "long_range_transport",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Trong giai đoạn onset của cold surge gió mùa Đông Bắc, các air mass lạnh từ Siberia High di chuyển qua vùng công nghiệp hóa ở Đông Trung Quốc rồi xuống phía Nam, mang theo các chất ô nhiễm dạng hạt và tiền chất tới Bắc Việt Nam.",
  "conditions": [
    "Cold surge onset phase",
    "East Asian winter monsoon active",
    "Trajectories passing over eastern China"
  ],
  "temporal_lag": "1-3d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2023.119669",
  "source_title": "Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period",
  "source_authors": "Phung-Ngoc et al.",
  "source_year": "2023",
  "source_doi": "10.1016/j.atmosenv.2023.119669",
  "source_quote": "During cold surge onsets, long-range transport from China causes an average increase of about 30% in PM2.5 concentrations in Hanoi.",
  "source_locator": "Results",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Nên kết nối edge này với edge long_range_transport → pm25."
}
```

```json
{
  "id": "trans_cold_002",
  "category": "transport_mechanisms",
  "cause_node": "long_range_transport",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Air mass được vận chuyển xa từ các vùng công nghiệp hóa phía thượng gió mang theo nền PM2.5 cao và SIA giàu sulfate/nitrate, làm tăng thêm mức PM2.5 quan sát tại Hà Nội trong các đợt cold surge.",
  "conditions": [
    "Trajectories from eastern China",
    "Cold surge events",
    "Background pollution elevated"
  ],
  "temporal_lag": "1-3d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2023.119669",
  "source_title": "Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period",
  "source_authors": "Phung-Ngoc et al.",
  "source_year": "2023",
  "source_doi": "10.1016/j.atmosenv.2023.119669",
  "source_quote": "The long-range transport from China during cold surge onsets increases PM2.5 levels in Hanoi by about 30%.",
  "source_locator": "Results",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Edge thứ hai trong chuỗi cold_surge_onset → long_range_transport → pm25."
}
```

## COMMON PITFALLS TO AVOID
- Gộp onset và persistence thành một mối quan hệ.
- Không ghi rõ nguồn transport (upwind region) hoặc season window.
- Không chỉ ra rõ đây là cơ chế regional/long-range (spatial_scope: regional), dễ gây hiểu nhầm là local.


