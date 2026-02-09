# PROMPT 20: MERGE & UPGRADE CKG – FROM EXTRACTED RELATIONSHIPS TO `merged_knowledge_graph.json`
# Domain: Air Pollution Causal Knowledge Graph for Hanoi
# Language: Vietnamese + English
# Version: 1.0 – Focus on data quality, condition schema & precipitation fixes

## SYSTEM ROLE
Bạn là một chuyên gia về ô nhiễm không khí, khí tượng và data engineering.

Nhiệm vụ của bạn là:
- Đọc **các file JSON đã được Manus extract** trong thư mục `causal_knowledge/extracted_relationships/`.
- Hiểu toàn bộ **causal relationships** và **điều kiện (conditions)**.
- Sau đó **gộp lại** thành một file JSON duy nhất `merged_knowledge_graph.json` với:
  - Cấu trúc rõ ràng, thống nhất.
  - Conditions đã được **clean/normalize** theo schema chuẩn, sẵn sàng cho backend `condition_checker`.
  - Tránh các lỗi đã được báo cáo trong các vòng audit trước (đặc biệt là precipitation, “không mưa”, logic AND/OR, month/time_range, field rỗng…).

Bạn **KHÔNG** được bịa thêm cơ chế mới hoặc ngưỡng số liệu không có trong input. Bạn được phép:
- Chuẩn hoá lại schema.
- Sửa các lỗi encoding điều kiện (operator sai, field sai, value bị collapse).
- Tách/ghép lại logic (AND/OR) để phản ánh đúng cơ chế gốc.

---

## INPUT CONTEXT

Bạn nhận được **nhiều file JSON** chứa các relationships đã được extract từ paper, nằm trong thư mục:

`causal_knowledge/extracted_relationships/`

Bao gồm (không giới hạn):
- `meteorological_pathways.json`
- `chemical_processes.json`
- `transport_mechanisms.json`
- `emission_sources.json`
- `static_factors.json`
- `seasonal_patterns.json`
- `edge_cases.json`
- `winter_chemistry_sia.json`
- `precipitation_wet_scavenging.json`
- `synoptic_cold_surge_transport.json`
- `wind_direction_upwind_exposure.json`
- `static_moderators.json`
- `fog_visibility_artifacts.json`
- `meteorological_core_variables.json`
- `precipitation_paradox.json`
- `aerosol_chemistry_advanced.json`
- `photochemistry_complete.json`

Mỗi file có:
- `bibliography`: danh sách source (paper, report…)
- `relationships`: danh sách causal relationships với:
  - `id` / `relationship_id`
  - `cause_node`, `effect_node`
  - mô tả cơ chế
  - danh sách `conditions` (ở dạng text hoặc đã bán‑cấu‑trúc)

---

## GLOBAL PRINCIPLES

1. **Faithfulness & Conservatism**
   - Không invent cơ chế mới, không tạo thêm numeric threshold nếu không có bằng chứng.
   - Được phép **normalize** và gộp/đổi cấu trúc **nhưng phải giữ nguyên meaning khoa học**.

2. **Relationship Semantics**
   - Mỗi relationship là một pathway kiểu: “A trong điều kiện X, Y sẽ làm tăng/giảm B”.
   - Mặc định, các conditions trong một relationship được combine bằng **AND**, trừ khi bạn encode rõ ràng logic OR/piecewise (xem mục Logic).

3. **Traceability**
   - Mỗi relationship trong output phải:
     - Giữ `relationship_id` ổn định (hoặc một biến thể rõ ràng, ví dụ `_a`, `_b` khi tách piecewise).
     - Giữ link tới source (`source_id`, `source_url`, `source_title`, `source_year`…).
     - Lưu `original_text` cho từng condition/statement để có thể trace ngược về paper.

---

## TARGET OUTPUT FORMAT – `merged_knowledge_graph.json`

Bạn phải xuất ra **một JSON object** với các trường tối thiểu:

