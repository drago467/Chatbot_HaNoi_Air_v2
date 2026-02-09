# CKG Gaps & Hướng Bổ Sung (từ phân tích `data/ckg_stats.json`)

## 1) Tóm tắt cấu trúc hiện tại

- **Số relationships (valid)**: 105  
- **Số nodes**: 99  
- **PM2.5**: in-degree = 68, out-degree = 0 (graph tập trung vào **nguyên nhân → PM2.5**, đúng với mục tiêu “giải thích cơ chế”)
- **Phân bố theo category**:
  - `seasonal_patterns`: 35
  - `transport_mechanisms`: 18
  - `emission_sources`: 17
  - `meteorological_pathways`: 13
  - `chemical_processes`: 10
  - `static_factors`: 6
  - `edge_cases`: 6

## 2) Nhận xét “gaps” quan trọng (ưu tiên theo giá trị cho giải thích cơ chế)

### 2.1. Gaps về “chuỗi cơ chế” (causal chains dài 2–4 bước)
Hiện tại nhiều đường đi tới `pm25` vẫn là **1 bước** (node → `pm25`) thay vì chuỗi cơ chế, ví dụ:
- `cold_surge_onset → pm25` (thiếu mắt xích: gió mùa/trajectory → vận chuyển xa → thay đổi thành phần/SIA → PM2.5)
- `precipitation → pm25` (thiếu mắt xích: scavenging/wet_deposition → giảm PM2.5; hoặc mưa nhẹ + ẩm cao → tăng ALW/SIA trong một số bối cảnh)

**Giá trị bổ sung**: thêm edges trung gian giúp chatbot giải thích “vì sao” rõ ràng hơn, thay vì chỉ kết luận.

### 2.2. Gaps về điều kiện áp dụng (conditions) gắn với biến đo được
Nhiều relationships có `conditions` theo mô tả (mùa/đêm/trời quang) nhưng chưa “liên kết” trực tiếp với các biến có thể lấy theo giờ (hoặc theo ngày), ví dụ:
- `inversion` thường cần proxy từ: nhiệt độ mặt đất/gradient nhiệt/độ mây/gió (nếu không có sounding)
- `stagnation` cần proxy: gió thấp + PBLH thấp + áp cao

**Giá trị bổ sung**: chuẩn hoá conditions thành các rule kiểm tra được (ví dụ `wind_speed < 3 m/s`, `relative_humidity > 75%`, `pblh < 300 m`).

### 2.3. Gaps về biến khí tượng “core”
Tập biến khí tượng core đang có nhưng chưa phủ đều về edges:
- Đã có mạnh: `relative_humidity`, `pblh`, `wind_speed`, `precipitation`, `temperature`, `pressure`
- Cần củng cố: `wind_direction` (hướng gió + hướng tới nguồn phát thải/biên giới), `solar_radiation` (photochemistry), `cloud_cover` (ổn định khí quyển), `visibility/fog` (ALW/measurement artifacts)

### 2.4. Gaps về hoá học (SIA/SOA) gắn với bối cảnh Hà Nội
Đã có một số đường hoá học (ALW, sulfate/nitrate), nhưng còn thiếu “tầng liên kết”:
- `NH3` (nguồn nông nghiệp/đô thị) → `aerosol_pH` → sulfate formation
- `temperature` + `relative_humidity` → partitioning nitrate/ammonium nitrate → PM2.5 (đặc biệt mùa đông)

### 2.5. Gaps về biến tĩnh (static) & cách dùng trong chatbot
`static_factors` hiện có 6 relationships, nhưng chatbot giải thích cần “vai trò” của biến tĩnh:
- Biến tĩnh không đổi theo giờ → dùng để **giải thích nền** (baseline risk) theo khu vực/phường: gần đường lớn, mật độ dân số, khu công nghiệp, địa hình trũng…
- Cần mô hình hoá: static factor như **moderator** (điều biến) hơn là direct cause trong một số trường hợp.

## 3) Đề xuất bổ sung theo “đúng mục tiêu khoá luận”

### 3.1. Bổ sung tri thức mục tiêu (không crawl lan man)
- **Ưu tiên 1 (khí tượng + vận chuyển)**: cold surge / monsoon / synoptic patterns → transport → stagnation → PM2.5
- **Ưu tiên 2 (hoá học mùa đông)**: RH/ALW/pH/NH3/NO2/SO2 → SIA → PM2.5
- **Ưu tiên 3 (mưa & wet scavenging)**: intensity threshold → scavenging efficiency → PM2.5 reduction

### 3.2. Chuẩn hoá node taxonomy
Danh sách node hiện có “other” khá lớn, chủ yếu do tên node quá cụ thể (dài). Nên chuẩn hoá về các node “concept” chung + notes mô tả chi tiết, ví dụ:
- `upper_level_ridge_low_pressure_system` → `synoptic_forcing` (notes: ridge/low-pressure pattern)
- `wind_direction_relative_to_emission_sources` → `wind_direction` + `upwind_emission_exposure`

## 4) Output liên quan
- `causal/causal_knowledge/data/merged_knowledge_graph.json`: canonical graph
- `causal/causal_knowledge/data/ckg_stats.json`: thống kê + sample paths để làm "bản đồ gaps"

