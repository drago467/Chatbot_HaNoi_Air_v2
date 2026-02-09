# Báo cáo Trích xuất Mối quan hệ Nhân quả: Yếu tố Tĩnh và PM2.5

## Tổng quan

Báo cáo này trình bày kết quả trích xuất các mối quan hệ nhân quả (causal relationships) giữa các yếu tố tĩnh (static factors) và nồng độ PM2.5, được thực hiện theo phương pháp nghiên cứu có hệ thống từ các nguồn khoa học Tier-1 (peer-reviewed journals).

## Phương pháp

Quá trình trích xuất tuân thủ nghiêm ngặt các quy tắc anti-hallucination, bao gồm việc chỉ sử dụng thông tin từ các nguồn Tier-1 đã được xác minh, trích dẫn nguyên văn (verbatim quotes) từ các bài báo gốc, và ghi nhận đầy đủ DOI cho mỗi nguồn tham khảo.

## Tóm tắt các Mối quan hệ Nhân quả

Tổng cộng **5 mối quan hệ nhân quả** đã được trích xuất từ **8 nguồn Tier-1**, được tổng hợp trong bảng dưới đây:

| Factor 1 | Factor 2 | Relationship | Direction | Strength | Confidence |
|----------|----------|--------------|-----------|----------|------------|
| dem_topography_valley_basin | pm25 | MODERATOR | - | STRONG | HIGH |
| lulc_vegetation | pm25 | INDIRECT_CAUSE | decrease | MODERATE | HIGH |
| population_density | pm25 | INDIRECT_CAUSE | increase | MODERATE | HIGH |
| road_network_proximity | pm25 | INDIRECT_CAUSE | increase | STRONG | HIGH |
| industrial_zones_proximity | pm25 | INDIRECT_CAUSE | increase | STRONG | HIGH |

## Chi tiết các Mối quan hệ

### 1. Địa hình thung lũng/bồn địa (dem_topography_valley_basin) → PM2.5

**Loại quan hệ**: MODERATOR (yếu tố điều tiết)

Địa hình thung lũng hoặc bồn địa tạo điều kiện hình thành các lớp không khí lạnh ổn định (cold-air pools - CAPs), đặc biệt trong mùa đông dưới hệ thống áp suất cao. Các lớp khí quyển ổn định này ngăn chặn sự trộn lẫn theo chiều dọc và giữ chất ô nhiễm, dẫn đến tích tụ PM2.5 gần bề mặt.

> "Because vertical mixing of pollutants is suppressed in the stable atmospheric layers, PM2.5 aerosols emitted into the CAP or produced there through chemical and photochemical processes lead to high levels of PM2.5." [1]

Nghiên cứu tại Salt Lake Valley cho thấy nồng độ PM2.5 giảm tới 30% khi độ cao tăng từ 1300m lên 1600m trong thung lũng, và tốc độ tích tụ đạt khoảng 6 μg/m³/ngày trong các sự kiện CAP kéo dài nhiều ngày.

### 2. Thảm thực vật (lulc_vegetation) → PM2.5

**Loại quan hệ**: INDIRECT_CAUSE (nguyên nhân gián tiếp - giảm PM2.5)

Thảm thực vật, đặc biệt là rừng, loại bỏ PM2.5 khỏi khí quyển thông qua quá trình lắng đọng khô (dry deposition). Các hạt bụi được bắt giữ trên bề mặt lá thông qua các cơ chế chặn, va đập và lắng đọng. Cấu trúc phức tạp của tán rừng cũng tăng cường nhiễu loạn không khí, có thể làm tăng tốc độ lắng đọng.

> "The deposition velocity onto the forest canopy was higher than which onto the wetland and the water surface and the velocity varied in different seasons." [2]

Nghiên cứu tại Boston cho thấy mức độ xanh hóa xung quanh (greenness) có mối liên hệ nghịch đáng kể với PM2.5 liên quan đến giao thông trong nhà, với hệ số tương quan -0.068 đến -0.101 tùy thuộc vào bán kính buffer.

### 3. Mật độ dân số (population_density) → PM2.5

**Loại quan hệ**: INDIRECT_CAUSE (nguyên nhân gián tiếp - tăng PM2.5)

Mật độ dân số cao dẫn đến tăng PM2.5 thông qua hai cơ chế chính: "hiệu ứng tắc nghẽn" (congestion effect) - nhiều phương tiện giao thông dẫn đến tốc độ thấp hơn và đốt cháy kém hiệu quả hơn; và "hiệu ứng tập trung ô nhiễm" (pollution centralization effect) - mật độ cao hơn của các nguồn phát thải như phương tiện và sưởi ấm dân dụng. Ngoài ra, các hình thái đô thị dày đặc với mật độ tòa nhà cao có thể làm giảm tốc độ gió và cản trở sự phân tán ô nhiễm.

