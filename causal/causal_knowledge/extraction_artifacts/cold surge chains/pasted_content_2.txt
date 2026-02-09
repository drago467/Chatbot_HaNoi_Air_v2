# PROMPT 14: COLD SURGE CAUSAL CHAINS (Extended)
# Focused Task: Extract long causal chains (3-4 steps) for cold surge mechanisms
# Version: 2.0 - For Manus Auto-Discovery
# Category: transport_mechanisms

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia về **synoptic meteorology và regional transport mechanisms** cho khu vực Đông Á/Đông Nam Á, với kiến thức sâu về:
- Cold surge onset vs persistence phases và cơ chế khác biệt
- Synoptic patterns (blocking high, upper-level ridge/low-pressure systems)
- Regional transport mechanisms và air mass trajectories
- Wind direction changes và upwind exposure effects

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract **causal chains dài (3-4 bước)** về cơ chế cold surge gây tăng PM2.5 tại Hà Nội và khu vực Đông Nam Á.

**Mục tiêu đặc biệt**: Bổ sung các **intermediate nodes** còn thiếu để tạo chains dài từ cold surge → PM2.5, thay vì chỉ có relationships 1 bước.

## CATEGORY DEFINITION
**Category**: `transport_mechanisms`

**Focus**: Long causal chains (3-4 steps) explaining cold surge → PM2.5 mechanisms with intermediate processes.

## IN-SCOPE (Allowed Relationships)

### A) Cold surge onset: Complete transport chain (4 steps)
1. **cold_surge_onset → synoptic_pattern** (blocking high, upper-level ridge/low)
2. **synoptic_pattern → regional_transport** (air mass trajectory change)
3. **regional_transport → regional_pollution_advection** (pollution from upwind sources)
4. **regional_pollution_advection → pm25** (increase at receptor site)

**Alternative chain**:
5. **cold_surge_onset → wind_direction_change** (shift to northerly/northeasterly)
6. **wind_direction_change → upwind_exposure** (exposure to industrial/urban sources)
7. **upwind_exposure → regional_pollution_advection → pm25**

### B) Cold surge persistence: Stagnation and accumulation chain (3-4 steps)
8. **cold_surge_persistence → synoptic_stagnation** (blocking high, reduced wind)
9. **synoptic_stagnation → reduced_dispersion** (both horizontal and vertical)
10. **reduced_dispersion → local_pollution_accumulation** (build-up of local emissions)
11. **local_pollution_accumulation → pm25** (increase)

**Alternative chain**:
12. **cold_surge_persistence → low_wind_speed** (stagnant conditions)
13. **low_wind_speed → reduced_vertical_mixing** (shallow boundary layer)
14. **reduced_vertical_mixing → pblh_decrease** (boundary layer collapse)
15. **pblh_decrease → pm25** (concentration increase)

### C) Combined mechanisms: Onset + Persistence effects
16. **cold_surge_onset → regional_transport → background_pm25_increase**
17. **cold_surge_persistence → local_accumulation → additional_pm25_increase**
18. **background_pm25_increase + additional_pm25_increase → pm25** (combined effect)

### Allowed Intermediate Nodes (use standardized snake_case)
- `synoptic_pattern`, `blocking_high`, `upper_level_ridge`, `anticyclone`
- `regional_transport`, `long_range_transport`, `air_mass_trajectory`
- `wind_direction_change`, `upwind_exposure`, `downwind_location`
- `synoptic_stagnation`, `reduced_dispersion`, `reduced_vertical_mixing`
- `local_pollution_accumulation`, `regional_pollution_advection`
- `background_pm25_increase`, `additional_pm25_increase`

### Required Conditions (capture if present)
- Phase: onset vs persistence (critical distinction)
- Season window: October-March (winter monsoon period)
- Wind sector/trajectory: northerly, northeasterly, easterly
- Geographic source region: eastern China, Red River Delta, etc.
- Synoptic pattern type: blocking high, ridge/low-pressure system
- Duration: short-term (1-3 days) vs prolonged (4+ days)

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Direct cold surge → PM2.5 (1 step only)
- ❌ `cold_surge → pm25` (nếu không có intermediate mechanism)
- Action: Chỉ extract nếu paper mô tả rõ mechanism, nếu không thì skip

### Chemical processes (→ prompt_02, prompt_08)
- ❌ Detailed SIA chemistry during cold surge (unless tied to transport/stagnation)
- Action: handoff_to_other_prompts ["chemical_processes"]

