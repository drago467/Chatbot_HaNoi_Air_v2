# Kế hoạch dữ liệu theo giờ (tối thiểu) để phục vụ diễn giải cơ chế

## 1) Nguyên tắc
- Mục tiêu không phải “dự báo theo giờ”, mà là **kiểm tra điều kiện (conditions)** để chọn causal chain phù hợp.
- Ưu tiên **biến dễ lấy, cập nhật theo giờ**, có API ổn định, và có ý nghĩa vật lý.
- Chấp nhận dùng **proxy** khi không có biến lý tưởng (ví dụ inversion).

## 2) Tối thiểu cần có (Phase 1)

### 2.1. Air quality (theo giờ)
- `pm25` (bắt buộc) – từ HanoiAir / trạm quan trắc (nếu có)

### 2.2. Meteorology (theo giờ)
Ưu tiên (gần như bắt buộc để giải thích):
- `temperature` (2m)
- `relative_humidity` (hoặc `dew_point` + `temperature` để suy ra)
- `wind_speed`
- `wind_direction`
- `precipitation` (mưa)

Khuyến nghị (tăng chất lượng diễn giải):
- `cloud_cover` (proxy ổn định khí quyển/điều kiện bức xạ ban đêm)
- `surface_pressure` (proxy synoptic/áp cao)
- `solar_radiation` (proxy photochemistry/ban ngày)
- `visibility`/`fog` (nếu có nguồn phù hợp)

### 2.3. “Hard variables” (nếu có)
- `pblh` (Planetary Boundary Layer Height): nếu nguồn có (reanalysis/forecast), cực hữu ích.
  - Nếu không có: dùng proxy `wind_speed` + `cloud_cover` + `temperature` theo chu kỳ ngày/đêm.

## 3) Biến hoá học / phát thải / biến tĩnh: xử lý theo chiến lược “không làm quá tay”

### 3.1. Biến hoá học (SIA/SOA)
Trong giai đoạn chưa có quan trắc hoá học theo giờ:
- Encode gián tiếp qua:
  - `relative_humidity` (ALW, aqueous chemistry)
  - `temperature` (partitioning nitrate/ammonium nitrate)
  - season/time-of-day (mùa đông/đêm)
- Trong câu trả lời: diễn giải “cơ chế có thể mạnh khi …”, và ghi `uncertainties` nếu thiếu kiểm chứng.

### 3.2. Biến phát thải
Chưa cần phát thải theo giờ dạng inventory. Dùng proxy:
- Traffic proxy: giờ cao điểm (time-of-day) + road proximity (static) + weekday/weekend
- Biomass burning: mùa vụ + FIRMS hotspots (theo ngày) + hướng gió (transport)
- Industrial: static zones + wind direction (upwind exposure)

### 3.3. Biến tĩnh (offline)
Xử lý offline và lưu theo “địa điểm” (phường/quận hoặc grid):
- `population_density`
- `distance_to_major_roads` / road density
- `industrial_zone_proximity`
- `lulc_*` (đất xây dựng/vegetation/water)
- `dem_topography` (elevation/slope/valley/basin proxy)

Vai trò trong reasoning:
- coi như **moderator**: làm tăng/giảm nguy cơ nền hoặc làm mạnh/yếu một causal chain.

## 4) Schema gợi ý cho “snapshot theo giờ”

Một bản ghi (record) tối thiểu:
- `timestamp_utc`
- `location_id` (phường/quận hoặc lat/lon)
- `pm25`
- `temperature`
- `relative_humidity`
- `wind_speed`
- `wind_direction`
- `precipitation`
- (optional) `pblh`, `cloud_cover`, `surface_pressure`, `solar_radiation`

## 5) Mapping conditions trong CKG → kiểm tra được từ snapshot

Ví dụ mapping:
- `"RH > 75%"` → `relative_humidity > 75`
- `"Gió yếu"` → `wind_speed < 3`
- `"Mùa đông"` → month ∈ [10..3] hoặc tag `season=winter`
- `"Có mưa"` → `precipitation > 0`
- `"PBLH thấp"` → `pblh < 300` (nếu có) hoặc proxy theo rule

Nếu không kiểm tra được:
- không loại bỏ cơ chế; ghi vào `uncertainties` và trình bày như điều kiện “thường gặp”.

## 6) Chiến lược triển khai tối ưu cho khoá luận
- Phase 1: chỉ cần meteorology core + pm25 theo giờ là đủ để demo “condition-aware explanation”.
- Phase 2: thêm static offline để cá nhân hoá theo khu vực (tăng tính thực tiễn).
- Phase 3: nếu còn thời gian, thêm `pblh` (hoặc proxy tốt hơn) để nâng độ “chắc” của diễn giải nghịch nhiệt/tầng biên.

