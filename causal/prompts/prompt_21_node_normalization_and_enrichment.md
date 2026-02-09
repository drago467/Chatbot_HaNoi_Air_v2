# PROMPT 21: NODE NORMALIZATION & SEMANTIC ENRICHMENT – PHASE 2 CKG
# Domain: Air Pollution Causal Knowledge Graph for Hanoi
# Language: Vietnamese + English
# Version: 1.0 – Focus on canonical nodes, descriptions, and fixing remaining issues

## SYSTEM ROLE
Bạn là một chuyên gia về ô nhiễm không khí, khí tượng và data engineering, được giao nhiệm vụ **chuẩn hoá hệ thống node** và **enrich semantic metadata** cho CKG đã được merge ở Phase 1.

Nhiệm vụ của bạn:
- Đọc file `merged_knowledge_graph_v2.json` (đã được tạo từ 18 file `_clean`).
- **Chuẩn hoá node naming**: tạo mapping từ `original_node` → `canonical_node` và áp dụng vào toàn bộ relationships.
- **Sinh mô tả ngắn** cho mỗi canonical node để phục vụ UI và embedding/retrieval.
- **Sửa các issues còn lại** (đặc biệt là 7 cases `checkable_empty_field` đã được phát hiện trong QA).
- **Thiết kế cấu trúc metadata** để hỗ trợ hybrid retrieval (graph filter + embedding).

Bạn **KHÔNG** được:
- Thay đổi `conditions` (field/operator/value/range) đã được normalize ở Phase 1.
- Invent thêm relationships hoặc cơ chế mới.
- Sửa `bibliography` hoặc `source_*` fields.

Bạn **ĐƯỢC PHÉP**:
- Chuẩn hoá `cause_node` / `effect_node` / `intermediate_nodes` sang canonical form.
- Thêm `canonical_*_node` fields vào relationships (giữ nguyên `original_*_node`).
- Sửa các conditions có `checkable = true` nhưng `field = ""` (map sang field hợp lệ hoặc set `checkable = false`).
- Sinh `description` cho canonical nodes.
- Thêm metadata cho retrieval/embedding.

---

## INPUT CONTEXT

Bạn nhận được:

1. **File chính**: `causal_knowledge/data/merged_knowledge_graph_v2.json`
   - Đã được merge từ 18 file `_clean`.
   - Có `schema_version = "canonical_v2"`.
   - Conditions đã được normalize ở Phase 1 (giữ nguyên 1–1 từ `_clean`).
   - Có thể có một số issues nhỏ (ví dụ: 7 cases `checkable_empty_field`).

2. **File inventory** (optional, nếu đã có): `causal_knowledge/data/node_inventory.json`
   - Chứa danh sách tất cả nodes xuất hiện trong merged_v2.
   - Thống kê số lần xuất hiện theo vai trò (cause/effect/intermediate) và category.

3. **Reference documents** (sẽ được gửi kèm):
   - `prompt_00_master_template.md`: quy tắc naming nodes (snake_case, tiếng Anh), guardrails về evidence và quality.
   - `VARIABLES_CHECKLIST.md`: danh sách các biến đã được cover trong prompts, dùng làm reference cho canonical taxonomy.

---

## GLOBAL PRINCIPLES

1. **Preserve Conditions**
   - **KHÔNG** sửa `conditions` (field/operator/value/range/checkable) đã được normalize ở Phase 1.
   - Chỉ được sửa các cases **rõ ràng là lỗi** (ví dụ: `checkable = true` nhưng `field = ""`).

2. **Node Normalization Strategy**
   - Mapping `original_node → canonical_node` được lưu trong metadata, không xoá `original_*_node`.
   - Canonical nodes phải tuân theo quy tắc naming trong `prompt_00` (snake_case, tiếng Anh).
   - Mỗi canonical node phải có `description` ngắn (1–2 câu) để dùng cho UI/embedding.

3. **Traceability**
   - Giữ nguyên `relationship_id`, `source_*` fields.
   - Thêm `canonical_*_node` nhưng không xoá `original_*_node`.
   - Ghi chú quyết định mapping vào `metadata.node_mapping_reason` nếu cần.

---

## TASK 1: FIX REMAINING ISSUES (checkable_empty_field)

### Vấn đề
QA script đã phát hiện **7 conditions** có `checkable = true` nhưng `field = ""` (hoặc `field` null/rỗng).

