# Báo cáo Tổng hợp: Nguồn Phát thải PM2.5 tại Hà Nội

## Tổng quan

Báo cáo này tổng hợp các causal relationships về nguồn phát thải (emission sources) ảnh hưởng đến nồng độ PM2.5 tại Hà Nội, Việt Nam. Nghiên cứu được thực hiện theo đúng quy tắc và format được định nghĩa trong system prompt, với trọng tâm vào việc extract các mối quan hệ nhân quả có cơ chế rõ ràng và bằng chứng khoa học đầy đủ.

## Nguồn tài liệu

Nghiên cứu sử dụng **7 nguồn tài liệu**, trong đó có **6 nguồn Tier-1** (peer-reviewed journals) và **1 nguồn Tier-2** (World Bank technical report). Các nguồn chính bao gồm các nghiên cứu source apportionment sử dụng PMF, PCA, và các phương pháp phân tích hóa học tiên tiến.

| Nguồn | Năm | Tier | Phương pháp chính |
|-------|-----|------|-------------------|
| Dominutti et al. | 2024 | Tier-1 | PMF + ACSM |
| Nguyen et al. (COVID-19) | 2021 | Tier-1 | Before/After analysis |
| Pham et al. (Rice straw) | 2021 | Tier-1 | Emission factors |
| Bui et al. | 2022 | Tier-1 | PCA + EF |
| Le et al. (Traffic) | 2021 | Tier-1 | Random Forest |
| Makkonen et al. | 2023 | Tier-1 | PMF |
| World Bank | 2021 | Tier-2 | GAINS model |

## Các nguồn phát thải chính

Dựa trên các nghiên cứu source apportionment, các nguồn phát thải PM2.5 chính tại Hà Nội được xác định như sau:

| Nguồn phát thải | Đóng góp PM2.5 | Pollutants chính | Đặc điểm thời gian |
|-----------------|----------------|------------------|-------------------|
| Industrial activities | 9-29% | SO2, NOx, heavy metals | Quanh năm |
| Biomass burning (đốt rơm rạ) | 19-26% | PM2.5, VOCs, CO | Mùa thu hoạch (T5-6, T9-10) |
| Road dust & construction | 17-23% | Crustal elements | Mùa khô |
| Traffic | 12-15% | NOx, CO, PM2.5 primary | Rush hour |
| Coal combustion | 10-15% | SO2, NOx | Quanh năm |
| Long-range transport | 25% (SIA) | Secondary aerosols | Quanh năm |

## Causal Relationships đã Extract

Tổng cộng **17 causal relationships** được extract, bao gồm:

### Direct Cause Relationships (14)
Các mối quan hệ nhân quả trực tiếp từ nguồn phát thải đến pollutants:

1. **Traffic → NOx**: Xe máy và ô tô phát thải NOx trực tiếp từ quá trình đốt nhiên liệu
2. **Traffic → CO**: Đốt nhiên liệu không hoàn toàn tạo CO
3. **Traffic → PM2.5 primary**: Exhaust và non-exhaust emissions
4. **Biomass burning → PM2.5**: Đốt rơm rạ với
 EF = 34.0 g/kg
5. **Biomass burning → VOCs**: Tiền chất của SOA
6. **Biomass burning → CO**: Cháy không hoàn toàn
7. **Industry → PM2.5**: Phát thải trực tiếp từ sản xuất
8. **Industry → SO2**: Đốt nhiên liệu chứa lưu huỳnh
9. **Industry → NOx**: Thermal NOx từ quá trình đốt
10. **Power plants → SO2**: Đốt than phát thải SO2
11. **Power plants → NOx**: Đốt than phát thải NOx
12. **Construction → Resuspension**: Làm bay bụi từ công trình
13. **Resuspension → PM2.5**: Bụi tái bay lên vào không khí
14. **Residential heating → PM2.5**: Đốt than/củi sinh hoạt

### Indirect Cause Relationships (3)
Các mối quan hệ gián tiếp qua precursors và secondary formation:

1. **Traffic → PM2.5** (qua NOx → nitrate)
2. **Industry → PM2.5** (qua SO2 → sulfate)
3. **Open waste burning → PM2.5** (đốt rác thải)

## Phát hiện quan trọng

### 1. Chỉ 1/3 PM2.5 từ nguồn địa phương
Theo World Bank (2021), chỉ khoảng 1/3 PM2.5 tại Hà Nội đến từ các nguồn phát thải địa phương. Phần còn lại được vận chuyển từ:
- Greater Hanoi areas
- Red River Delta Region
- Các tỉnh khác của Việt Nam
- Các nước láng giềng và vận tải quốc tế

### 2. Secondary aerosols chiếm tỷ lệ lớn
Khoảng 50% PM2.5 là secondary particulate matter, với:
- Sulfate chiếm ưu thế (từ coal combustion)
- Nitrate (từ traffic và industry)
- SOA (từ biomass burning và traffic)

### 3. COVID-19 lockdown cung cấp bằng chứng quan trọng
Trong thời gian lockdown COVID-19:
- NO2 giảm 75.8% → Traffic là nguồn chính của NOx
- CO giảm 28-41% → Traffic là nguồn chính của CO
- PM2.5 chỉ giảm 14-18% → Traffic không phải nguồn duy nhất
- SO2 giảm 60.7% → Cả traffic và industry đóng góp

### 4. Biomass burning có tính mùa vụ rõ rệt
Đốt rơm rạ đóng góp 19-26% PM2.5, với:
- Emission factor: 34.0 ± 17.6 g PM2.5/kg rơm rạ
- Phát thải hàng năm: 10.8 Gg PM2.5
- Peaks vào mùa thu hoạch (T5-6 và T9-10)

## Handoff to Other Prompts

Các chủ đề cần được xử lý bởi các prompts khác:

| Chủ đề | Prompt đề xuất |
|--------|----------------|
| NOx/SO2/VOCs → chemical reactions → SIA/SOA → PM2.5 | chemical_processes |
| Wind/PBLH/Inversion → PM2.5 dispersion | meteorological_pathways |
| Back-trajectory, regional transport | transport_mechanisms |
| Population density, land use → emissions | static_factors |

## Missing Information

Các thông tin còn thiếu cần nghiên cứu thêm:
1. Emission factors cụ thể cho traffic tại Hà Nội (g/km)
2. Đóng góp của agriculture/NH3 từ chăn nuôi và phân bón
3. Seasonal variation chi tiết của từng emission source
4. Spatial distribution trong nội thành vs ngoại thành
5. Emission inventory cập nhật sau 2020
6. Đóng góp của craft villages (làng nghề)

## Contradictions

Có sự khác biệt về tỷ lệ đóng góp giữa các nghiên cứu do:
- Phương pháp source apportionment khác nhau (PMF, PCA, GAINS)
- Thời gian và địa điểm lấy mẫu khác nhau
- Định nghĩa nguồn phát thải khác nhau

## Kết luận

Nghiên cứu đã extract được 17 causal relationships với đầy đủ bằng chứng từ 7 nguồn tài liệu chất lượng cao. Các nguồn phát thải chính tại Hà Nội bao gồm industrial activities, biomass burning, traffic, và coal combustion. Đặc biệt, regional transport đóng vai trò quan trọng với khoảng 2/3 PM2.5 đến từ các nguồn bên ngoài Hà Nội.

---
*Báo cáo được tạo theo PROMPT 04: EMISSION SOURCES với system guardrails từ PROMPT 00: SYSTEM GUARDRAILS & FOUNDATION*
