# CKG Gaps - Đánh giá Cập nhật (Sau khi merge prompts 08-13)

**Ngày đánh giá**: 2026-01-23  
**Nguồn dữ liệu**: `data/merged_knowledge_graph.json` (105 relationships, 99 nodes)  
**Script phân tích**: `scripts/analyze_ckg.py`

---

## 1. Tóm tắt cấu trúc hiện tại

### 1.1. Thống kê tổng quan
- **Số relationships (valid)**: 105
- **Số nodes**: 99
- **Số edges**: 98
- **PM2.5**: in-degree = 68, out-degree = 0 (đúng với mục tiêu "giải thích cơ chế")

### 1.2. Phân bố theo category
- `seasonal_patterns`: 35 relationships
- `transport_mechanisms`: 18 relationships
- `emission_sources`: 17 relationships
- `meteorological_pathways`: 13 relationships
- `chemical_processes`: 10 relationships
- `static_factors`: 6 relationships
- `edge_cases`: 6 relationships

### 1.3. Node coverage buckets
- `meteorology_core`: 6 nodes
- `pollutants`: 7 nodes
- `chemistry`: 8 nodes
- `emissions`: 12 nodes
- `seasonal_synoptic`: 12 nodes
- `static`: 6 nodes
- **`other`: 48 nodes** ⚠️ (chiếm ~48% tổng số nodes - cần normalize)

---

## 2. Đánh giá gaps đã được giải quyết từ prompts 08-13

### 2.1. ✅ Causal chains dài (2-4 bước) - ĐÃ CÓ MỘT PHẦN

**Chains dài hiện có**:
- ✅ `industry → so2 → sulfate_formation → sia_formation → pm25` (4 bước)
- ✅ `power_plants → so2 → sulfate_formation → sia_formation → pm25` (4 bước)
- ✅ `so2 → sulfate_formation → sia_formation → pm25` (3 bước)
- ✅ `no2 → sulfate_formation → sia_formation → pm25` (3 bước)
- ✅ `h2o2 → sulfate_formation → sia_formation → pm25` (3 bước)
- ✅ `temperature → inversion → pm25` (2 bước)
- ✅ `precipitation → wet_deposition → pm25` (2 bước)
- ✅ `solar_radiation → pblh → pm25` (2 bước)
- ✅ `nh3 → sia_formation → pm25` (2 bước)

**Chains dài CÒN THIẾU**:
- ❌ `cold_surge_onset → synoptic_pattern → transport → regional_pollution → pm25` (chưa có)
- ❌ `cold_surge → wind_direction_change → upwind_exposure → pm25` (chưa có)
- ❌ `light_precipitation + high_RH → ALW_increase → sia_formation → pm25_increase` (chưa có)
- ❌ `NH3 → aerosol_pH → sulfate_formation → pm25` (chưa có, chỉ có `nh3 → sia_formation → pm25`)

**Đánh giá**: Đã có một số chains dài cho chemical processes và meteorological pathways, nhưng **thiếu chains dài cho cold surge transport** và **precipitation mechanisms phức tạp**.

### 2.2. ⚠️ Conditions cụ thể - CHƯA ĐƯỢC CHUẨN HÓA

**Tình trạng hiện tại**:
- Nhiều relationships có `conditions` dạng text mô tả (ví dụ: "Mùa đông", "Ban đêm", "RH > 75%")
- Chưa được chuẩn hóa thành rules kiểm tra được với format structured
- Chưa có mapping rõ ràng: CKG conditions → data fields

**Ví dụ conditions hiện có** (cần normalize):
- `"RH > 75%"` → cần format: `{"type": "threshold", "field": "relative_humidity", "operator": ">", "value": 75}`
- `"Gió yếu"` → cần format: `{"type": "threshold", "field": "wind_speed", "operator": "<", "value": 3}`
- `"Mùa đông"` → cần format: `{"type": "season", "value": "winter"}`

**Đánh giá**: **Cần normalize conditions** để có thể check với data thực tế trong Phase 2.5 (Data Pipeline).

### 2.3. ⚠️ Biến khí tượng core - ĐÃ CÓ NHƯNG CHƯA ĐỦ

**Biến đã có mạnh**:
- ✅ `relative_humidity` (2 relationships)
- ✅ `pblh` (2 relationships)
- ✅ `wind_speed` (2 relationships)
- ✅ `precipitation` (2 relationships)
- ✅ `temperature` (2 relationships)
- ✅ `pressure` (1 relationship)

