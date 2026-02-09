
# Báo cáo Tổng hợp: Tác động của Mây và Bức xạ Mặt trời đến Ô nhiễm PM2.5

**Ngày:** 23 tháng 1 năm 2026
**Tác giả:** Manus AI

## 1. Giới thiệu

Báo cáo này tổng hợp kết quả từ một nghiên cứu chuyên sâu về các mối quan hệ nhân quả giữa **độ che phủ của mây (cloud cover)**, **bức xạ mặt trời (solar radiation)**, và sự hình thành các hạt vật chất mịn (PM2.5) trong khí quyển, với trọng tâm áp dụng cho khu vực Hà Nội, Việt Nam và các vùng có đặc điểm khí hậu tương tự ở Đông Nam Á. Nghiên cứu được thực hiện bằng cách tuân thủ một bộ quy tắc nghiêm ngặt về trích xuất dữ liệu khoa học, đảm bảo tính chính xác, yêu cầu bằng chứng cụ thể và tránh các suy diễn không có cơ sở.

Nhiệm vụ tập trung vào việc làm rõ hai chuỗi cơ chế chính:
1.  Tác động của mây đến sự ổn định khí quyển và sự tích tụ PM2.5.
2.  Vai trò của bức xạ mặt trời trong việc thúc đẩy các phản ứng quang hóa tạo ra sol khí hữu cơ thứ cấp (Secondary Organic Aerosol - SOA), một thành phần quan trọng của PM2.5.

## 2. Phương pháp luận

Quá trình nghiên cứu bao gồm việc tìm kiếm và phân tích các bài báo khoa học đã được bình duyệt (peer-reviewed) từ các tạp chí uy tín (Tier-1). Sáu nguồn tài liệu chính đã được lựa chọn và phân tích chi tiết để trích xuất các mối quan hệ nhân quả. Mỗi mối quan hệ được ghi lại với cơ chế vật lý/hóa học rõ ràng, các điều kiện đi kèm, và bằng chứng trích dẫn trực tiếp từ nguồn. Các kết quả sau đó được tổng hợp thành một tệp dữ liệu có cấu trúc JSON theo một lược đồ định sẵn.

## 3. Các Chuỗi Quan hệ Nhân quả chính được xác định

Nghiên cứu đã xác định và cung cấp bằng chứng cho ba chuỗi quan hệ nhân quả chính, như được yêu cầu trong nhiệm vụ.

### 3.1. Chuỗi 1: Mây → Ổn định Khí quyển → Tích tụ PM2.5

Cơ chế này giải thích cách mây ảnh hưởng đến sự phân tán vật lý của các chất ô nhiễm. Có hai kịch bản chính tùy thuộc vào thời gian trong ngày.

**Ban ngày:**

> Mây che phủ làm giảm lượng bức xạ mặt trời chiếu xuống bề mặt, dẫn đến việc sưởi ấm bề mặt yếu hơn. Điều này làm giảm sự đối lưu và phát triển của lớp biên hành tinh (Planetary Boundary Layer - PBL), tạo ra một lớp khí quyển ổn định hơn. Lớp biên thấp và ổn định này hoạt động như một chiếc "vung", ngăn cản các chất ô nhiễm phân tán lên cao và gây ra sự tích tụ PM2.5 gần mặt đất. Một nghiên cứu của Lu và cộng sự (2024) đã định lượng rằng sự tương tác này có thể làm giảm tới 50% chiều cao lớp biên và bức xạ mặt trời [4].

**Ban đêm:**

> Ngược lại, vào ban đêm, bầu trời quang đãng (ít mây) làm tăng cường quá trình làm mát bức xạ bề mặt. Bề mặt lạnh đi nhanh chóng, tạo ra một lớp nghịch nhiệt (temperature inversion) gần mặt đất. Lớp nghịch nhiệt này cực kỳ ổn định và "bẫy" các chất ô nhiễm được phát thải vào ban đêm, dẫn đến nồng độ PM2.5 tăng đột biến. Các nghiên cứu của Hu và cộng sự (2021) và một nghiên cứu nền tảng tại Hà Nội của Hien và cộng sự (2002) đã cung cấp bằng chứng mạnh mẽ cho cơ chế này [1, 6].

| Tác nhân | Hiệu ứng trung gian | Kết quả cuối cùng | Điều kiện | Nguồn | 
| :--- | :--- | :--- | :--- | :--- | 
| **Mây che phủ (cao)** | Giảm bức xạ mặt trời → Giảm chiều cao PBL | Tăng tích tụ PM2.5 | Ban ngày | [4] | 
| **Mây che phủ (thấp)** | Tăng làm mát bức xạ | Tăng nghịch nhiệt → Tăng tích tụ PM2.5 | Ban đêm | [1, 6] | 

### 3.2. Chuỗi 2: Bức xạ Mặt trời → Quang hóa → Hình thành SOA (PM2.5)

Cơ chế này mô tả quá trình hóa học tạo ra các hạt thứ cấp từ các chất khí tiền chất dưới tác động của ánh sáng mặt trời.

> Bức xạ mặt trời, đặc biệt là tia cực tím (UV), cung cấp năng lượng để bắt đầu các phản ứng quang hóa. Quá trình này bắt đầu bằng việc quang phân (photolysis) các phân tử như NO₂, O₃, và các hợp chất hữu cơ chứa oxy, tạo ra các gốc tự do có khả năng phản ứng cao, quan trọng nhất là gốc hydroxyl (OH) [3]. Các gốc OH này sau đó tấn công các hợp chất hữu cơ dễ bay hơi (Volatile Organic Compounds - VOCs), khởi đầu một chuỗi các phản ứng oxy hóa phức tạp. Các sản phẩm của quá trình oxy hóa này có độ bay hơi thấp hơn và sẽ ngưng tụ lại để tạo thành sol khí hữu cơ thứ cấp (SOA), đóng góp trực tiếp vào khối lượng PM2.5. Các nghiên cứu của Wu và cộng sự (2022) và Badali và cộng sự (2015) cho thấy tốc độ hình thành SOA tăng lên đáng kể khi có bức xạ mặt trời mạnh, đặc biệt là vào mùa hè [2, 3].

