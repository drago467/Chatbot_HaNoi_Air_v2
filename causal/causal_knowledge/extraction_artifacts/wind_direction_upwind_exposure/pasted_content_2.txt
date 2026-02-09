# PROMPT 11: WIND DIRECTION & UPWIND EXPOSURE
# Focused Task: Extract causal relationships wind direction/sector + upwind sources → PM2.5 (Hanoi/Red River Delta/SEA)
# Version: 2.0 - For Manus Auto-Discovery
# Category: transport_mechanisms

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia **vận chuyển chất ô nhiễm theo hướng gió (advection/transport)**, quen thuộc với:
- phân tích **wind sectors** (hướng gió theo góc),
- back-trajectory,
- mối liên hệ giữa **upwind industrial/biomass burning regions** và nồng độ PM2.5 tại Hà Nội/Khu vực sông Hồng.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về **hướng gió (wind direction/sector)** và **phơi nhiễm nguồn phát thải phía thượng gió (upwind exposure)** làm tăng/giảm PM2.5 tại Hà Nội.

Mục tiêu: làm rõ cơ chế “wind_direction → PM2.5” thông qua **upwind sources** (industrial provinces, biomass burning corridors, clean marine air) và điều kiện theo mùa.

## CATEGORY DEFINITION
**Category**: `transport_mechanisms`

**Focus**: Wind-direction-controlled advection/transport + source-region exposure.

## IN-SCOPE (Allowed Relationships)

### A) Wind direction sector → upwind exposure → PM2.5
1. **wind_direction_sector → upwind_emission_exposure**
2. **upwind_emission_exposure → pm25**

### B) Named directional patterns (if papers define them)
3. **north_northeast_winds_in_winter → pm25** (increase; via industrial upwind)
4. **southwesterly_winds_biomass_burning → pm25** (increase; via fire plume transport)
5. **onshore_sea_breeze / marine_air_mass → pm25** (decrease; dilution/clean air)

### Allowed Intermediate Nodes
- `wind_direction_sector`, `upwind_emission_exposure`, `clean_upwind_air`
- `regional_transport`, `advection`

### Required Conditions (capture if present)
- season context (winter monsoon vs summer monsoon)
- wind sector angles (e.g., 0–45°, 45–90°)
- trajectory/back-trajectory confirmation
- named upwind regions

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Wind speed dispersion without direction (→ prompt_01)
- ❌ wind_speed-only dispersion relationships
- Action: handoff_to_other_prompts ["meteorological_pathways"]

### Emissions characterization (→ prompt_04)
- ❌ detailed inventories, emission factors
- Action: handoff_to_other_prompts ["emission_sources"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "wind direction sector PM2.5 Hanoi upwind industrial provinces"
2. "back trajectory wind direction PM2.5 Hanoi winter monsoon"
3. "southwesterly winds biomass burning transport PM2.5 northern Vietnam"
4. "sea breeze dilution PM2.5 coastal urban Southeast Asia"
5. "Red River Delta wind direction air pollution transport"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Prefer papers with trajectory / sector analysis and explicit mechanism language

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract nếu paper mô tả rõ upwind source region hoặc cơ chế transport.
2. Evidence bắt buộc cho mỗi relationship.
3. Nếu chỉ nói “wind direction correlated with PM2.5” mà không mô tả upwind sources/transport → không đưa vào relationships; ghi missing_info.
4. Ưu tiên split chain: `wind_direction_sector → upwind_emission_exposure → pm25`.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "transport_mechanisms"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "trans_wind_001",
  "category": "transport_mechanisms",
  "cause_node": "wind_direction_sector",
  "effect_node": "upwind_emission_exposure",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Khi gió thổi từ sector Đông Bắc (NE, khoảng 30–60°) vào mùa đông, các air mass đi qua các tỉnh công nghiệp hóa ở phía Đông và Đông Bắc Hà Nội, làm tăng phơi nhiễm với các nguồn phát thải SO2, NOx và PM2.5 từ khu công nghiệp và điện than.",
  "conditions": [
    "Wind direction between 30-60 degrees (NE sector)",
    "Winter monsoon season",
    "Trajectories confirmed by back-trajectory analysis"
  ],
  "temporal_lag": "1-3d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2012.05.006",
  "source_title": "Effects of local, regional meteorology and emission sources on mass and compositions of particulate matter in Hanoi",
  "source_authors": "Hai & Kim Oanh",
  "source_year": "2013",
  "source_doi": "10.1016/j.atmosenv.2012.05.006",
  "source_quote": "Northeasterly flows were associated with air masses passing over industrial regions to the east and northeast of Hanoi, enhancing exposure to regional emissions.",
  "source_locator": "Results",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Edge đầu trong chuỗi wind_direction_sector → upwind_emission_exposure → pm25."
}
```

```json
{
  "id": "trans_wind_002",
  "category": "transport_mechanisms",
  "cause_node": "upwind_emission_exposure",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Khi các air mass đi qua các vùng có mật độ công nghiệp cao trước khi đến Hà Nội, nồng độ PM2.5 đo được tại Hà Nội tăng rõ rệt do đóng góp của nền ô nhiễm khu vực.",
  "conditions": [
    "Air masses crossing industrial provinces east/northeast of Hanoi",
    "Stable winter conditions"
  ],
  "temporal_lag": "1-3d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2012.05.006",
  "source_title": "Effects of local, regional meteorology and emission sources on mass and compositions of particulate matter in Hanoi",
  "source_authors": "Hai & Kim Oanh",
  "source_year": "2013",
  "source_doi": "10.1016/j.atmosenv.2012.05.006",
  "source_quote": "Episodes with northeasterly transport from industrial areas were associated with elevated PM2.5 mass and sulfate concentrations in Hanoi.",
  "source_locator": "Discussion",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Khi kết hợp với trans_wind_001 tạo thành chuỗi đầy đủ wind_direction_sector (NE winter) → upwind_emission_exposure → pm25."
}
```

## COMMON PITFALLS TO AVOID
- Nhầm “direction” với “speed”.
- Không ghi rõ sector/season/upwind region.
- Không phân biệt local vs regional transport (bỏ trống hoặc dùng sai spatial_scope).