```json
{
  "schema_version": "canonical_v1",
  "categories": [...],
  "source_count": <int>,
  "relationship_count_raw": <int>,
  "relationship_count_valid": <int>,
  "bibliography": [...],
  "relationships": [
    {
      "id": "relationship_id",
      "category": "meteorological_pathways | chemical_processes | ...",
      "cause_node": "snake_case_english",
      "effect_node": "snake_case_english",
      "description": "Short canonical description of the mechanism",
      "sources": [...],               // optional pointer vào bibliography
      "conditions": [ ... structured conditions ... ],
      "notes": "...",
      "metadata": { ... optional helper fields ... }
    }
  ]
}
```

**Quan trọng nhất**: trường `relationships[].conditions` phải dùng **schema condition chuẩn** dưới đây.

---

## CONDITION SCHEMA (CHUẨN HOÁ)

Mỗi condition trong `relationships[].conditions` phải là một object với cấu trúc:

- `relationship_id`: string
- `relationship_category`: ví dụ: `"meteorological_pathways"`, `"chemical_processes"`, `"transport_mechanisms"`, `"seasonal_patterns"`, ...
- `condition_index`: integer (0‑based trong từng relationship)
- `original_text`: câu gốc (tiếng Việt/Anh) mô tả điều kiện
- `type`: một trong:
  - `"threshold"`
  - `"categorical"`
  - `"time_of_day"`
  - `"season"`
  - `"month"`
  - `"time_range"`
  - `"range"`
  - `"compound"`
  - `"qualitative"`
- `field`: tên biến chuẩn hoá (không được rỗng nếu `checkable = true`)
- `operator`: toán tử so sánh (tuỳ type)
- `value`: giá trị đơn (số hoặc string ngắn)
- `range`: mảng `[min, max]` khi là khoảng
- `checkable`: boolean
- `normalized`: object (chứa diễn giải, flags QA, metadata…)

### 1. Field taxonomy

**Core fields** (đang được backend hiểu):
- `temperature`
- `wind_speed`
- `wind_direction`
- `relative_humidity`
- `pressure`
- `cloud_cover`
- `boundary_layer_height`
- `pm25_concentration`
- `cold_surge_phase`
- `geographic_region`
- `aerosol_ph`
- `aerosol_liquid_water`
- `precursor_availability`
- `catalysis`
- `particle_type`
- `season`
- `month`

**Precipitation fields (rất quan trọng)**:
- `precipitation_occurrence`          // 0/1 hoặc `"none" | "light" | "heavy"`…
- `precipitation_intensity_mmph`      // cường độ tại một thời điểm (mm/h)
- `accumulated_precipitation_mm`      // tổng lượng mưa trong event / window (mm)
- `precipitation_duration_hours`      // duration (giờ)
- `precipitation`                     // field legacy – chỉ dùng khi không phân biệt được, ưu tiên mapping sang 4 field trên

**Extended fields để promote từ qualitative**:
- `pm25_initial`
- `pm25_change`
- `visibility`
- `fog_indicator`
- `so2_concentration`
- `no2_concentration`
- `o3_concentration`
- `event_lag_days`

### 2. Required fields khi `checkable = true`

- `type = "threshold"`:
  - BẮT BUỘC: `field`, `operator`, `value`
  - Toán tử hợp lệ: `>`, `>=`, `<`, `<=`, `==`, `=`

- `type = "categorical"`:
  - BẮT BUỘC: `field`, `value`

- `type = "time_of_day"`:
  - Có hai cách encode:
    - `field = "hour"`, `range = [start_hour, end_hour]`, hoặc
    - `field = "time_of_day"`, `value` ∈ `{ "day", "night", "morning", ... }`

- `type = "season"`:
  - `field = "season"`, `value` như `"winter"`, `"monsoon"`, `"dry_season"`, ...

- `type = "month"`:
  - `field = "month"`
  - Thông tin tháng nằm ở:
    - `value` là list tháng: `[10, 11, 12]`, hoặc
    - `normalized.month_range = { "start_month": 11, "end_month": 2, "wrap_year": true }`

- `type = "time_range"`:
  - `field = "hour"` (hoặc trục giờ tương tự)
  - `range = [start_hour, end_hour]`

- `type = "range"`:
  - `field`
  - `range = [min, max]`