**Biến đã có nhưng cần củng cố**:
- ⚠️ `wind_direction`: có `wind_direction_relative_to_emission_sources` nhưng tên node dài, cần normalize
- ⚠️ `solar_radiation`: có 1 relationship (`solar_radiation → pblh → pm25`), nhưng chưa có chains về photochemistry
- ❌ `cloud_cover`: chưa có trong graph
- ❌ `visibility/fog`: có trong prompts 08-13 nhưng cần kiểm tra coverage

**Đánh giá**: Đã có một số biến core, nhưng **thiếu `cloud_cover`** và **cần củng cố chains cho `solar_radiation`** (photochemistry).

### 2.4. ⚠️ Winter chemistry chains - ĐÃ CÓ MỘT PHẦN

**Chains hiện có**:
- ✅ `nh3 → sia_formation → pm25` (2 bước)
- ✅ `temperature → inversion → pm25` (2 bước)
- ✅ `relative_humidity → sia_formation` (có trong graph)

**Chains còn thiếu**:
- ❌ `NH3 → aerosol_pH → sulfate_formation → pm25` (thiếu intermediate node `aerosol_pH`)
- ❌ `temperature + RH → NH4NO3_partitioning → pm25` (có `ammonium_nitrate_formation` nhưng chưa có chain đầy đủ)

**Đánh giá**: Đã có một số chains về winter chemistry, nhưng **thiếu intermediate nodes** (`aerosol_pH`, `NH4NO3_partitioning`) để tạo chains dài hơn.

### 2.5. ⚠️ Node taxonomy - CẦN NORMALIZE

**Vấn đề**:
- **48 nodes "other"** (chiếm ~48% tổng số nodes)
- Nhiều nodes có tên quá dài và cụ thể:
  - `wind_direction_relative_to_emission_sources` → nên normalize thành `wind_direction` + `upwind_emission_exposure`
  - `upper_level_ridge_low_pressure_system` → nên normalize thành `synoptic_forcing`
  - `cold_surge_persistence_phase` → có thể merge với `cold_surge_persistence`
  - `planetary_boundary_layer_pbl_height_variation` → có thể merge với `pblh`

**Đánh giá**: **Cần normalize node names** để giảm số lượng nodes "other" và tạo taxonomy rõ ràng hơn.

---

## 3. Gaps còn lại cần bổ sung (Ưu tiên)

### 3.1. 🔴 Ưu tiên cao: Causal chains dài cho cold surge

**Gap**: Thiếu chains dài giải thích cơ chế cold surge → PM2.5

**Chains cần bổ sung**:
1. `cold_surge_onset → synoptic_pattern → transport → regional_pollution → pm25`
2. `cold_surge → wind_direction_change → upwind_exposure → pm25`
3. `cold_surge_persistence → stagnation → local_pollution_accumulation → pm25`

**Giá trị**: Giúp chatbot giải thích rõ "Tại sao PM2.5 cao vào mùa đông?" với mechanism đầy đủ.

**Action**: Tạo prompt mới `prompt_14_cold_surge_chains.md` (nếu prompt_10 chưa cover đủ)

### 3.2. 🔴 Ưu tiên cao: Causal chains dài cho precipitation

**Gap**: Thiếu chains giải thích cơ chế phức tạp của precipitation

**Chains cần bổ sung**:
1. `light_precipitation + high_RH → ALW_increase → sia_formation → pm25_increase` (paradox: mưa nhẹ có thể tăng PM2.5)
2. `precipitation_intensity → scavenging_efficiency → pm25_reduction` (threshold effects)

**Giá trị**: Giúp chatbot giải thích "Mưa có làm giảm PM2.5 không?" với điều kiện cụ thể.

**Action**: Review `prompt_09_precipitation_wet_scavenging_gaps.md` đã cover chưa, nếu chưa thì bổ sung

### 3.3. 🟡 Ưu tiên trung bình: Biến khí tượng core còn thiếu

**Gap**: Thiếu `cloud_cover` và chains về photochemistry

**Cần bổ sung**:
1. `cloud_cover → atmospheric_stability → inversion → pm25`
2. `solar_radiation → photochemistry → SOA_formation → pm25`
3. `cloud_cover → solar_radiation → photochemistry` (moderator effect)

**Action**: Tạo prompt mới `prompt_15_meteorological_core_variables.md` nếu cần

### 3.4. 🟡 Ưu tiên trung bình: Winter chemistry chains đầy đủ

**Gap**: Thiếu intermediate nodes trong winter chemistry chains