**Lưu ý**: Bạn cần tự tìm các conditions này trong file JSON bằng cách:
- Tìm các condition có `"checkable": true` và `"field": ""` (hoặc `"field": null`, hoặc không có field).
- Hoặc tìm các condition có `"checkable": true` nhưng `field` là chuỗi rỗng sau khi strip whitespace.

### Yêu cầu
Với mỗi condition như vậy:

1. **Đọc `original_text`** và cố gắng suy ra field hợp lệ:
   - Nếu là thời gian: `"Ban ngày"`, `"Ban đêm"`, `"13:00-15:00"` → `field = "hour"` hoặc `"time_of_day"`.
   - Nếu là mùa: `"Mùa đông"`, `"monsoon"` → `field = "season"`.
   - Nếu là compound/phức tạp: có thể cần tách thành nhiều conditions hoặc set `checkable = false`.

2. **Nếu không thể map chắc chắn**:
   - Set `checkable = false`.
   - Thêm `normalized.issue = "checkable_with_empty_field"`.
   - Ghi chú trong `normalized.notes` lý do không map được.

3. **Nếu map được**:
   - Điền `field` đúng.
   - Đảm bảo `type`, `operator`, `value`/`range` phù hợp với field mới.
   - Cập nhật `normalized` nếu cần.

### Output
Sau khi sửa, phải **không còn** condition nào `checkable = true` với `field = ""`.

---

## TASK 2: BUILD CANONICAL NODE TAXONOMY

### Bước 1: Inventory nodes hiện có
Từ `merged_knowledge_graph_v2.json`, trích toàn bộ:
- `cause_node` (distinct values)
- `effect_node` (distinct values)
- `intermediate_nodes` (nếu có, flatten thành list)

Gom thành một danh sách `all_nodes` với metadata:
- Số lần xuất hiện làm cause/effect/intermediate.
- Categories xuất hiện.
- Ví dụ relationships liên quan.

### Bước 2: Thiết kế taxonomy canonical
Dựa trên:
- `VARIABLES_CHECKLIST.md` (đã có sẵn canonical names).
- `prompt_00_master_template.md` (quy tắc naming).
- Domain knowledge về ô nhiễm không khí.

Phân loại nodes thành các nhóm:

**Pollutants:**
- `pm25`, `pm10`, `so2`, `no2`, `o3`, `co`, `nox`, `nh3`, `vocs`, `hno3`, `h2o2`, ...

**Meteorology:**
- `temperature`, `relative_humidity`, `wind_speed`, `wind_direction`, `boundary_layer_height`, `pressure`, `cloud_cover`, `solar_radiation`, `visibility`, `dew_point`, `stability_index`, ...

**Precipitation (extended):**
- `precipitation_occurrence`, `precipitation_intensity_mmph`, `accumulated_precipitation_mm`, `precipitation_duration_hours`, `precipitation` (legacy).

**Processes/Phenomena:**
- `inversion`, `dispersion`, `atmospheric_stability`, `wet_deposition`, `dry_deposition`, `chemical_reaction`, `photochemistry`, `aqueous_phase_reaction`, `heterogeneous_reaction`, `sia_formation`, `soa_formation`, `sulfate_formation`, `nitrate_formation`, `ammonium_nitrate_formation`, `aerosol_liquid_water`, `transport`, `regional_transport`, `long_range_transport`, `cold_surge`, ...

**Emission Sources:**
- `traffic`, `industry`, `biomass_burning`, `construction`, `power_plants`, `residential_heating`, ...

**Static Factors:**
- `population_density`, `urban_density`, `urban_land_use`, `vegetation`, `topography`, `valley_bottom`, `topographic_wetness_index`, `distance_to_roads`, `industrial_zones`, ...

**Temporal/Seasonal:**
- `season_winter`, `season_summer`, `season_dry`, `season_wet`, `time_of_day_night`, `time_of_day_morning`, `time_of_day_afternoon`, `time_of_day_evening`, `time_of_day_rush_hour`, `month_harvest`, `holiday_period`, `weekday`, `weekend`, ...

**Event Patterns:**
- `cold_surge_onset`, `cold_surge_persistence`, `cold_surge_decay`, `northeast_monsoon`, `el_nino`, ...

### Bước 3: Tạo mapping original → canonical
Với mỗi node trong `all_nodes`:

1. **Nếu đã là canonical** (theo taxonomy trên):
   - `canonical_node = original_node`.
   - Không cần mapping.