> "The results suggest that population density is positively associated with PM2.5 concentrations, pointing to pollution centralization and congestion effects dominating the mitigating effects of mode-shifting associated with density." [3]

### 4. Khoảng cách đến mạng lưới đường (road_network_proximity) → PM2.5

**Loại quan hệ**: INDIRECT_CAUSE (nguyên nhân gián tiếp - tăng PM2.5)

Mạng lưới đường là nguồn phát thải PM2.5 chính từ khí thải xe cộ và các nguồn không phải khí thải (mài mòn phanh, mài mòn lốp, bụi đường). Nồng độ cao nhất gần đường và giảm theo khoảng cách, tuân theo mô hình suy giảm theo khoảng cách (distance-decay pattern).

> "Incremental PM2.5 decreased 75% between 5 m and 30 m from the roadway." [5]

Nghiên cứu cho thấy các trường học cách đường cao tốc hơn 3 km có mức PM2.5 liên quan đến giao thông thấp hơn 63% so với các trường gần đường.

### 5. Khoảng cách đến khu công nghiệp (industrial_zones_proximity) → PM2.5

**Loại quan hệ**: INDIRECT_CAUSE (nguyên nhân gián tiếp - tăng PM2.5)

Các khu công nghiệp chứa mật độ cao các nhà máy và quy trình công nghiệp là nguồn điểm chính của PM2.5 và các tiền chất của nó. Phát thải từ ống khói và phát thải phân tán dẫn đến nồng độ PM2.5 tăng cao đáng kể trong và xung quanh các khu vực này.

> "The spatial agglomeration of high-pollution factories in China aggravated PM2.5 pollution... The industrial sector accounts for roughly 30% of total PM2.5 pollution in China, and more than 90% of the industrial sector pollution comes from high-pollution industries." [7]

## Nguồn tham khảo

[1] Silcox, G. D., Kelly, K. E., Crosman, E. T., Whiteman, C. D., & Allen, B. L. (2012). Wintertime PM2.5 concentrations during persistent, multi-day cold-air pools in a mountain valley. *Atmospheric Environment*, 46, 17-24. https://doi.org/10.1016/j.atmosenv.2011.10.041

[2] Liu, J., Zhu, L., Wang, H., Yang, Y., Liu, J., Qiu, D., ... & Liu, J. (2016). Dry deposition of particulate matter at an urban forest, wetland and lake surface in Beijing. *Atmospheric Environment*, 125, 178-187. https://doi.org/10.1016/j.atmosenv.2015.11.023

[3] Han, S., & Sun, B. (2019). Impact of Population Density on PM2.5 Concentrations: A Case Study in Shanghai, China. *Sustainability*, 11(7), 1968. https://doi.org/10.3390/su11071968

[4] Hien, P. D., Men, N. T., Tan, P. M., & Hangartner, M. (2020). Impact of urban expansion on the air pollution landscape: A case study of Hanoi, Vietnam. *Science of The Total Environment*, 702, 134635. https://doi.org/10.1016/j.scitotenv.2019.134635

[5] Mukherjee, A., McCarthy, M. C., Brown, S. G., & Hiler, D. (2020). Influence of roadway emissions on near-road PM2.5: Monitoring data analysis and implications. *Transportation Research Part D: Transport and Environment*, 86, 102481. https://doi.org/10.1016/j.trd.2020.102481

[6] Han, L., Zhao, J., Gao, Y., Gu, Z., Xin, K., & Zhang, J. (2020). Spatial distribution characteristics of PM2.5 and PM10 in Xi'an City predicted by land use regression models. *Sustainable Cities and Society*, 61, 102329. https://doi.org/10.1016/j.scs.2020.102329

[7] Zheng, Y., Xu, W., Huang, J., & Lv, A. (2022). Spatial agglomeration of high-pollution factories and PM2.5 pollution: Evidence from prefecture-level cities in China from 1998 to 2013. *Journal of Cleaner Production*, 366, 132904. https://doi.org/10.1016/j.jclepro.2022.132904

[8] Matthaios, V. N., Holland, I., Kang, C. M., Hart, J. E., Hauptman, M., Wolfson, J. M., ... & Koutrakis, P. (2024). The effects of urban green space and road proximity to indoor traffic-related PM2.5, NO2, and BC exposure in inner-city schools. *Journal of Exposure Science & Environmental Epidemiology*, 34(5), 745-752. https://doi.org/10.1038/s41370-024-00669-8

---
*Báo cáo được tạo bởi Manus AI*
*Ngày: 23/01/2026*