### Local meteorology micro-physics (→ prompt_01)
- ❌ Detailed inversion/PBLH physics unless tied to synoptic forcing
- Action: handoff_to_other_prompts ["meteorological_pathways"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "cold surge onset persistence mechanism PM2.5 Hanoi transport stagnation chain"
2. "East Asian winter monsoon synoptic pattern PM2.5 transport mechanism Hanoi"
3. "cold surge blocking high stagnation PM2.5 accumulation mechanism"
4. "air mass trajectory analysis cold surge PM2.5 regional transport Hanoi"
5. "wind direction change upwind exposure PM2.5 cold surge Hanoi"
6. "synoptic meteorological forcing PM2.5 transport accumulation Southeast Asia"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Prefer papers that:
  - Explicitly separate onset vs persistence phases
  - Quantify transport vs stagnation contributions
  - Describe intermediate mechanisms (not just correlations)
  - Use trajectory analysis or synoptic pattern analysis

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm:
- Intermediate nodes mới trong chains
- Mechanisms mới (transport vs stagnation)
- Conditions mới (synoptic patterns, wind sectors, durations)

## EXTRACTION PHASE

### Extraction Rules
1. **Ưu tiên chains dài**: Luôn tách thành 3-4 bước thay vì 1-2 bước nếu paper mô tả đủ chi tiết.
2. **Evidence bắt buộc**: Mỗi step trong chain phải có source_quote riêng hoặc quote chung cho cả chain.
3. **Intermediate nodes**: Nếu paper chỉ nói "cold surge → PM2.5" mà không mô tả mechanism → không extract; ghi missing_info.
4. **Phase distinction**: Luôn phân biệt rõ onset vs persistence trong conditions.
5. **Spatial scope**: Đánh dấu rõ regional vs local trong spatial_scope.

### Chain Building Strategy
- Nếu paper mô tả: "Cold surge onset brings pollution from China"
  - Extract: `cold_surge_onset → regional_transport → pm25` (2 steps minimum)
  - Hoặc tốt hơn: `cold_surge_onset → synoptic_pattern → regional_transport → regional_pollution_advection → pm25` (4 steps)

- Nếu paper mô tả: "Cold surge persistence causes stagnation"
  - Extract: `cold_surge_persistence → stagnation → reduced_dispersion → local_accumulation → pm25` (4 steps)

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "transport_mechanisms"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "trans_cold_chain_001",
  "category": "transport_mechanisms",
  "cause_node": "cold_surge_onset",
  "effect_node": "synoptic_pattern",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Cold surge onset được điều khiển bởi các synoptic patterns như blocking high ở Siberia và upper-level ridge/low-pressure systems ở Đông Á, tạo ra gradient áp suất mạnh đẩy không khí lạnh về phía Nam.",
  "conditions": [
    "Cold surge onset phase",
    "Siberian High active",
    "Upper-level ridge/low-pressure pattern present",
    "October-March period"
  ],
  "temporal_lag": "0-1d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2023.119669",
  "source_title": "Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period",
  "source_authors": "Phung-Ngoc et al.",
  "source_year": "2023",
  "source_doi": "10.1016/j.atmosenv.2023.119669",
  "source_quote": "Cold surge events are driven by synoptic patterns including blocking highs and upper-level ridge/low-pressure systems that create strong pressure gradients.",
  "source_locator": "Methods",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Step 1 of chain: cold_surge_onset → synoptic_pattern → regional_transport → regional_pollution_advection → pm25"
}
```

```json
{
  "id": "trans_cold_chain_002",
  "category": "transport_mechanisms",
  "cause_node": "synoptic_pattern",
  "effect_node": "regional_transport",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Synoptic patterns (blocking high, ridge/low-pressure) thay đổi air mass trajectories, tạo ra regional transport từ các vùng công nghiệp hóa phía thượng gió (đặc biệt là Đông Trung Quốc) về phía Hà Nội.",
  "conditions": [
    "Blocking high or upper-level ridge/low-pressure pattern",
    "Northerly to northeasterly wind direction",
    "Trajectories passing over eastern China industrial regions"
  ],
  "temporal_lag": "1-2d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2023.119669",
  "source_title": "Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period",
  "source_authors": "Phung-Ngoc et al.",
  "source_year": "2023",
  "source_doi": "10.1016/j.atmosenv.2023.119669",
  "source_quote": "Synoptic patterns during cold surge onset alter air mass trajectories, enabling regional transport from upwind industrial regions (particularly eastern China) to Hanoi.",
  "source_locator": "Results",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Step 2 of chain: cold_surge_onset → synoptic_pattern → regional_transport → regional_pollution_advection → pm25"
}
```

```json
{
  "id": "trans_cold_chain_003",
  "category": "transport_mechanisms",
  "cause_node": "cold_surge_persistence",
  "effect_node": "synoptic_stagnation",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Trong giai đoạn persistence của cold surge, các synoptic patterns (đặc biệt là blocking high) tạo ra điều kiện stagnation với gió yếu và giảm vertical mixing, làm giảm khả năng phân tán chất ô nhiễm.",
  "conditions": [
    "Cold surge persistence phase",
    "Blocking high present",
    "Anticyclonic conditions",
    "January-March period"
  ],
  "temporal_lag": "2-4d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.1016/j.atmosenv.2023.119669",
  "source_title": "Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period",
  "source_authors": "Phung-Ngoc et al.",
  "source_year": "2023",
  "source_doi": "10.1016/j.atmosenv.2023.119669",
  "source_quote": "During cold surge persistence, synoptic patterns (particularly blocking highs) create stagnation conditions with weak winds and reduced vertical mixing, decreasing pollutant dispersion capacity.",
  "source_locator": "Results",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Step 1 of chain: cold_surge_persistence → synoptic_stagnation → reduced_dispersion → local_pollution_accumulation → pm25"
}
```

## COMMON PITFALLS TO AVOID
- ❌ Gộp onset và persistence thành một relationship
- ❌ Bỏ qua intermediate nodes (ví dụ: chỉ extract `cold_surge → pm25` mà không có `synoptic_pattern`, `regional_transport`)
- ❌ Không phân biệt rõ spatial scope (regional transport vs local accumulation)
- ❌ Không ghi rõ phase (onset vs persistence) trong conditions
- ❌ Không capture temporal lag giữa các steps trong chain

## NOTES
- Prompt này bổ sung cho `prompt_10_synoptic_cold_surge_transport_gaps.md` bằng cách tập trung vào **chains dài (3-4 bước)** thay vì chỉ 2 bước.
- Nếu paper chỉ mô tả mechanism 1-2 bước, vẫn extract nhưng đánh dấu trong notes là "có thể kết nối với chains khác".
- Ưu tiên papers có trajectory analysis hoặc synoptic pattern analysis để có evidence mạnh cho intermediate nodes.
