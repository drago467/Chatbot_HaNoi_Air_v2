# Causal Relationship Extraction Prompts
# Domain: Air Pollution (PM2.5, Pollutants, Meteorology)
# Version: 1.0

## Tổng quan

Bộ prompts này được thiết kế để extract causal relationships từ papers khoa học (tiếng Anh và tiếng Việt) về ô nhiễm không khí, đặc biệt tập trung vào PM2.5 tại Hà Nội và khu vực Đông Nam Á.

## Cấu trúc Prompts

### Prompt 00: Master Template
**File**: `prompt_00_master_template.md`
- Template chung cho tất cả các prompts
- Định nghĩa output format (JSON)
- Naming conventions
- Quality criteria
- Common pitfalls

**Sử dụng**: Đọc trước khi sử dụng các prompts khác. Đây là foundation cho tất cả các prompts.

### Prompt 01: Meteorological Pathways
**File**: `prompt_01_meteorological_pathways.md`
**Focus**: Causal relationships giữa các biến khí tượng và PM2.5

**Các pathways chính**:
- Temperature → Inversion → PBLH → PM2.5
- Wind Speed → Dispersion → PM2.5
- Wind Direction → Transport → PM2.5
- Humidity → Chemical Processes → PM2.5
- Precipitation → Wet Deposition → PM2.5
- Cloud Cover → Solar Radiation → PBLH → PM2.5
- Pressure → Atmospheric Stability → PM2.5
- Stability Index → Atmospheric Stability → PM2.5

**Sử dụng**: Khi extract từ papers về khí tượng học và ô nhiễm không khí.

### Prompt 02: Chemical Processes
**File**: `prompt_02_chemical_processes.md`
**Focus**: Các phản ứng hóa học hình thành PM2.5 và secondary aerosols

**Các pathways chính**:
- SO2 + NO2 + Humidity → SIA Formation → PM2.5
- NO2 + O3 + Solar Radiation → Nitrate Formation → PM2.5
- VOCs + NOx + Solar Radiation → O3 Formation → Secondary Aerosols
- NH3 + HNO3 → Ammonium Nitrate → PM2.5
- Temperature → Chemical Reaction Rate → PM2.5

**Sử dụng**: Khi extract từ papers về hóa học khí quyển và aerosol physics.

### Prompt 03: Transport Mechanisms
**File**: `prompt_03_transport_mechanisms.md`
**Focus**: Vận chuyển và lan truyền ô nhiễm

**Các pathways chính**:
- Wind Direction + Emission Sources → Regional Transport → PM2.5
- Wind Speed → Transport Distance → PM2.5
- Cold Surge → Wind Pattern → PM2.5 (non-linear)
- Long-range Transport → Background Pollution → PM2.5
- Topography → Air Flow → PM2.5 Accumulation

**Sử dụng**: Khi extract từ papers về động lực học khí quyển và vận chuyển ô nhiễm.

### Prompt 04: Emission Sources
**File**: `prompt_04_emission_sources.md`
**Focus**: Nguồn phát thải và tác động đến PM2.5

**Các pathways chính**:
- Traffic → NOx/PM2.5 Primary → PM2.5
- Industry → SO2/NOx → Secondary Aerosols → PM2.5
- Biomass Burning → PM2.5 Primary + VOCs → PM2.5
- Construction → Resuspension → PM2.5
- Power Plants → SO2/NOx → Secondary Aerosols → PM2.5
- Residential Heating → PM2.5 Primary → PM2.5

**Sử dụng**: Khi extract từ papers về emission inventory và source apportionment.

### Prompt 05: Static Factors
**File**: `prompt_05_static_factors.md`
**Focus**: Các yếu tố tĩnh (LULC, địa hình, dân cư) ảnh hưởng PM2.5