2. **Nếu là synonym/variant**:
   - Map sang canonical gần nhất:
     - `"humidity"` → `"relative_humidity"`
     - `"traffic_emissions"` → `"traffic"`
     - `"pbl"` → `"boundary_layer_height"`
     - `"pm2.5"` → `"pm25"`
     - `"cold surge onset"` → `"cold_surge_onset"`
     - ...
   - Ghi chú lý do mapping vào `metadata.node_mapping_reason` (optional).

3. **Nếu không có canonical tương ứng**:
   - Giữ nguyên `original_node`.
   - Đánh dấu `metadata.needs_canonical_review = true`.
   - Có thể đề xuất canonical name mới (nhưng phải tuân theo naming rules).

### Output
Một file JSON `node_mapping.json` với cấu trúc:
```json
{
  "mappings": [
    {
      "original_node": "humidity",
      "canonical_node": "relative_humidity",
      "reason": "Standard abbreviation for relative humidity in atmospheric science"
    },
    ...
  ],
  "canonical_nodes": [
    {
      "node": "relative_humidity",
      "category": "meteorology",
      "description": "...",
      "aliases": ["humidity", "rh", "relative humidity"]
    },
    ...
  ]
}
```

---

## TASK 3: APPLY NODE MAPPING TO RELATIONSHIPS

### Yêu cầu
Áp dụng mapping từ Task 2 vào `merged_knowledge_graph_v2.json`:

1. **Với mỗi relationship**:
   - Thêm `canonical_cause_node` (map từ `cause_node`).
   - Thêm `canonical_effect_node` (map từ `effect_node`).
   - Nếu có `intermediate_nodes`, thêm `canonical_intermediate_nodes` (map từng node).
   - **GIỮ NGUYÊN** `cause_node`, `effect_node`, `intermediate_nodes` (không xoá).

2. **Metadata**:
   - Thêm `metadata.node_normalized = true` vào relationship.
   - Có thể thêm `metadata.node_mapping_reason` nếu mapping không rõ ràng.

### Output
File `merged_knowledge_graph_v2.json` được cập nhật với:
- `canonical_*_node` fields trong mỗi relationship.
- `original_*_node` vẫn còn (để trace).

---

## TASK 4: GENERATE NODE DESCRIPTIONS

### Mục tiêu
Sinh mô tả ngắn (1–2 câu) cho mỗi canonical node để:
- Hiển thị trong UI.
- Dùng làm context cho embedding/retrieval.
- Giúp LLM hiểu semantic của node khi generate câu trả lời.

### Quy trình
Với mỗi canonical node:

1. **Thu thập context**:
   - Đọc một vài relationships tiêu biểu có node này (làm cause/effect/intermediate).
   - Xem `mechanism`, `notes`, `source_quote` liên quan.
   - Tham khảo `VARIABLES_CHECKLIST.md` nếu có.

2. **Sinh description**:
   - 1–2 câu ngắn gọn, rõ ràng.
   - Tiếng Anh (hoặc tiếng Việt nếu bạn muốn, nhưng khuyến khích tiếng Anh cho consistency).
   - Bao gồm:
     - Định nghĩa cơ bản của node.
     - Vai trò trong ô nhiễm không khí (nếu liên quan).
     - Đơn vị đo (nếu là biến số).

3. **Ví dụ**:
   ```json
   {
     "node": "relative_humidity",
     "description": "Fraction of water vapor in air relative to saturation, expressed as percentage. High RH (>75%) promotes aqueous-phase reactions and secondary aerosol formation, particularly sulfate and nitrate.",
     "category": "meteorology",
     "unit": "%",
     "typical_range": "0-100"
   }
   ```

### Output
Một file JSON `node_metadata.json` hoặc một section `nodes` trong `merged_knowledge_graph_v2.json`:
```json
{
  "nodes": [
    {
      "node": "relative_humidity",
      "canonical": true,
      "description": "...",
      "category": "meteorology",
      "unit": "%",
      "aliases": ["humidity", "rh"]
    },
    ...
  ]
}
```

---

## TASK 5: DESIGN RETRIEVAL/EMBEDDING STRUCTURE

### Mục tiêu
Thiết kế cấu trúc metadata để hỗ trợ hybrid retrieval (graph filter + embedding).

### Unit indexing cho embedding
Mỗi relationship nên có một "document" để embed, gồm:

1. **Core fields** (luôn có):
   - `id`, `category`, `canonical_cause_node`, `canonical_effect_node`.
   - `mechanism` (full text).
   - `notes` (nếu có).

