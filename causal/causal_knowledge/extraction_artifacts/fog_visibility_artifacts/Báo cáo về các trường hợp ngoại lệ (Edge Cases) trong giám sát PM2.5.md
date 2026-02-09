# Báo cáo về các trường hợp ngoại lệ (Edge Cases) trong giám sát PM2.5

**Tác giả:** Manus AI
**Ngày:** 23 tháng 1 năm 2026

## Giới thiệu

Báo cáo này tổng hợp và phân tích các trường hợp ngoại lệ (edge cases) trong việc giám sát nồng độ bụi mịn PM2.5, dựa trên các nghiên cứu khoa học đã được bình duyệt. Các trường hợp này bao gồm các hiện tượng gây ra sai số trong đo đạc và các cơ chế hóa học khí quyển phức tạp dẫn đến sự hình thành PM2.5 trong những điều kiện không ngờ tới. Việc hiểu rõ các edge cases này là rất quan trọng để có thể diễn giải chính xác dữ liệu chất lượng không khí, đặc biệt là tại các khu vực có điều kiện khí hậu đặc thù như Hà Nội.

Báo cáo tập trung vào hai nhóm edge cases chính:
1.  **Sai số đo đạc do sương mù và độ ẩm cao**: Hiện tượng các cảm biến quang học (light-scattering) ghi nhận sai nồng độ PM2.5 do sự hiện diện của hơi nước trong không khí.
2.  **Sự hình thành PM2.5 trong điều kiện bất thường**: Các cơ chế hóa học dẫn đến sự gia tăng nhanh chóng của PM2.5 ngay cả khi trời trong, nắng đẹp hoặc trong điều kiện sương mù dày đặc.

## 1. Sai số đo đạc do sương mù và độ ẩm cao (Measurement Artifacts)

Một trong những thách thức lớn nhất khi sử dụng các cảm biến PM2.5 giá rẻ dựa trên phương pháp tán xạ ánh sáng là sự ảnh hưởng của độ ẩm. Các nghiên cứu đã chỉ ra rằng các cảm biến này có thể ghi nhận sai lệch đáng kể khi độ ẩm tương đối (RH) tăng cao, và đặc biệt là khi có sương mù.

### 1.1. Cơ chế gây sai số

Cơ chế chính gây ra sai số là do các cảm biến tán xạ ánh sáng không thể phân biệt được giữa các hạt bụi rắn và các giọt nước lỏng trong không khí (như trong sương mù). Về cơ bản, các giọt sương mù cũng là các hạt aerosol lỏng, chúng tán xạ ánh sáng tương tự như các hạt bụi, dẫn đến việc cảm biến "đếm nhầm" chúng là bụi PM2.5. Một nghiên cứu của Kim và cộng sự (2023) đã chứng minh rõ ràng rằng độ ẩm ở dạng hơi (gaseous humidity) không gây ra sai số, nhưng độ ẩm ở dạng lỏng như sương mù (steam humidity) lại gây ra sai số đo đạc nghiêm trọng [1].

> "Độ ẩm ở dạng khí không gây ra sai số trong các phép đo PM bằng phương pháp tán xạ ánh sáng. Ngược lại, độ ẩm ở dạng hơi nước, chẳng hạn như sương mù, đã gây ra sai số trong phép đo PM." [1]

Ngoài ra, ở độ ẩm tương đối rất cao (thường trên 85%), các hạt bụi có tính hút ẩm (như sunfat, nitrat) sẽ hấp thụ hơi nước và tăng kích thước. Sự tăng trưởng kích thước này làm tăng tiết diện tán xạ ánh sáng của chúng, khiến cảm biến ghi nhận nồng độ khối lượng PM cao hơn thực tế. Jayaratne và cộng sự (2018) đã chỉ ra rằng nồng độ PM2.5 đo được có thể tăng gấp 2-3 lần ở độ ẩm trên 85% [2].

### 1.2. Bằng chứng định lượng

| Điều kiện | Ảnh hưởng đến cảm biến | Nguồn | 
| :--- | :--- | :--- | 
| Sương mù (RH > 100%) | Ghi nhận giọt sương mù là hạt bụi, gây sai số lớn. | [1] | 
| Độ ẩm cao (RH > 85%) | Hạt hút ẩm trương nở, tăng tiết diện tán xạ, gây sai số. | [2] | 

**Bảng 1:** Tổng hợp ảnh hưởng của độ ẩm và sương mù đến cảm biến PM2.5.

## 2. Các cơ chế hình thành PM2.5 bất thường

Bên cạnh các sai số đo đạc, các điều kiện khí quyển đặc biệt có thể thúc đẩy các phản ứng hóa học, dẫn đến sự hình thành nhanh chóng của các hạt thứ cấp (secondary aerosols), là thành phần chính của PM2.5 trong các đợt ô nhiễm nặng.