**Các pathways chính**:
- Urban Density → Emission Sources → PM2.5
- Land Use Type → Emission Patterns → PM2.5
- Topography → Air Flow → PM2.5 Accumulation
- Distance to Roads → Traffic Exposure → PM2.5
- Vegetation → Deposition → PM2.5
- Industrial Zones → Emissions → PM2.5
- Valley/Basin Topography → Air Trapping → PM2.5
- TWI → Air Flow → PM2.5

**Sử dụng**: Khi extract từ papers về địa lý môi trường, quy hoạch đô thị, và GIS applications.

### Prompt 06: Seasonal Patterns
**File**: `prompt_06_seasonal_patterns.md`
**Focus**: Quy luật theo mùa và temporal variations

**Các pathways chính**:
- Season → Weather Pattern → PM2.5
- Season → Emission Pattern → PM2.5
- Diurnal Cycle → PBLH Variation → PM2.5
- Month → Agricultural Activity → Biomass Burning → PM2.5
- Holiday Period → Traffic Pattern → PM2.5
- Time of Day → Emission Intensity → PM2.5

**Sử dụng**: Khi extract từ papers về biến đổi khí hậu và quy luật thời tiết theo mùa.

### Prompt 07: Edge Cases and Exceptions
**File**: `prompt_07_edge_cases.md`
**Focus**: Các trường hợp đặc biệt và exceptions

**Các edge cases chính**:
- Humidity cao → PM2.5 tăng (measurement artifact)
- Wind Speed cao → PM2.5 không giảm (transport from sources)
- Precipitation nhẹ → PM2.5 không giảm
- Temperature cao → PM2.5 tăng (high emissions + photochemistry)
- Non-linear relationships (threshold effects, reversal effects)

**Sử dụng**: Khi extract các trường hợp đặc biệt không tuân theo quy luật thông thường.

### Prompts 08–13: Gap-Focused / Advanced

Các prompt này mở rộng 01–07, tập trung lấp các \"gaps\" cụ thể được phát hiện sau vòng extract đầu tiên.  
Tên file giữ hậu tố `_gaps` để dễ tracing.

- **Prompt 08: Winter Chemistry – SIA Chains**  
  - **File**: `prompt_08_winter_chemistry_sia_gaps.md`  
  - **Focus**: Chuỗi hóa học mùa đông: `RH/ALW/pH/NH3/NOx/SO2/HONO/H2O2 → SIA → PM2.5` (winter haze, Hanoi/SEA).

- **Prompt 09: Precipitation & Wet Scavenging**  
  - **File**: `prompt_09_precipitation_wet_scavenging_gaps.md`  
  - **Focus**: `precipitation_intensity/duration/type → wet_deposition/scavenging → PM2.5 change`.

- **Prompt 10: Synoptic Patterns & Cold Surge Transport**  
  - **File**: `prompt_10_synoptic_cold_surge_transport_gaps.md`  
  - **Focus**: `cold_surge/monsoon/synoptic_pattern → long_range_transport/stagnation → PM2.5`.

- **Prompt 11: Wind Direction & Upwind Exposure**  
  - **File**: `prompt_11_wind_direction_upwind_exposure_gaps.md`  
  - **Focus**: `wind_direction_sector + upwind_emission_exposure → PM2.5` (industrial/biomass burning/clean marine).

- **Prompt 12: Static Factors as Moderators**  
  - **File**: `prompt_12_static_moderators_gaps.md`  
  - **Focus**: static factors (population, roads, industrial zones, LULC, DEM) như `MODERATOR/INDIRECT_CAUSE` của PM2.5 (baseline & sensitivity).

- **Prompt 13: Fog, Visibility & Artifacts**  
  - **File**: `prompt_13_fog_visibility_artifacts_gaps.md`  
  - **Focus**: edge cases fog/very high RH/low visibility & clear-sky; phân biệt **measurement artifacts** vs **real chemistry increase**.

## Hướng dẫn sử dụng

### Workflow đề xuất

1. **Đọc Master Template trước** (`prompt_00_master_template.md`)
   - Hiểu output format
   - Nắm naming conventions
   - Nắm quality criteria

