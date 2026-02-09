# PROMPT 07: Edge Cases và Exceptions trong PM2.5

## Tổng quan

Tài liệu này tóm tắt các **edge cases** (trường hợp ngoại lệ), **non-linear relationships** (quan hệ phi tuyến), và **measurement artifacts** (sai số đo lường) đã được trích xuất từ các nguồn khoa học đáng tin cậy. Các trường hợp này phá vỡ các quy tắc chung thường được áp dụng trong việc dự đoán nồng độ PM2.5.

---

## 1. Quan hệ phi tuyến giữa Độ ẩm và PM2.5 (Inverted U-shaped)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | humidity_pm25_nonlinear_001 |
| **Loại** | Non-linear relationship |
| **Ngưỡng đảo ngược** | RH ≈ 70% |
| **Nguồn** | Lou et al. (2017), Environmental Monitoring and Assessment |

**Cơ chế:** Ở độ ẩm thấp đến trung bình (RH < 70%), độ ẩm thúc đẩy các phản ứng hóa học thứ cấp, làm tăng PM2.5. Tuy nhiên, ở độ ẩm rất cao (RH > 70%), quá trình lắng đọng ướt chiếm ưu thế, làm giảm PM2.5.

**Trích dẫn:**
> "Our results revealed that RH had an inverted U-shaped relationship with PM2.5 concentrations (peaking at RH = 45–70%)..."

---

## 2. Mưa phùn làm tăng PM2.5 (Drizzle Exception)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | drizzle_pm25_increase_001 |
| **Loại** | Exception |
| **Điều kiện** | Mưa phùn (drizzle), cường độ thấp |
| **Nguồn** | Zheng et al. (2019), Atmospheric Pollution Research |

**Cơ chế:** Mưa phùn có hiệu ứng loại bỏ âm (negative removal effect). Các giọt mưa nhỏ không đủ lớn để gây ra lắng đọng hiệu quả, thay vào đó làm tăng độ ẩm gần bề mặt, thúc đẩy sự phát triển hút ẩm của hạt.

**Trích dẫn:**
> "The removal effect of drizzle on PM2.5 and PM10 was negative, and the removal effect of moderate rain and heavy rain was significantly higher than that of light rain."

---

## 3. Đỉnh PM2.5 bị trì hoãn sau đợt không khí lạnh (Cold Surge Delayed Peak)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | cold_surge_delayed_peak_001 |
| **Loại** | Non-linear relationship (Delayed effect) |
| **Độ trễ** | 2-5 ngày |
| **Nguồn** | Ly et al. (2018), Aerosol and Air Quality Research |

**Cơ chế:** Đợt không khí lạnh ban đầu làm sạch không khí. Tuy nhiên, sau khi đi qua, khối không khí lạnh còn sót lại tạo ra lớp nghịch nhiệt ổn định, bẫy các chất ô nhiễm phát thải sau đó, dẫn đến đỉnh PM2.5 mới sau vài ngày.

**Trích dẫn:**
> "Large increases in both PM2.5 and CO were frequently observed several days after cold surges... High hourly levels of PM2.5 (higher than 120 μg m⁻³) appeared at the fourth day after the cold surge."

---

## 4. Gió mạnh vận chuyển ô nhiễm (Wind Transport Exception)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | wind_transport_increase_001 |
| **Loại** | Exception |
| **Điều kiện** | Gió từ khu vực nguồn ô nhiễm, điều kiện ô nhiễm |
| **Nguồn** | Sun et al. (2022), Remote Sensing |

**Cơ chế:** Trong điều kiện ô nhiễm, gió mạnh có thể vận chuyển PM2.5 từ khu vực nguồn ô nhiễm đến khu vực tiếp nhận, làm tăng nồng độ tại địa phương thay vì làm phân tán.

**Trích dẫn:**
> "The correlation between wind speed and PM2.5 was negative for clean conditions and positive for polluted conditions in both two sites."

---

## 5. Sai số đo lường do phát triển hút ẩm (Hygroscopic Growth Artifact)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | measurement_artifact_hygroscopic_growth_001 |
| **Loại** | Measurement Artifact |
| **Điều kiện** | Cảm biến quang học, RH cao |
| **Nguồn** | Won et al. (2021), Scientific Reports |

**Cơ chế:** Cảm biến PM2.5 dựa trên tán xạ ánh sáng không có chức năng kiểm soát độ ẩm. Ở RH cao, các hạt hút ẩm tăng kích thước, tán xạ nhiều ánh sáng hơn, khiến cảm biến đánh giá quá cao nồng độ khối lượng.

**Trích dẫn:**
> "An important reason for the lower accuracies is that low-cost sensors lack the RH and temperature control functions; therefore, light scattering sensors overestimate the PM concentration affected by humidity."

---

## 6. Khói quang hóa làm tăng PM2.5 (Photochemical Smog Spike)

| Thuộc tính | Giá trị |
|------------|---------|
| **ID** | photochemical_smog_spike_001 |
| **Loại** | Exception |
| **Điều kiện** | Nắng mạnh, nhiệt độ cao, nhiều tiền chất |
| **Nguồn** | Wang et al. (2020), Journal of Geophysical Research: Atmospheres |

**Cơ chế:** Bức xạ mặt trời mạnh thúc đẩy các phản ứng quang hóa giữa NOx và VOCs, tạo ra aerosol hữu cơ thứ cấp (SOA) và aerosol vô cơ thứ cấp, gây ra các đợt ô nhiễm PM2.5 đột ngột.

**Trích dẫn:**
> "This study focuses on a pollution episode of PM2.5 that occurred simultaneously with an O3 episode in Shanghai in the summer of 2013... SOC accounted for 48.7% of OC on average, indicating that secondary formation was the main source of OC."

---

## Tài liệu tham khảo

1. Lou, C., et al. (2017). Relationships of relative humidity with PM2.5 and PM10 in the Yangtze River Delta, China. *Environmental Monitoring and Assessment*, 189, 582. https://doi.org/10.1007/s10661-017-6281-z

2. Zheng, Z., et al. (2019). Effect of precipitation on reducing atmospheric pollutant over Beijing. *Atmospheric Pollution Research*, 10(5), 1443-1453. https://doi.org/10.1016/j.apr.2019.04.001

3. Ly, B.T., et al. (2018). Characterizing PM2.5 in Hanoi with New High Temporal Resolution Sensor. *Aerosol and Air Quality Research*, 18, 2487-2497. https://doi.org/10.4209/aaqr.2017.10.0435

4. Liu, Q., et al. (2022). Rapid reappearance of air pollution after cold air outbreaks in northern and eastern China. *Atmospheric Chemistry and Physics*, 22, 13371-13388. https://doi.org/10.5194/acp-22-13371-2022

5. Sun, X., et al. (2022). Effect of Vertical Wind Shear on PM2.5 Changes over a Receptor Region in Central China. *Remote Sensing*, 14(14), 3333. https://doi.org/10.3390/rs14143333

6. Won, W.S., et al. (2021). Hygroscopic properties of particulate matter and effects of their interactions with weather on visibility. *Scientific Reports*, 11, 16401. https://doi.org/10.1038/s41598-021-95834-6

7. Wang, H., et al. (2020). Estimation of Secondary Organic Aerosol Formation During a Photochemical Smog Episode in Shanghai, China. *Journal of Geophysical Research: Atmospheres*, 125(7), e2019JD032033. https://doi.org/10.1029/2019JD032033