### 2.1. Sương mù và mây tầng thấp thúc đẩy phản ứng pha lỏng

Trái ngược với việc chỉ gây ra sai số đo đạc, sương mù và mây tầng thấp còn là một "lò phản ứng" hóa học hiệu quả. Lượng nước lỏng dồi dào trong các giọt sương mù/mây tạo điều kiện lý tưởng cho các phản ứng hóa học pha lỏng, đặc biệt là quá trình oxy hóa SO2 thành sunfat (SO4), một thành phần quan trọng của PM2.5. Các nghiên cứu tại vùng Đồng bằng Bắc Bộ Trung Quốc đã chỉ ra rằng tốc độ hình thành sunfat trong nước mây có thể đạt tới 0.5-1.3 μg m⁻³ h⁻¹, cao hơn nhiều so với các con đường phản ứng trong pha khí và trên bề mặt hạt aerosol [3] [4].

> "Tỷ lệ oxy hóa lưu huỳnh cao (>0.6) trong điều kiện ô nhiễm nặng có liên quan đến mây tầng thấp và sương mù ở Đồng bằng Bắc Bộ Trung Quốc, gây ra bởi luồng không khí ẩm từ phía nam." [3]

Cơ chế này đặc biệt hiệu quả khi có sự hiện diện của amoniac (NH3) nồng độ cao, làm tăng độ pH của các giọt nước (>5.5), từ đó thúc đẩy quá trình oxy hóa SO2 bởi các chất oxy hóa như NO2 và HONO [4]. Điều này giải thích tại sao các đợt ô nhiễm PM2.5 nghiêm trọng thường đi kèm với độ ẩm cao và sương mù.

### 2.2. Trời trong, nắng đẹp vẫn có thể có PM2.5 cao

Một trường hợp ngoại lệ khác là hiện tượng nồng độ PM2.5 vẫn ở mức cao dù trời trong và nắng đẹp. Điều này có vẻ phản trực giác nhưng lại được giải thích bằng hóa học quang hóa (photochemistry). Bức xạ mặt trời mạnh mẽ, đặc biệt là tia cực tím (UV), thúc đẩy các phản ứng quang hóa tạo ra các gốc oxy hóa mạnh như hydroxyl (OH). Các gốc này sẽ oxy hóa các hợp chất hữu cơ dễ bay hơi (VOCs) có trong khí quyển (từ khí thải giao thông, công nghiệp, sinh học) để tạo thành các hợp chất hữu cơ có độ bay hơi thấp, sau đó ngưng tụ lại thành các hạt aerosol hữu cơ thứ cấp (Secondary Organic Aerosol - SOA) [7].

Một nghiên cứu của Wu và cộng sự (2022) cho thấy trong điều kiện bức xạ mặt trời mạnh, tốc độ hình thành SOA có thể rất nhanh, lên tới 15.0% mỗi giờ [7]. Đáng chú ý, một nghiên cứu khác của Christiansen và cộng sự (2020) còn phát hiện ra rằng ở nhiều khu vực, nồng độ PM2.5 trung bình vào những ngày trời trong lại cao hơn những ngày có mây, ngoại trừ một vài trường hợp vào mùa đông [8].

> "Ở tất cả các khu vực, nồng độ PM2.5 vào ngày trời trong thường cao hơn so với ngày có mây, với một vài ngoại lệ trong mùa đông." [8]

Điều này cho thấy vai trò quan trọng của hóa học quang hóa trong việc hình thành PM2.5, đặc biệt là ở các đô thị có nguồn phát thải VOCs dồi dào.

### 2.3. Vòng lặp phản hồi tích cực của nước trong aerosol (Aerosol Liquid Water)

Nước chứa trong các hạt aerosol (Aerosol Liquid Water - ALW) đóng một vai trò trung tâm trong các vòng lặp phản hồi tích cực làm trầm trọng thêm các đợt ô nhiễm. Khi độ ẩm tăng (thường trên 40-60%), các hạt aerosol chuyển từ trạng thái bán rắn sang trạng thái lỏng. Sự chuyển pha này tạo điều kiện cho các phản ứng hóa học không đồng nhất và pha lỏng diễn ra nhanh hơn, tạo ra nhiều hơn các hợp chất hút ẩm như sunfat và nitrat [5]. Các hạt này lại hút thêm nhiều nước hơn, làm tăng ALW, và cứ thế tạo thành một vòng lặp phản hồi tích cực, dẫn đến sự bùng nổ nồng độ PM2.5 trong các đợt ô nhiễm sương mù (haze) [5].