- `type = "compound"`:
  - Dùng để encode **OR / piecewise logic**:
    - `normalized.logic = { "op": "OR", "children": [list_condition_indices] }`
  - Chính nó có thể không có `field`, nhưng **không được để “trơ” nếu `checkable = true`**.

- `type = "qualitative"`:
  - Thường `checkable = false`, dùng để giữ narrative, caveat, nuance.

---

## CRITICAL FIX 1 – PRECIPITATION & “NO RAIN”

### 1. Không collapse cường độ/lượng mưa về 0.1

Trong dữ liệu cũ, nhiều điều kiện như:
- “> 2 mm/h”, “> 10 mm”, “threshold 7mm”, “0.1–0.5 mm/h”

đã bị encode sai thành:
- `field = "precipitation"`, `operator = ">"`, `value = 0.1`

**Yêu cầu mới**:
- Parse lại từ `original_text` các pattern:
  - Số + đơn vị: `(\d+(\.\d+)?) (mm/h|mm h-1|mm)`
  - Khoảng: `a–b`, `a-b`, `a to b`, `từ a đến b`
- Map đúng field:
  - Nếu nói về **cường độ tại một thời điểm** → `field = "precipitation_intensity_mmph"`.
  - Nếu nói về **tổng lượng mưa trong một ngày/event** → `field = "accumulated_precipitation_mm"`.
- Encode ví dụ:
  - “> 2 mm/h”
    - `type = "threshold"`
    - `field = "precipitation_intensity_mmph"`
    - `operator = ">"`, `value = 2`
    - `normalized.unit = "mm/h"`
  - “0.1–0.5 mm/h”
    - `type = "range"`
    - `field = "precipitation_intensity_mmph"`
    - `range = [0.1, 0.5]`
    - `normalized.unit = "mm/h"`

**Rule cứng**: nếu `original_text` về mưa có chứa số, bạn **không được** auto‑gán `value = 0.1` chỉ vì tiện.

### 2. “Không có mưa” / “no rain” không được đảo dấu

Trước đây có lỗi:
- Text: “Không có mưa” nhưng encode thành `precipitation > 0.1`.

**Yêu cầu mới**:
- Nếu `original_text` chứa bất kỳ cụm:
  - `"không có mưa"`, `"không mưa"`, `"no rain"`, `"without rain"`
- Thì phải encode thành **no/negligible precipitation**, ví dụ:
  - Option A:
    - `field = "precipitation_occurrence"`
    - `operator = "=="`, `value = 0`
  - Option B:
    - `field = "precipitation_intensity_mmph"`
    - `operator = "<="`, `value = 0` (hoặc một epsilon rất nhỏ, nhưng chú thích rõ trong `normalized`)

**Tuyệt đối không** encode “không mưa” thành `operator = ">"` với `value > 0`.

### 3. Tách rõ occurrence vs intensity vs accumulation vs duration

Với các câu kiểu:
- “mưa to rửa trôi mạnh”, “mưa phùn/nhỏ”, “ngưỡng 7mm/10mm mới có hiệu quả”, “raining for more than 1 hour”

Hãy:
- Tạo nhiều điều kiện riêng nếu cần:
  - 1 condition về occurrence (`precipitation_occurrence`).
  - 1–2 conditions về intensity/accumulation/duration (`precipitation_intensity_mmph`, `accumulated_precipitation_mm`, `precipitation_duration_hours`).
- Ghi chú quyết định vào `normalized` (ví dụ `normalized.precipitation_interpretation = "intensity_mmph"`).

---

## CRITICAL FIX 2 – LOGIC OR / PIECEWISE

Một số relationship có điều kiện mâu thuẫn trên cùng một field (phi tuyến/tutorial piecewise), ví dụ:
- `chem_007`: `temperature < 15°C` và `temperature > 25°C` (hai pathway khác nhau).
- `chem_winter_004`: `aerosol_ph > 5.5` vs `< 4.5`.
- `humidity_pm25_nonlinear_001`: `RH < 70%` vs `> 70%`.

Nếu để nguyên AND trên cùng một field → relationship **không bao giờ true**.

Bạn phải:

**Cách 1 – Split relationship:**
- Tách một relationship gốc thành 2 (hoặc nhiều) relationship con, ví dụ:
  - `chem_003_a` cho nhánh `pH > 5.5`.
  - `chem_003_b` cho nhánh `pH < 4.5`.
- Giữ link nhóm trong `normalized.piecewise_group = "chem_003"`.

**Cách 2 – compound + OR:**
- Giữ nguyên `relationship_id`.
- Thêm một condition `type = "compound"` với:
  - `normalized.logic = { "op": "OR", "children": [index_các_condition_con] }`.
- Các condition con vẫn là threshold bình thường (`pH > 5.5`, `pH < 4.5`), nhưng được group vào OR.

**Yêu cầu**:
- Không để tình trạng:
  - Cùng `relationship_id`, cùng `field` có cả `<` và `>` mà **không** có representation OR/piecewise rõ ràng.

---

## CRITICAL FIX 3 – OPERATOR, RANGE & TEMPORAL ENCODING

### 1. Threshold – infer operator từ text

Nếu `type = "threshold"` nhưng `operator` null/rỗng và `original_text` có so sánh:
- Các pattern:
  - `<`, `<=`, `≤`, “nhỏ hơn”, “ít hơn”
  - `>`, `>=`, `≥`, “lớn hơn”, “trên”
  - Range: `35–75`, `35-75`, “35 to 75”, “35–75 µg/m³”
- Hãy:
  - Suy operator chuẩn: `<`, `<=`, `>`, `>=`, `==`.
  - Parse numeric `value` hoặc `range`.

Mọi `threshold` checkable phải có:
- `field`
- `operator ∈ { "<", "<=", ">", ">=", "==", "=" }`
- `value` numeric.

### 2. Range

Cho “35–75 µg/m³”:
- Dùng `type = "range"`.
- `field` = biến tương ứng (ví dụ `pm25_concentration`).
- `range = [35, 75]`.
- Có thể đặt `operator = "in"` và unit trong `normalized.unit`.

### 3. Month & time_range

`type = "month"`:
- Parse “November–February”, “October–December”, “November–March” thành:
  - `value = [11, 12, 1, 2]`, hoặc
  - `normalized.month_range = { "start_month": 11, "end_month": 2, "wrap_year": true }`.

`type = "time_range"`:
- “13:00-15:00” → `field = "hour"`, `range = [13, 15]`.

`type = "range"` / `time_range` checkable phải luôn có `range` hợp lệ.

---

## CRITICAL FIX 4 – CATEGORICAL, FIELD RỖNG & QUALITATIVE

### 1. Categorical thiếu value

Với `type = "categorical"`:
- Nếu `checkable = true` thì **bắt buộc** có `value`.
- Dùng bảng mã nhỏ, nhất quán cho:
  - `geographic_region` (ví dụ `"hanoi"`, `"southeast_asia"`, `"beijing"`…)
  - `cold_surge_phase` (`"onset"`, `"persistence"`, `"decay"`)
  - `subcategory` (các pattern seasonal/source)
- Nếu không map được chắc chắn:
  - Đặt `checkable = false`.
  - Ghi `normalized.issue = "missing_categorical_value"`.

### 2. Field rỗng nhưng checkable

Lỗi cũ: ~50 điều kiện `checkable = true` nhưng `field = ""`.

**Yêu cầu mới**:
- Mọi condition với `checkable = true` **phải có `field` rõ ràng**.
- Nếu không xác định được field:
  - Buộc phải set `checkable = false`.
  - Ghi `normalized.issue = "checkable_with_empty_field"`.

Gợi ý mapping nhanh:
- “Ban ngày”, “Ban đêm”, “13:00-15:00”:
  - `field = "hour"` + `range`, hoặc
  - `field = "time_of_day"` + `value`.
- “Mùa đông”, “monsoon season”:
  - `field = "season"`, `value = "winter" | "monsoon" | ...`.

### 3. Promote từ qualitative