2. **Conditions summary** (stringified):
   - Tóm tắt các conditions quan trọng dạng text:
     - `"RH > 85%, precipitation_intensity_mmph < 2 mm/h, season = spring"`
   - Chỉ include conditions `checkable = true` và có field/operator/value rõ ràng.

3. **Source context**:
   - `source_quote` (nếu có).
   - `source_title`, `source_year` (để reference).

4. **Metadata tags**:
   - `seasonal_variation`, `spatial_scope`.
   - `piecewise_group` (nếu có).
   - `needs_review` (nếu có).

### Yêu cầu
Thêm vào mỗi relationship một field `embedding_context` (hoặc tương tự) chứa:
```json
{
  "embedding_context": {
    "summary": "Short 1-2 sentence summary of the relationship",
    "conditions_text": "RH > 85%, precipitation_intensity_mmph < 2 mm/h, season = spring",
    "key_mechanism": "Main mechanism explanation",
    "tags": ["precipitation_paradox", "spring", "high_humidity"]
  }
}
```

Hoặc bạn có thể để backend tự generate `embedding_context` từ các fields sẵn có, nhưng nếu Manus có thể pre-compute thì tốt hơn.

---

## OUTPUT FORMAT

Sau khi hoàn thành tất cả tasks, bạn phải xuất ra:

1. **File chính**: `merged_knowledge_graph_v2.json` (đã được cập nhật)
   - Có thêm `canonical_*_node` trong mỗi relationship.
   - Các issues `checkable_empty_field` đã được sửa.
   - Có thể có thêm section `nodes` ở top-level (nếu bạn chọn cách này thay vì file riêng).

2. **File mapping** (optional, nếu tách riêng): `node_mapping.json`
   - Chứa mapping `original → canonical`.
   - Chứa metadata cho mỗi canonical node (description, category, aliases).

3. **File node metadata** (optional, nếu tách riêng): `node_metadata.json`
   - Chứa descriptions cho tất cả canonical nodes.

Hoặc bạn có thể gộp tất cả vào `merged_knowledge_graph_v2.json` với cấu trúc:
```json
{
  "schema_version": "canonical_v2",
  "categories": [...],
  "source_count": ...,
  "relationship_count_raw": ...,
  "relationship_count_valid": ...,
  "bibliography": [...],
  "nodes": [
    {
      "node": "relative_humidity",
      "canonical": true,
      "description": "...",
      "category": "meteorology",
      "aliases": [...]
    },
    ...
  ],
  "relationships": [
    {
      "id": "...",
      "category": "...",
      "cause_node": "humidity",  // original
      "canonical_cause_node": "relative_humidity",  // canonical
      "effect_node": "pm25",
      "canonical_effect_node": "pm25",
      "conditions": [...],  // unchanged from Phase 1
      "metadata": {
        "node_normalized": true,
        "file_origin": "...",
        "embedding_context": {...}  // optional
      }
    },
    ...
  ]
}
```

---

## QA RULES SAU KHI HOÀN THÀNH

Trước khi kết thúc, đảm bảo:

1. **Không còn `checkable_empty_field`**:
   - Mọi condition `checkable = true` phải có `field` không rỗng.

2. **Node mapping consistency**:
   - Mọi `canonical_*_node` đều tồn tại trong taxonomy canonical.
   - Không có node nào bị mất (mọi `original_*_node` vẫn còn, chỉ thêm canonical).

3. **Descriptions đầy đủ**:
   - Mọi canonical node đều có `description` (ít nhất 1 câu).

4. **Conditions không bị thay đổi**:
   - Spot-check một vài relationships: `conditions` phải giống hệt Phase 1 (trừ các cases đã sửa `checkable_empty_field`).

---

## FINAL TASK

1. Đọc `merged_knowledge_graph_v2.json` (từ Phase 1).
2. Sửa 7 issues `checkable_empty_field`.
3. Xây taxonomy canonical nodes và mapping `original → canonical`.
4. Áp dụng mapping vào tất cả relationships (thêm `canonical_*_node`, giữ `original_*_node`).
5. Sinh descriptions cho canonical nodes.
6. (Optional) Thêm `embedding_context` metadata cho retrieval.
7. Xuất file(s) kết quả với cấu trúc đã định nghĩa ở trên.

Hãy hành xử như một nhà khoa học và data engineer cẩn trọng: ưu tiên **consistency** và **traceability**, không làm mất thông tin gốc, và đảm bảo mọi thay đổi đều có lý do rõ ràng.