**Cần bổ sung**:
1. `NH3 → aerosol_pH → sulfate_formation → pm25` (cần thêm node `aerosol_pH`)
2. `temperature + RH → NH4NO3_partitioning → pm25` (cần thêm node `NH4NO3_partitioning`)

**Action**: Review `prompt_08_winter_chemistry_sia_gaps.md` đã cover chưa, nếu chưa thì bổ sung

---

## 4. Đánh giá coverage hiện tại

### 4.1. Coverage cho các câu hỏi phổ biến

**Câu hỏi 1: "Tại sao PM2.5 cao vào mùa đông?"**
- ✅ Có: `cold_surge → pm25`, `winter_season → pm25`, `temperature → inversion → pm25`
- ⚠️ Thiếu: Chains dài giải thích cold surge mechanism (transport, stagnation)
- **Coverage**: ~70% (có cơ bản nhưng thiếu chi tiết)

**Câu hỏi 2: "Mưa có làm giảm PM2.5 không?"**
- ✅ Có: `precipitation → wet_deposition → pm25`
- ⚠️ Thiếu: Chains về light precipitation + high RH → increase PM2.5 (paradox)
- **Coverage**: ~60% (thiếu edge cases)

**Câu hỏi 3: "Gió mùa đông bắc ảnh hưởng thế nào?"**
- ✅ Có: `cold_surge → pm25`, `northeast_monsoon → pm25`, `wind_direction_relative_to_emission_sources → pm25`
- ⚠️ Thiếu: Chains dài về transport mechanism
- **Coverage**: ~65% (có cơ bản nhưng thiếu chi tiết)

**Câu hỏi 4: "Nếu gió mạnh hơn thì PM2.5 sẽ thế nào?"**
- ✅ Có: `wind_speed → pm25` (direct)
- ⚠️ Thiếu: Chains giải thích mechanism (dispersion, transport)
- **Coverage**: ~50% (chỉ có direct relationship)

### 4.2. Tổng kết coverage

- **Coverage tổng thể**: ~65-70%
- **Đã đủ để demo cơ bản**: ✅ Có
- **Đã đủ để giải thích chi tiết**: ⚠️ Chưa đủ (thiếu chains dài cho một số cơ chế chính)

---

## 5. Kế hoạch bổ sung để đạt "good enough"

### 5.1. Bổ sung critical gaps (20-30 relationships mới)

**Ưu tiên 1**: Cold surge chains (5-8 relationships)
- Tạo prompt `prompt_14_cold_surge_chains.md`
- Focus: synoptic patterns → transport → regional pollution

**Ưu tiên 2**: Precipitation chains (3-5 relationships)
- Review và bổ sung `prompt_09_precipitation_wet_scavenging_gaps.md`
- Focus: light precipitation paradox, intensity thresholds

**Ưu tiên 3**: Meteorological core variables (3-5 relationships)
- Tạo prompt `prompt_15_meteorological_core_variables.md`
- Focus: cloud_cover, solar_radiation photochemistry

**Ưu tiên 4**: Winter chemistry intermediate nodes (2-4 relationships)
- Review và bổ sung `prompt_08_winter_chemistry_sia_gaps.md`
- Focus: aerosol_pH, NH4NO3_partitioning

**Tổng ước tính**: 13-22 relationships mới

### 5.2. Chuẩn hóa (không cần bổ sung thêm data)

**Normalize conditions**: Chuẩn hóa ít nhất 50% relationships có conditions
**Normalize node names**: Giảm nodes "other" từ 48 xuống <30

---

## 6. Kết luận

### 6.1. Điểm mạnh
- ✅ Đã có một số chains dài cho chemical processes (3-4 bước)
- ✅ Coverage cơ bản cho các câu hỏi phổ biến (~65-70%)
- ✅ Đã có prompts 08-13 giải quyết một số gaps

### 6.2. Điểm cần cải thiện
- ⚠️ Thiếu chains dài cho cold surge transport (ưu tiên cao)
- ⚠️ Thiếu chains về precipitation paradox (ưu tiên cao)
- ⚠️ Conditions chưa được chuẩn hóa (cần normalize)
- ⚠️ Node taxonomy có nhiều "other" (cần normalize)

### 6.3. Khuyến nghị

**Để đạt "good enough"**:
1. Bổ sung 13-22 relationships mới (ưu tiên cold surge và precipitation chains)
2. Normalize conditions cho ít nhất 50% relationships
3. Normalize node names để giảm "other" nodes

**Sau khi hoàn thành**: CKG sẽ có coverage ~80-85% và sẵn sàng cho Phase 2 (Backend Core Services).
