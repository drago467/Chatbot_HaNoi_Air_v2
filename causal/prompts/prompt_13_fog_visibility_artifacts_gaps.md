# PROMPT 13: FOG, VISIBILITY & ARTIFACTS
# Focused Task: Extract edge-case causal relationships fog/visibility/high RH → measurement artifacts or non-intuitive PM2.5 outcomes
# Version: 2.0 - For Manus Auto-Discovery
# Category: edge_cases

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia **khí tượng sương mù & đo đạc PM**, quen thuộc với:
- hiện tượng fog/haze/low visibility,
- aerosol liquid water (ALW) trong sương mù,
- các sai số của thiết bị đo PM (nhất là optical scattering) trong điều kiện RH rất cao.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships thuộc nhóm **edge cases** liên quan đến:

1) **Fog / very high RH / low visibility** gây ra biến đổi PM2.5 theo cơ chế đặc biệt (ALW tăng, aqueous chemistry bùng phát) hoặc **measurement artifacts**.  
2) Trường hợp “trực giác sai”: trời quang/nắng nóng nhưng PM2.5 vẫn rất cao do cơ chế hóa học/tiền chất.

Mục tiêu: giúp chatbot có thể giải thích các “ngoại lệ” một cách có căn cứ, giảm trả lời chung chung.

## CATEGORY DEFINITION
**Category**: `edge_cases`

**Focus**: Measurement artifacts and non-intuitive conditions that break common assumptions.

## IN-SCOPE (Allowed Relationships)

### A) Fog / low visibility artifacts
1. **fog → measurement_artifact_pm25**
2. **very_high_relative_humidity → measurement_artifact_pm25**
3. **low_visibility → measurement_artifact_pm25**

### B) Fog/ALW as chemistry accelerator (if explicitly stated)
4. **fog/high_ALW → accelerated_aqueous_phase_reaction → sia_formation → pm25**

### C) Clear-sky/high radiation but high PM2.5 (non-intuitive)
5. **clear_sky + high_solar_radiation + high_precursors → secondary_aerosol_formation → pm25**

### Allowed Intermediate Nodes
- `measurement_artifact_pm25`, `low_visibility`, `fog`
- `accelerated_aqueous_phase_reaction`, `secondary_aerosol_formation`

### Required Conditions to capture
- RH near saturation (e.g., `RH > 90%`)
- fog episodes, nighttime/early morning
- instrument/measurement method if paper mentions it (e.g., optical scattering)
- clear-sky conditions + precursor-rich environment

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### General wet scavenging by rain (→ prompt_09)
- ❌ precipitation-driven removal
- Action: handoff_to_other_prompts ["meteorological_pathways"]

### General SIA chemistry without edge-case framing (→ prompt_02 / prompt_08)
- ❌ standard chemistry pathways not tied to fog/visibility artifact or non-intuitive cases
- Action: handoff_to_other_prompts ["chemical_processes"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "fog measurement artifact PM2.5 optical sensor high humidity"
2. "low visibility haze aerosol liquid water rapid sulfate formation"
3. "high relative humidity PM2.5 measurement bias"
4. "clear sky high radiation secondary aerosol formation PM2.5"
5. "fog haze episodes Hanoi PM2.5 mechanism"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Instrumentation/measurement methodology papers are allowed if they provide explicit artifact mechanism

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm cơ chế artifact mới (sensor bias type, RH threshold) hoặc edge-case chemistry framing.

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract edge-case relationships, ghi rõ trong `notes` rằng đây là ngoại lệ/measurement artifact.
2. Evidence bắt buộc: quote + URL/DOI + locator.
3. Nếu paper chỉ nói “fog correlates with PM2.5” mà không nêu artifact mechanism hoặc chemistry mechanism → không đưa vào relationships; ghi missing_info.
4. Mỗi nguồn tối đa 10 relationships.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "edge_cases"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "edge_fog_001",
  "category": "edge_cases",
  "cause_node": "fog",
  "effect_node": "measurement_artifact_pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Trong điều kiện sương mù dày và độ ẩm tương đối gần 100%, các hạt sương có thể bị cảm biến optical scattering ghi nhận như hạt PM2.5, dẫn đến việc đánh giá cao hơn thực tế nồng độ PM2.5.",
  "conditions": [
    "Fog episodes",
    "RH > 95%",
    "Optical scattering instruments"
  ],
  "temporal_lag": "0-1h",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://doi.org/10.5194/amt-9-3497-2016",
  "source_title": "Influence of high humidity on PM2.5 measurements by optical particle counters",
  "source_authors": "Nguyen et al.",
  "source_year": "2016",
  "source_doi": "10.5194/amt-9-3497-2016",
  "source_quote": "Under fog conditions with RH exceeding 95%, optical particle counters significantly overestimated PM2.5 mass concentrations due to the presence of large water droplets.",
  "source_locator": "Results",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Phải được phân biệt rõ với các trường hợp PM2.5 thực sự tăng do chemistry."
}
```

```json
{
  "id": "edge_clear_001",
  "category": "edge_cases",
  "cause_node": "clear_sky_high_solar_radiation",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Trong bối cảnh nền tiền chất cao (NOx, SO2, VOCs), điều kiện trời quang và bức xạ mặt trời mạnh vào mùa đông có thể tăng cường phản ứng quang hóa và các phản ứng multiphase, dẫn đến hình thành mạnh secondary aerosols (SIA/SOA) và làm PM2.5 tăng cao, mặc dù trực giác thường nghĩ trời nắng là không khí sạch.",
  "conditions": [
    "Clear-sky winter days",
    "High solar radiation",
    "High precursor levels (NOx, SO2, VOCs)"
  ],
  "temporal_lag": "6-24h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "source_url": "https://doi.org/10.1038/s41467-020-16683-x",
  "source_title": "Fast sulfate formation from oxidation of SO2 by NO2 and HONO observed in Beijing haze",
  "source_authors": "Wang et al.",
  "source_year": "2020",
  "source_doi": "10.1038/s41467-020-16683-x",
  "source_quote": "Winter haze episodes with clear-sky conditions and strong solar radiation can still exhibit high PM levels due to enhanced secondary aerosol formation from abundant precursors.",
  "source_locator": "Discussion",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Đây là edge case 'trời đẹp nhưng PM2.5 vẫn cao'; cần nhấn mạnh trong giải thích cho người dùng."
}
```

## COMMON PITFALLS TO AVOID
- Nhầm “fog increases PM2.5” (do chemistry) với “fog biases PM2.5 measurement”.
- Không ghi rõ điều kiện RH/visibility threshold.
- Không phân biệt artifact (measurement_artifact_pm25) với tăng PM2.5 thực sự do hóa học.