### 3.3. Chuỗi 3: Mây che phủ như một yếu tố điều tiết (Moderator)

Ngoài việc ảnh hưởng đến sự ổn định khí quyển, mây còn đóng vai trò điều tiết trực tiếp chuỗi phản ứng quang hóa.

> Bằng cách làm giảm lượng bức xạ UV chiếu xuống bề mặt, mây che phủ có tác dụng làm chậm lại tốc độ của các phản ứng quang phân. Điều này làm giảm tốc độ sản sinh gốc OH và do đó làm giảm tốc độ hình thành SOA. Nghiên cứu của Yang và cộng sự (2022) đã định lượng rằng các sol khí (tương tự như mây) có thể làm giảm đáng kể tốc độ quang phân và sản xuất ozone, một sản phẩm phụ của quá trình quang hóa [5].

Điều này dẫn đến một sự đánh đổi phức tạp: mây che phủ có thể làm giảm việc hình thành PM2.5 thứ cấp (hiệu ứng hóa học), nhưng đồng thời lại làm tăng sự tích tụ của PM2.5 sơ cấp và thứ cấp đã có sẵn (hiệu ứng vật lý). Hiệu ứng tổng thể phụ thuộc vào điều kiện khí tượng, nồng độ các chất tiền chất và thời gian trong ngày.

## 4. Kết luận và Hàm ý cho Hà Nội

Nghiên cứu đã xác nhận và cung cấp bằng chứng khoa học vững chắc cho các cơ chế chính mà qua đó mây và bức xạ mặt trời ảnh hưởng đến nồng độ PM2.5. Các phát hiện này đặc biệt phù hợp với Hà Nội, một thành phố nằm trong vùng đồng bằng, chịu ảnh hưởng của chế độ gió mùa và thường xuyên có các đợt ô nhiễm không khí cao vào mùa đông, trùng khớp với các điều kiện hình thành nghịch nhiệt bức xạ và nghịch nhiệt chìm lắng được mô tả trong nghiên cứu của Hien và cộng sự (2002) [6].

- **Vào mùa đông ở Hà Nội**, các đợt ô nhiễm nghiêm trọng thường liên quan đến điều kiện trời quang, lặng gió vào ban đêm, tạo điều kiện lý tưởng cho nghịch nhiệt bức xạ hình thành và tích tụ ô nhiễm.
- **Vào mùa hè**, mặc dù bức xạ mặt trời mạnh có thể thúc đẩy sự hình thành SOA, nhưng các yếu tố khác như chiều cao lớp biên lớn hơn và sự xuất hiện của mưa rào thường giúp phân tán ô nhiễm hiệu quả hơn.

Sự hiểu biết về các cơ chế kép này—một mặt là sự tích tụ vật lý do điều kiện ổn định và mặt khác là sự hình thành hóa học do quang hóa—là rất quan trọng để xây dựng các mô hình dự báo chất lượng không khí chính xác hơn và đưa ra các chiến lược kiểm soát ô nhiễm hiệu quả cho Hà Nội và các đô thị tương tự.

## 5. Tài liệu tham khảo

[1] Hu, J., Zhao, T., Liu, J., et al. (2021). Nocturnal surface radiation cooling modulated by cloud cover change reinforces PM2.5 accumulation: Observational study of heavy air pollution in the Sichuan Basin, Southwest China. *Science of The Total Environment*, 794, 148624. https://doi.org/10.1016/j.scitotenv.2021.148624

[2] Wu, Y., Liu, D., Tian, P., et al. (2022). Tracing the Formation of Secondary Aerosols Influenced by Solar Radiation and Relative Humidity in Suburban Environment. *Journal of Geophysical Research: Atmospheres*, 127(17). https://doi.org/10.1029/2022JD036913

[3] Badali, K. M., Zhou, S., Aljawhary, D., et al. (2015). Formation of hydroxyl radicals from photolysis of secondary organic aerosol material. *Atmospheric Chemistry and Physics*, 15, 7831–7840. https://doi.org/10.5194/acp-15-7831-2015

[4] Lu, H., Xie, M., Zhuang, B., et al. (2024). Impacts of atmospheric circulation patterns and cloud inhibition on aerosol radiative effect and boundary layer structure during winter air pollution in Sichuan Basin, China. *Atmospheric Chemistry and Physics*, 24, 8963–8982. https://doi.org/10.5194/acp-24-8963-2024

[5] Yang, H., Chen, L., Liao, H., et al. (2022). Impacts of aerosol–photolysis interaction and aerosol–radiation feedback on surface-layer ozone in North China during multi-pollutant air pollution episodes. *Atmospheric Chemistry and Physics*, 22, 4101–4116. https://doi.org/10.5194/acp-22-4101-2022

[6] Hien, P.D., Bac, V.T., Tham, H.C., et al. (2002). Influence of meteorological conditions on PM2.5 and PM2.5−10 concentrations during the monsoon season in Hanoi, Vietnam. *Atmospheric Environment*, 36(21), 3473-3484. https://doi.org/10.1016/S1352-2310(02)00295-9