## 3. Ý nghĩa đối với Hà Nội

Các edge cases này có ý nghĩa đặc biệt quan trọng đối với việc giám sát và dự báo chất lượng không khí tại Hà Nội, một thành phố có khí hậu nhiệt đới ẩm, thường xuyên có sương mù và độ ẩm cao, đặc biệt là vào mùa đông và mùa xuân.

1.  **Diễn giải dữ liệu cảm biến**: Dữ liệu từ các mạng lưới cảm biến PM2.5 giá rẻ tại Hà Nội cần được diễn giải một cách thận trọng, đặc biệt là trong những ngày có sương mù hoặc độ ẩm rất cao. Cần có các thuật toán hiệu chỉnh để loại bỏ các sai số do sương mù gây ra, tránh báo động sai về mức độ ô nhiễm.
2.  **Dự báo ô nhiễm**: Các mô hình dự báo chất lượng không khí cần tích hợp đầy đủ các cơ chế hóa học phức tạp liên quan đến sương mù và hóa học quang hóa. Việc chỉ dựa vào lượng phát thải là không đủ để dự báo chính xác các đợt ô nhiễm PM2.5 nghiêm trọng.
3.  **Kiểm soát ô nhiễm**: Các chiến lược kiểm soát ô nhiễm không chỉ cần tập trung vào việc giảm phát thải bụi sơ cấp mà còn phải kiểm soát chặt chẽ các khí tiền chất như SO2, NOx và VOCs, là những tác nhân chính gây ra sự hình thành các hạt thứ cấp trong cả điều kiện sương mù và trời nắng.

## Kết luận

Việc hiểu rõ các trường hợp ngoại lệ trong giám sát và hình thành PM2.5 là tối quan trọng. Sương mù và độ ẩm cao không chỉ gây ra sai số đo đạc cho các cảm biến quang học mà còn là môi trường phản ứng hóa học mạnh mẽ, thúc đẩy sự hình thành PM2.5. Ngược lại, ngay cả trong điều kiện trời trong, nắng đẹp, các phản ứng quang hóa vẫn có thể tạo ra lượng lớn aerosol hữu cơ thứ cấp. Đối với một thành phố như Hà Nội, việc áp dụng các kiến thức này vào thực tiễn sẽ giúp cải thiện đáng kể độ chính xác của hệ thống giám sát và hiệu quả của các biện pháp quản lý chất lượng không khí.

## Tài liệu tham khảo

[1] Kim, H., Kim, J., & Roh, S. (2023). Effects of Gas and Steam Humidity on Particulate Matter Measurements Obtained Using Light-Scattering Sensors. *Sensors (Basel)*. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10347098/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10347098/)

[2] Jayaratne, R., Liu, X., Thai, P., Dunbabin, M., & Morawska, L. (2018). The influence of humidity on the performance of a low-cost air particle mass sensor and the effect of atmospheric fog. *Atmospheric Measurement Techniques*. [https://amt.copernicus.org/articles/11/4883/2018/](https://amt.copernicus.org/articles/11/4883/2018/)

[3] Cai, S., et al. (2024). Important Role of Low Cloud and Fog in Sulfate Aerosol Formation During Winter Haze Over the North China Plain. *Geophysical Research Letters*. [https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL106597](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL106597)

[4] Wang, J., et al. (2020). Fast sulfate formation from oxidation of SO2 by NO2 and HONO observed in Beijing haze. *Nature Communications*. [https://www.nature.com/articles/s41467-020-16683-x](https://www.nature.com/articles/s41467-020-16683-x)

[5] Meng, X., et al. (2024). Particle phase state and aerosol liquid water greatly impact secondary aerosol formation: insights into phase transition and its role in haze events. *Atmospheric Chemistry and Physics*. [https://acp.copernicus.org/articles/24/2399/2024/](https://acp.copernicus.org/articles/24/2399/2024/)

[6] Cheng, Y., et al. (2016). Reactive nitrogen chemistry in aerosol water as a source of sulfate during haze events in China. *Science Advances*. [https://www.science.org/doi/10.1126/sciadv.1601530](https://www.science.org/doi/10.1126/sciadv.1601530)

[7] Wu, Y., et al. (2022). Tracing the Formation of Secondary Aerosols Influenced by Solar Radiation and Relative Humidity in Suburban Environment. *Journal of Geophysical Research: Atmospheres*. [https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022JD036913](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022JD036913)

[8] Christiansen, A. E., Carlton, A. G., & Henderson, B. H. (2020). Differences in fine particle chemical composition on clear and cloudy days. *Atmospheric Chemistry and Physics*. [https://acp.copernicus.org/articles/20/11607/2020/](https://acp.copernicus.org/articles/20/11607/2020/)