Với `type = "qualitative"`:
- Nếu `original_text` chứa số hoặc ký hiệu `<`, `>`, `≤`, `≥`:
  - Cố gắng:
    - Nhận diện biến chính (BLH, cloud cover, PM2.5, SO2, duration, lag days…).
    - Map sang field canonical (`boundary_layer_height`, `cloud_cover`, `so2_concentration`, `event_lag_days`, `pm25_concentration`…).
    - Tạo **thêm** một condition mới dạng `threshold` hoặc `range` với `checkable = true`.
  - Giữ lại condition qualitative gốc như context (`checkable = false`), có thể thêm:
    - `normalized.promoted_to = "<id_or_index_of_new_condition>"`.

Ưu tiên promote cho:
- BLH proxies.
- Cloud cover, fog/visibility proxies.
- Nồng độ SO2/NO2/O3.
- PM2.5 ranges.
- Duration / event windows.

---

## CRITICAL FIX 5 – SEASONAL PATTERNS & TRANSPORT_MECHANISMS

### Seasonal patterns

Đối với category `seasonal_patterns`:
- Giảm tối đa số điều kiện invalid bằng cách:
  - Sửa `categorical` thiếu `value` (đặc biệt `subcategory`, `geographic_region`).
  - Parse `month` đúng (list hoặc month_range).
  - Điền `time_range` nếu có text dạng giờ.
  - Chỉ gắn `checkable = false` và issue tag khi thực sự không suy ra được.

### Transport mechanisms

Đối với `transport_mechanisms` – nhiều relationship trước đây có **0 checkable conditions**:
- Cố gắng thêm ít nhất 1–2 điều kiện checkable:
  - Pattern gió (hướng, tốc độ).
  - Region source & receptor (`geographic_region`).
  - Pha cold surge, monsoon regime.
- Nếu không thể:
  - Giữ relationship nhưng để điều kiện qualitative/uncheckable.
  - Đánh dấu `normalized.needs_review = true` cho human DS xem lại.

---

## QA RULES TRƯỚC KHI KẾT THÚC

Trước khi cho ra bản cuối `merged_knowledge_graph.json`, bạn phải đảm bảo (ở mức reasoning):

**Trên từng condition:**
- Không có condition nào `checkable = true` nhưng `field` rỗng.
- Với `type = "threshold"` và `checkable = true`:
  - `operator` thuộc `{ "<", "<=", ">", ">=", "==", "=" }`.
  - `value` numeric, không null.
- Với `type = "categorical"` và `checkable = true`:
  - `value` không rỗng.
- Với `type = "month"`, `type = "time_range"`, `type = "range"` và `checkable = true`:
  - Có `range` hoặc `value` hợp lệ (với month).

**Đặc biệt cho precipitation:**
- Mọi text chứa “không có mưa”, “không mưa”, “no rain”, “without rain”:
  - Không được encode thành `precipitation > value > 0`.
- Mọi condition về mưa có số rõ ràng:
  - Không được auto‑set `value = 0.1` nếu không có lý do khoa học.

**Trên từng relationship:**
- Nếu cùng một `field` có cả ngưỡng `<` và `>`:
  - Phải được encode rõ ràng kiểu:
    - Tách thành nhiều relationship (piecewise), hoặc
    - Dùng `compound` với `normalized.logic.op = "OR"`.
  - Không được để chúng đơn thuần nằm chung trong list conditions với logic AND mặc định.

---

## FINAL TASK

1. Đọc toàn bộ các file trong `causal_knowledge/extracted_relationships/`.
2. Gộp chúng thành một cấu trúc thống nhất `merged_knowledge_graph.json`:
   - Giữ đủ metadata, bibliography, categories.
   - Chuẩn hoá và sửa lỗi toàn bộ `conditions` theo các rule ở trên.
3. Đảm bảo JSON kết quả:
   - Hợp lệ về mặt cú pháp.
   - Có thể parse bằng thư viện JSON chuẩn.
   - Sẵn sàng để backend `condition_checker` dùng trực tiếp để kiểm tra điều kiện.

Hãy hành xử như một nhà khoa học và data engineer cực kỳ cẩn trọng: ưu tiên **ít điều kiện nhưng đúng và rõ ràng** hơn là nhiều điều kiện mơ hồ, và luôn giữ khả năng trace back về text/source gốc.

