# PROMPT 09: PRECIPITATION & WET SCAVENGING
# Focused Task: Extract causal relationships precipitation/intensity/type → wet_deposition/scavenging → PM2.5 change
# Version: 2.0 - For Manus Auto-Discovery
# Category: meteorological_pathways

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia khí tượng về **mưa và quá trình wet scavenging/wet deposition** của hạt bụi trong khí quyển, đặc biệt trong bối cảnh khí hậu gió mùa Đông Nam Á.  
Bạn hiểu rõ sự khác biệt giữa:
- in-cloud vs below-cloud scavenging
- light vs heavy rain
- monsoon rain vs frontal rain
và cách chúng làm thay đổi nồng độ PM2.5.

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về **mưa và quá trình wet scavenging/wet deposition** làm thay đổi PM2.5 tại Hà Nội/Vietnam/SEA.

Mục tiêu: bổ sung các mắt xích trung gian và điều kiện định lượng (intensity threshold, duration) để tránh mối quan hệ “precipitation → pm25” quá chung chung.

## CATEGORY DEFINITION
**Category**: `meteorological_pathways`

**Focus**: Wet removal processes (in-cloud/below-cloud scavenging), intensity threshold, season dependence.

## IN-SCOPE (Allowed Relationships)

### A) Direct wet removal chain
1. **precipitation → wet_deposition**
2. **wet_deposition → pm25** (decrease via scavenging)

### B) Intensity / duration / type modifiers
3. **precipitation_intensity → scavenging_efficiency → pm25**
4. **precipitation_duration → scavenging_efficiency → pm25**
5. **precipitation_type (convective/frontal/monsoon) → scavenging_efficiency → pm25**

### C) Conditions & thresholds (capture if present)
- light vs moderate vs heavy rain
- rainfall rate (mm/h), accumulated rain (mm), duration (h)
- season (wet/dry; summer monsoon vs winter)
- in-cloud vs below-cloud scavenging mechanisms

### Allowed Intermediate Nodes
- `wet_deposition`, `scavenging_efficiency`, `in_cloud_scavenging`, `below_cloud_scavenging`
- `precipitation_intensity`, `precipitation_duration`, `precipitation_type`

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Fog/visibility measurement artifacts (→ prompt_13)
- ❌ fog-driven measurement artifact unless explicitly linked
- Action: handoff_to_other_prompts ["edge_cases"]

### Chemical formation (→ prompt_02 / prompt_08)
- ❌ RH/ALW chemistry pathways unrelated to rain scavenging
- Action: handoff_to_other_prompts ["chemical_processes"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "wet scavenging PM2.5 rainfall intensity scavenging efficiency"
2. "wet deposition particulate matter scavenging below-cloud in-cloud"
3. "precipitation effect PM2.5 Hanoi Vietnam monsoon"
4. "rain washout PM2.5 reduction threshold mm per hour"
5. "monsoon wet deposition PM2.5 Southeast Asia"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Tier-2 (WHO/agency reports) allowed if mechanism clearly described

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm: (a) ngưỡng intensity/duration mới, (b) cơ chế scavenging mới, hoặc (c) điều kiện mùa/loại mưa mới.

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract IN-SCOPE wet removal relationships.
2. Mỗi relationship bắt buộc có quote/URL/locator.
3. Nếu paper chỉ nói “rain correlates with lower PM” mà không mô tả cơ chế scavenging → confidence tối đa MEDIUM và ghi rõ limitation, hoặc đưa vào missing_info theo guardrails.
4. Ưu tiên tách thành chuỗi 2 bước: `precipitation → wet_deposition → pm25`.
5. Mỗi nguồn tối đa 10 relationships.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "meteorological_pathways"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "met_rain_001",
  "category": "meteorological_pathways",
  "cause_node": "precipitation_intensity",
  "effect_node": "wet_deposition",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Cường độ mưa càng lớn thì hiệu quả rửa trôi các hạt PM2.5 trong cột khí quyển càng cao. Mưa mạnh làm tăng đáng kể hệ số scavenging, đặc biệt đối với các hạt mịn trong lớp biên gần mặt đất.",
  "conditions": [
    "Rainfall rate > 5 mm h-1",
    "Convective rain events",
    "Urban environment"
  ],
  "temporal_lag": "0-3h",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6013115/",
  "source_title": "Comparison of dry and wet deposition of particulate matter in near-surface waters during summer",
  "source_authors": "Wu et al.",
  "source_year": "2018",
  "source_doi": "10.1371/journal.pone.0199241",
  "source_quote": "Wet deposition was more effective in scavenging PM2.5 (92% efficiency) during strong precipitation events.",
  "source_locator": "Results",
  "seasonal_variation": "summer",
  "spatial_scope": "local",
  "notes": "Có thể kết hợp với edge thứ hai: wet_deposition → pm25 (decrease)."
}
```

```json
{
  "id": "met_rain_002",
  "category": "meteorological_pathways",
  "cause_node": "wet_deposition",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Trong và ngay sau các trận mưa vừa đến mưa to, nồng độ PM2.5 trong không khí giảm mạnh do các hạt bị cuốn theo hạt mưa (washout).",
  "conditions": [
    "Accumulated rainfall > 10 mm",
    "Event duration > 1 h"
  ],
  "temporal_lag": "0-6h",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6013115/",
  "source_title": "Comparison of dry and wet deposition of particulate matter in near-surface waters during summer",
  "source_authors": "Wu et al.",
  "source_year": "2018",
  "source_doi": "10.1371/journal.pone.0199241",
  "source_quote": "Wet deposition events significantly reduced PM2.5 mass concentrations, with removal efficiencies exceeding 90% for fine particles.",
  "source_locator": "Discussion",
  "seasonal_variation": "summer",
  "spatial_scope": "local",
  "notes": "Quan hệ này có thể tổng quát cho bối cảnh gió mùa mưa lớn ở Đông Nam Á."
}
```

## COMMON PITFALLS TO AVOID
- Không phân biệt intensity/duration (mưa nhẹ vs mưa lớn).
- Nhầm lẫn mưa gây giảm PM2.5 với các trường hợp RH/ALW tăng (cơ chế hóa học khác).
- Gộp luôn mọi loại mưa vào một mối quan hệ mà không ghi rõ điều kiện.