2. **Chọn prompt phù hợp** dựa trên nội dung paper:
   - Paper về khí tượng → Prompt 01
   - Paper về hóa học → Prompt 02
   - Paper về vận chuyển → Prompt 03
   - Paper về nguồn phát thải → Prompt 04
   - Paper về địa lý/GIS → Prompt 05
   - Paper về biến đổi theo mùa → Prompt 06
   - Paper có edge cases → Prompt 07

3. **Sử dụng kết hợp nhiều prompts** nếu paper cover nhiều aspects:
   - Có thể extract từ cùng một paper với nhiều prompts khác nhau
   - Mỗi prompt tập trung vào một aspect cụ thể

4. **Validate output**:
   - Kiểm tra theo checklist trong mỗi prompt
   - Đảm bảo mechanism rõ ràng
   - Đảm bảo conditions đầy đủ
   - Đảm bảo confidence phù hợp

### Format Input

Khi sử dụng prompts với LLM, format input như sau:

```
[ROLE và TASK từ prompt]

[SPECIFIC FOCUS từ prompt]

[KEY MECHANISMS TO LOOK FOR từ prompt]

[EXAMPLES OF GOOD EXTRACTIONS từ prompt]

[COMMON PITFALLS TO AVOID từ prompt]

---

DOCUMENT TEXT:
[Paste đoạn văn bản từ paper cần extract]

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

### Output Format

Tất cả prompts đều output theo format JSON được định nghĩa trong Master Template:

```json
{
  "relationships": [
    {
      "id": "unique_id",
      "cause_node": "snake_case",
      "effect_node": "snake_case",
      "relationship_type": "DIRECT_CAUSE | INDIRECT_CAUSE | MODERATOR | MEDIATOR",
      "mechanism": "Chi tiết cơ chế",
      "conditions": ["Điều kiện 1", "Điều kiện 2"],
      "temporal_lag": "2-6h",
      "strength": "STRONG | MODERATE | WEAK",
      "confidence": "HIGH | MEDIUM | LOW",
      "evidence_text": "Quote từ document",
      "evidence_page": "Trang/section",
      "seasonal_variation": "winter | summer | all_season",
      "spatial_scope": "local | regional | global",
      "notes": "Ghi chú thêm"
    }
  ],
  "entities_mentioned": ["pm25", "temperature"],
  "missing_info": "Thông tin còn thiếu"
}
```

## Quality Assurance

### Checklist chung (từ Master Template):
- [ ] Mechanism có cụ thể không?
- [ ] Conditions có đầy đủ không?
- [ ] Evidence text có support relationship không?
- [ ] Confidence có phù hợp với evidence không?
- [ ] Temporal lag có hợp lý không?
- [ ] Relationship type có đúng không?
- [ ] Nodes có standardized không?

### Checklist riêng cho mỗi prompt:
- Xem phần "VALIDATION CHECKLIST" trong mỗi prompt file

## Lưu ý quan trọng

1. **CHỈ extract causal relationships**, không phải correlation đơn thuần
2. **Mechanism phải rõ ràng**: Giải thích TẠI SAO và NHƯ THẾ NÀO
3. **Conditions phải cụ thể**: Thresholds, time periods, spatial scope
4. **Confidence phải phù hợp**: Dựa trên quality of evidence
5. **Nodes phải standardized**: Dùng snake_case, tiếng Anh theo naming conventions

## Tài liệu tham khảo

- CausalRAG Paper: `doc/2503.19878v3.pdf`
- MedCoT-RAG Paper: `doc/2508.15849v1.pdf`
- Mở rộng tri thức PM2.5 Hà Nội: `causal/doc/Mở rộng tri thức PM2.5 Hà Nội.md`
- Chatbot Implementation Plan: `causal/doc/chatbot_implementation_plan.md`

## Version History

- **v1.0** (2026-01-21): Initial release
  - 8 prompts (00-07)
  - Cover tất cả các biến và mechanisms chính
  - Support cả tiếng Anh và tiếng Việt
