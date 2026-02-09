# Báo cáo Xác thực và Nghiên cứu Proxy

**ID Nhiệm vụ:** 19  
**Danh mục:** Xác thực & Nghiên cứu  
**Mức độ ưu tiên:** Cao  

---

Báo cáo này trình bày kết quả đánh giá và nghiên cứu khoa học về năm chiến lược proxy được sử dụng trong Đồ thị Tri thức Chất lượng không khí Hà Nội. Đối với mỗi proxy, chúng tôi đã tiến hành một cuộc tổng quan tài liệu, đánh giá phương pháp tiếp cận hiện tại, và đưa ra các khuyến nghị để cải tiến.

---

## Proxy Chiều cao Lớp biên Hành tinh (PBLH)

### Tổng quan Tài liệu

Chiều cao lớp biên hành tinh (PBLH) là một tham số cơ bản quyết định thể tích không khí mà các chất ô nhiễm bề mặt có thể được pha loãng vào. Các nghiên cứu cho thấy mối tương quan nghịch rõ rệt giữa PBLH và nồng độ các chất ô nhiễm, đặc biệt là PM2.5. Su và cộng sự (2018) đã chỉ ra rằng mối tương quan này đặc biệt mạnh khi PBLH nông (< 1 km), một điều kiện thường thấy vào mùa đông [1]. Nghiên cứu của họ cũng nhấn mạnh tầm quan trọng của "tỷ lệ thông gió" (ventilation rate), một chỉ số kết hợp cả phân tán ngang (tốc độ gió) và phân tán dọc (PBLH), cho thấy nó có mối tương quan nghịch mạnh với nồng độ PM2.5 bề mặt. Một nghiên cứu cụ thể tại Hà Nội của Ngoc và cộng sự (2021) đã xác nhận rằng PBLH là một trong những yếu tố chính kiểm soát các đợt ô nhiễm không khí. Họ phát hiện ra rằng vào những ngày mù mịt, PBLH luôn ở dưới 1000m, làm suy yếu sự pha trộn dọc và dẫn đến sự tích tụ các chất ô nhiễm [2].

Các phương pháp ước tính PBLH khi không có dữ liệu đo đạc trực tiếp (như lidar hoặc radiosonde) thường dựa vào các công thức thực nghiệm sử dụng các biến khí tượng bề mặt. Các công thức cổ điển, như của Arya (1981), đã thiết lập các mối quan hệ giữa PBLH ổn định với các tham số lớp bề mặt như vận tốc ma sát (u*), độ dài Obukhov (L) và tham số Coriolis (f) [3]. Các công thức này, mặc dù có nền tảng vật lý, nhưng đòi hỏi các đầu vào không phải lúc nào cũng có sẵn từ các trạm thời tiết tiêu chuẩn. Các phương pháp hiện đại hơn thường sử dụng các mô hình thống kê hoặc học máy để ước tính PBLH từ các biến dễ đo lường hơn như nhiệt độ, tốc độ gió và độ che phủ mây, nhưng các hệ số trong các mô hình này thường phụ thuộc nhiều vào địa điểm và mùa.

### Đánh giá Phương pháp Hiện tại

Phương pháp hiện tại sử dụng một công thức nhân đơn giản:

`PBLH = base_height × wind_factor × cloud_factor × time_factor × temp_factor`

- **Điểm mạnh**: Cách tiếp cận này trực quan và dễ thực hiện, nắm bắt được các mối quan hệ định tính chính: PBLH tăng theo tốc độ gió và nhiệt độ, và giảm theo độ che phủ mây. Nó cũng bao gồm một yếu tố biến thiên theo ngày đêm, điều này là quan trọng.
- **Điểm yếu**: Điểm yếu lớn nhất là tính đặc thù và các hệ số tùy ý của nó. Công thức này không dựa trên một lý thuyết vật lý được công bố rộng rãi. Các giá trị cụ thể (ví dụ: `base_height = 150 m`, `wind_factor = 1 + (wind_speed / 4.0)`) dường như được điều chỉnh cho một điều kiện cụ thể và có thể không khái quát tốt cho các điều kiện hoặc địa điểm khác. Nó không phân biệt giữa các chế độ lớp biên khác nhau (ví dụ: đối lưu ban ngày so với ổn định ban đêm) một cách rõ ràng, mặc dù `time_factor` có thể cố gắng làm điều này một cách gián tiếp.
- **Mức độ tin cậy**: **Thấp đến Trung bình**. Mặc dù nó nắm bắt được các mối quan hệ đúng hướng, nhưng việc thiếu cơ sở lý thuyết và các hệ số tùy ý làm cho các ước tính định lượng của nó không chắc chắn. Nó có thể hoạt động như một proxy bậc một, nhưng không có khả năng chính xác trong một loạt các điều kiện.

### Khuyến nghị

1.  **Sửa đổi cách tiếp cận hiện tại**: Thay vì một công thức nhân duy nhất, hãy phát triển các tham số hóa riêng biệt cho lớp biên đối lưu ban ngày (CBL) và lớp biên ổn định ban đêm (SBL). Ví dụ, một mô hình tốc độ tăng trưởng CBL đơn giản có thể được sử dụng cho ban ngày, trong khi một công thức dựa trên u* và L (như của Arya) có thể được sử dụng cho ban đêm nếu có dữ liệu cần thiết. Nếu không, một phiên bản sửa đổi của phương pháp hiện tại với các hệ số được hiệu chỉnh dựa trên dữ liệu lidar từ Hà Nội có thể được sử dụng.
2.  **Cách tiếp cận thay thế**: Sử dụng các sản phẩm PBLH từ các mô hình tái phân tích toàn cầu như ERA5. Mặc dù có độ phân giải không gian thô, ERA5 cung cấp các ước tính PBLH nhất quán về mặt vật lý và có thể được hiệu chỉnh thống kê (statistical downscaling) bằng cách sử dụng dữ liệu quan sát bề mặt cục bộ để cải thiện độ chính xác ở quy mô địa phương.
3.  **Chiến lược xác thực**: Các ước tính PBLH từ proxy nên được xác thực so với các phép đo PBLH từ lidar tại Hà Nội (ví dụ, từ nghiên cứu của Ngoc và cộng sự, 2021). So sánh nên được thực hiện trên cơ sở theo mùa và theo ngày đêm để đánh giá hiệu suất của proxy trong các điều kiện khí tượng khác nhau.

---

## Proxy Độ ổn định Khí quyển

### Tổng quan Tài liệu

Độ ổn định khí quyển chi phối sự phân tán của các chất ô nhiễm. Các điều kiện không ổn định (thường là ban ngày, trời nắng) tăng cường sự pha trộn hỗn loạn và phân tán, trong khi các điều kiện ổn định (thường là ban đêm, trời quang) ngăn chặn sự pha trộn và dẫn đến nồng độ ô nhiễm cao. Sơ đồ phân loại Pasquill-Gifford (PG) là một phương pháp kinh điển để ước tính độ ổn định chỉ từ các quan sát bề mặt: tốc độ gió, độ che phủ mây và bức xạ mặt trời (được suy ra từ thời gian trong ngày và góc mặt trời) [4]. Bảng phân loại PG tiêu chuẩn xác định các lớp ổn định từ A (rất không ổn định) đến F (rất ổn định). Mặc dù được sử dụng rộng rãi trong các mô hình phân tán quy chuẩn, hiệu suất của nó đã bị chỉ trích, đặc biệt là trong việc xác định chính xác các điều kiện không ổn định. Các phương pháp thay thế để ước tính độ ổn định khi không có profile nhiệt độ thẳng đứng bao gồm sử dụng độ lệch chuẩn của hướng gió (sigma theta) hoặc số Richardson khối (bulk Richardson number), nhưng những phương pháp này đòi hỏi dữ liệu đo đạc chi tiết hơn.

### Đánh giá Phương pháp Hiện tại

Phương pháp hiện tại là một phiên bản đơn giản hóa của các lớp ổn định Pasquill-Gifford dựa trên tốc độ gió, độ che phủ mây và thời gian trong ngày. 

- **Điểm mạnh**: Phương pháp này đơn giản và chỉ dựa vào các biến khí tượng có sẵn. Nó nắm bắt được bản chất của sơ đồ PG, đó là sự cân bằng giữa sự sinh ra hỗn loạn do cơ học (gió) và do sức nổi (bức xạ/mây).
- **Điểm yếu**: Sơ đồ PG ban đầu được phát triển cho các khu vực nông thôn, địa hình bằng phẳng và có thể không hoạt động tốt trong môi trường đô thị phức tạp như Hà Nội, nơi mà độ nhám bề mặt và hiệu ứng đảo nhiệt đô thị (UHI) có thể làm thay đổi đáng kể cấu trúc ổn định. Ví dụ, UHI có thể làm xói mòn các lớp nghịch nhiệt ổn định vào ban đêm, dẫn đến các điều kiện ít ổn định hơn so với dự đoán của sơ đồ PG tiêu chuẩn. Việc đơn giản hóa các lớp thành một vài loại có thể làm mất đi các sắc thái quan trọng.
- **Mức độ tin cậy**: **Trung bình**. Phương pháp này cung cấp một ước tính bậc một hợp lý về độ ổn định, nhưng độ chính xác của nó trong môi trường đô thị nhiệt đới là không chắc chắn. Nó có khả năng hoạt động tốt nhất trong việc phân biệt giữa các điều kiện rất ổn định (ban đêm, gió nhẹ, trời quang) và các điều kiện gần trung tính/không ổn định (ban ngày, gió mạnh).

### Khuyến nghị

1.  **Sửa đổi cách tiếp cận hiện tại**: Kết hợp một sự điều chỉnh cho hiệu ứng đảo nhiệt đô thị. Ví dụ, vào ban đêm với gió nhẹ, lớp ổn định có thể được nâng cấp lên một lớp ít ổn định hơn (ví dụ, từ F lên E, hoặc E lên D) để tính đến sự pha trộn tăng cường do UHI. Các ngưỡng cụ thể có thể được xác định từ các nghiên cứu về UHI tại Hà Nội.
2.  **Cách tiếp cận thay thế**: Nếu có dữ liệu, hãy sử dụng phương pháp dựa trên số Richardson khối (Bulk Richardson number), đòi hỏi nhiệt độ ở hai độ cao và tốc độ gió. Mặc dù đòi hỏi nhiều dữ liệu hơn, nó có nền tảng vật lý vững chắc hơn. Một lựa chọn khác là sử dụng các chỉ số ổn định được cung cấp trực tiếp bởi các mô hình tái phân tích như ERA5, mặc dù chúng có thể cần được xác thực và hiệu chỉnh ở quy mô địa phương.
3.  **Chiến lược xác thực**: So sánh các lớp ổn định được suy ra từ proxy với các phép đo trực tiếp về thông lượng nhiệt và động lượng từ một tháp dòng xoáy (eddy covariance tower), nếu có. Một phương pháp gián tiếp hơn là so sánh các lớp ổn định với gradient nhiệt độ thẳng đứng được đo bởi radiosonde hoặc các thiết bị bay không người lái (UAV).

---

## Proxy Nước lỏng trong Sol khí (ALW)

### Tổng quan Tài liệu

Nước lỏng trong sol khí (Aerosol Liquid Water - ALW) là một thành phần quan trọng của khối lượng PM2.5, đặc biệt là ở độ ẩm tương đối (RH) cao. ALW ảnh hưởng đến các đặc tính quang học của sol khí, kích thước hạt và đóng vai trò là môi trường cho các phản ứng hóa học trong pha lỏng, có thể dẫn đến sự hình thành sol khí thứ cấp. Mối quan hệ giữa ALW và RH có tính phi tuyến cao và phụ thuộc vào thành phần hóa học của sol khí. Các hạt hút ẩm (như sunfat, nitrat) hấp thụ nước ở RH thấp hơn so với các hạt kỵ nước. Quá trình này thường bắt đầu tăng tốc đáng kể trên một ngưỡng RH nhất định, được gọi là điểm tan chảy (deliquescence relative humidity - DRH), thường nằm trong khoảng 60-80% đối với các hỗn hợp sol khí trong khí quyển. Các mô hình nhiệt động lực học như ISORROPIA-II được sử dụng để tính toán chính xác ALW dựa trên thành phần hóa học và điều kiện khí tượng, nhưng chúng đòi hỏi đầu vào chi tiết [6]. Các tham số hóa đơn giản hơn thường biểu diễn ALW như một hàm của RH, đôi khi có thêm sự phụ thuộc vào nhiệt độ hoặc một chỉ số về độ hút ẩm của sol khí (ví dụ, tham số kappa) [7].

### Đánh giá Phương pháp Hiện tại

Phương pháp hiện tại là một hàm tuyến tính từng đoạn của RH:

`If RH < 70%: ALW ≈ 0`
`Elif RH < 80%: ALW ≈ 0.1 * (RH - 70) / 10`
`...`

- **Điểm mạnh**: Phương pháp này nắm bắt được hành vi cơ bản là ALW tăng không đáng kể ở RH thấp và tăng nhanh ở RH cao. Ngưỡng 70% là một ước tính hợp lý cho sự khởi đầu của việc hấp thụ nước đáng kể.
- **Điểm yếu**: Đây là một sự đơn giản hóa quá mức của một quá trình phức tạp. Mối quan hệ thực tế giữa ALW và RH có hình dạng chữ 'S' (sigmoidal) hơn là tuyến tính từng đoạn. Quan trọng hơn, nó bỏ qua hoàn toàn sự phụ thuộc vào thành phần hóa học của sol khí. Trong các điều kiện ô nhiễm nặng với nồng độ cao của các muối vô cơ hòa tan, lượng ALW ở một mức RH nhất định sẽ cao hơn nhiều so với trong các điều kiện sạch hơn. Công thức này không tính đến nồng độ khối lượng của sol khí.
- **Mức độ tin cậy**: **Thấp**. Mặc dù nó cung cấp một ước tính định tính, nó có khả năng đánh giá thấp đáng kể ALW trong các đợt ô nhiễm nặng và có thể không chính xác về mặt định lượng trong hầu hết các điều kiện. Nó chỉ hữu ích như một chỉ báo rất thô về sự hiện diện có thể có của ALW.

### Khuyến nghị

1.  **Sửa đổi cách tiếp cận hiện tại**: Cải thiện tham số hóa bằng cách làm cho nó phụ thuộc vào cả RH và nồng độ khối lượng PM2.5. Một công thức đơn giản có thể là `ALW = f(RH) * PM2.5`, trong đó `f(RH)` là một hàm phi tuyến (ví dụ, hàm mũ hoặc logistic) được hiệu chỉnh từ dữ liệu. Điều này sẽ tính đến thực tế là nhiều sol khí hơn có thể hấp thụ nhiều nước hơn.
2.  **Cách tiếp cận thay thế**: Một cách tiếp cận tốt hơn là sử dụng tham số hóa dựa trên kappa (κ). Tham số độ hút ẩm, κ, có thể được ước tính cho các loại sol khí khác nhau (ví dụ, đô thị, sinh khối cháy) hoặc được suy ra từ thành phần hóa học nếu có. Sau đó, ALW có thể được tính toán bằng cách sử dụng các công thức tiêu chuẩn liên quan đến κ, RH và thể tích sol khí khô. Ví dụ, Bian và cộng sự (2014) đã sử dụng một phương pháp dựa trên các phép đo độ hút ẩm để tính toán ALW ở Đồng bằng Hoa Bắc và so sánh nó với kết quả từ ISORROPIA II [6].
3.  **Chiến lược xác thực**: Các ước tính ALW từ proxy có thể được so sánh với các tính toán từ mô hình ISORROPIA-II chạy với dữ liệu thành phần hóa học PM2.5 chi tiết từ các chiến dịch đo đạc tại Hà Nội. Điều này sẽ cung cấp một tiêu chuẩn vàng để đánh giá hiệu suất của proxy.

---

## Phát hiện Đợt không khí lạnh (Cold Surge)

### Tổng quan Tài liệu

Các đợt không khí lạnh (cold surges) là các sự kiện thời tiết quy mô lớn đặc trưng bởi sự xâm nhập nhanh chóng của không khí lạnh và khô từ các vĩ độ cao (thường là từ áp cao Siberia-Mông Cổ) xuống các vĩ độ thấp hơn. Chúng là một đặc điểm nổi bật của gió mùa mùa đông ở Đông Á và có tác động đáng kể đến thời tiết ở Đông Nam Á, bao gồm cả Việt Nam. Các tiêu chí để xác định một đợt không khí lạnh thường bao gồm sự giảm nhiệt độ đột ngột, tăng áp suất mực nước biển (MSLP) và gió bắc hoặc đông bắc mạnh [8]. Các ngưỡng cụ thể thay đổi theo vùng. Ví dụ, một nghiên cứu ở Thái Lan đã xác định một đợt không khí lạnh bằng sự tăng MSLP ít nhất 1.8 hPa, tăng tốc độ gió ít nhất 2.6 m/s và giảm nhiệt độ ít nhất 1.7°C trong 24 giờ [9]. Các nghiên cứu khác tập trung vào sự di chuyển của một đường đẳng áp cụ thể (ví dụ, 1020 hPa) đến một vĩ độ nhất định. Các đợt không khí lạnh có thể làm thay đổi đáng kể chất lượng không khí bằng cách vừa mang theo ô nhiễm từ các khu vực nguồn phía bắc, vừa gây ra các điều kiện khí tượng (ví dụ, PBLH thấp hơn) có lợi cho sự tích tụ ô nhiễm tại địa phương.

### Đánh giá Phương pháp Hiện tại

Phương pháp hiện tại xác định một đợt không khí lạnh nếu:

`pressure > 1020 hPa AND wind_direction in [0-90] AND temperature < 15°C`

- **Điểm mạnh**: Cách tiếp cận này đơn giản và nắm bắt được các thành phần chính của một đợt không khí lạnh: áp suất cao, gió bắc và nhiệt độ thấp.
- **Điểm yếu**: Các ngưỡng là tĩnh và không tính đến sự thay đổi theo thời gian, điều này là cốt lõi của một sự kiện "surge" hay "outbreak". Một đợt không khí lạnh được định nghĩa bởi sự giảm nhiệt độ và tăng áp suất *nhanh chóng*, chứ không chỉ bởi các giá trị tuyệt đối. Ngưỡng nhiệt độ 15°C có thể quá thấp cho đầu mùa đông và quá cao cho cao điểm mùa đông.
- **Mức độ tin cậy**: **Thấp đến Trung bình**. Nó có thể xác định đúng một số sự kiện mạnh, nhưng có khả năng sẽ bỏ sót nhiều đợt không khí lạnh yếu hơn nhưng vẫn có ý nghĩa và có thể có kết quả dương tính giả khi điều kiện chỉ đơn giản là lạnh và ổn định nhưng không phải là một phần của một đợt không khí lạnh động.

### Khuyến nghị

1.  **Sửa đổi cách tiếp cận hiện tại**: Proxy phải dựa trên sự *thay đổi* của các biến khí tượng trong một khoảng thời gian cụ thể (ví dụ: 24 giờ). Một định nghĩa tốt hơn sẽ là:
    *   Giảm nhiệt độ trong 24 giờ > X °C (ví dụ: 3-5°C)
    *   VÀ Tăng MSLP trong 24 giờ > Y hPa (ví dụ: 2-4 hPa)
    *   VÀ Hướng gió duy trì ở hướng đông bắc.
    Các ngưỡng X và Y nên được xác định từ một phân tích khí hậu học của dữ liệu lịch sử cho Hà Nội.
2.  **Cách tiếp cận thay thế**: Áp dụng một chỉ số được chấp nhận rộng rãi trong khu vực, chẳng hạn như các chỉ số Gió mùa mùa đông Đông Á (EAWM) hoặc một chỉ số đợt không khí lạnh dựa trên phương pháp của Abdillah và cộng sự (2021) [8], sử dụng các thước đo định lượng của các luồng khối không khí lạnh về phía xích đạo.
3.  **Chiến lược xác thực**: Xác định các sự kiện đợt không khí lạnh lịch sử ảnh hưởng đến miền Bắc Việt Nam từ tài liệu hoặc báo cáo của cơ quan khí tượng. Kiểm tra xem proxy (hiện tại hoặc được đề xuất) có nắm bắt thành công các sự kiện đã biết này hay không. Phân tích các dị thường PM2.5 tổng hợp trong các sự kiện đợt không khí lạnh đã xác định để xác nhận tác động của chúng đối với chất lượng không khí.

---

## Proxy Phơi nhiễm Phát thải Ngược gió

### Tổng quan Tài liệu

Sự đóng góp của các nguồn phát thải ngược gió đối với chất lượng không khí tại địa phương là một khái niệm cơ bản trong khoa học ô nhiễm không khí. Vận chuyển tầm xa (LRT) của các chất ô nhiễm, đặc biệt là trong các sự kiện quy mô lớn như các đợt không khí lạnh, có thể là một yếu tố chính gây ra các đợt ô nhiễm nghiêm trọng ở các khu vực xuôi gió như Hà Nội. Các nghiên cứu như của Kim và cộng sự (2021) cho thấy các tương tác phức tạp, phi tuyến xảy ra khi các chất ô nhiễm được vận chuyển [10]. Việc định lượng tác động của các nguồn ngược gió thường đòi hỏi các công cụ phức tạp như mô hình vận chuyển hóa học (ví dụ: CMAQ, CAMx) hoặc mô hình thụ thể (ví dụ: PMF, PSCF). Hàm Đóng góp Nguồn Tiềm năng (PSCF) là một kỹ thuật được sử dụng rộng rãi kết hợp các quỹ đạo ngược của khối không khí (từ các mô hình như HYSPLIT) với các kiểm kê phát thải để xác định các nguồn gốc địa lý có khả năng của các chất ô nhiễm đến một địa điểm thụ thể.

### Đánh giá Phương pháp Hiện tại

Phương pháp hiện tại tính toán một tổng có trọng số của phát thải công nghiệp và giao thông trong bán kính 50km:

`exposure = (0.7 * industrial_emissions) + (0.3 * traffic_emissions)`

- **Điểm mạnh**: Nó cực kỳ đơn giản và thừa nhận rằng các loại nguồn khác nhau góp phần gây ô nhiễm.
- **Điểm yếu**: Proxy này có sai sót cơ bản để đại diện cho phơi nhiễm *ngược gió*.
    1.  **Tĩnh và Đẳng hướng**: Nó sử dụng một bán kính 50km cố định, hoàn toàn bỏ qua hướng gió và tốc độ gió. Nó coi các phát thải từ một nguồn cách 49km *xuôi gió* giống như một nguồn cách 49km *ngược gió*. Đây không phải là một thước đo phơi nhiễm ngược gió; nó là một thước đo mật độ phát thải tại địa phương.
    2.  **Trọng số Tùy ý**: Các trọng số 0.7 và 0.3 là tùy ý và thiếu cơ sở khoa học. Tác động tương đối của phát thải công nghiệp so với giao thông phụ thuộc vào thành phần hóa học, chiều cao phát tán và sự gần gũi với thụ thể, không có yếu tố nào trong số này được xem xét.
    3.  **Bỏ qua Vận chuyển**: Nó hoàn toàn bỏ qua quá trình vật lý của sự vận chuyển trong khí quyển.
- **Mức độ tin cậy**: **Rất Thấp**. Proxy này không đo lường phơi nhiễm ngược gió. Nó chỉ là một chỉ số về mật độ phát thải tại địa phương. Do đó, nó không phù hợp với mục đích đã nêu.

### Khuyến nghị

1.  **Sửa đổi cách tiếp cận hiện tại**: Cần phải làm cho công thức này trở nên động. Thay vì một tổng tĩnh, chỉ số phơi nhiễm nên được tính toán trong một vùng đệm (buffer) phía trên gió, với hình dạng và kích thước của vùng đệm này thay đổi theo hướng gió và tốc độ gió. Ví dụ, với gió Bắc mạnh, vùng đệm sẽ là một hình nón hẹp kéo dài về phía Bắc. Với gió nhẹ và hay thay đổi, vùng đệm có thể là một hình tròn.
2.  **Cách tiếp cận thay thế (Được khuyến nghị mạnh mẽ)**: Sử dụng mô hình quỹ đạo ngược (back-trajectory model) như HYSPLIT. Bằng cách chạy các quỹ đạo ngược từ Hà Nội, có thể xác định các khu vực mà khối không khí đã đi qua trong 24-72 giờ trước đó. Sau đó, chỉ số phơi nhiễm có thể được tính bằng cách chồng lớp các quỹ đạo này lên bản đồ mật độ phát thải (ví dụ, từ bộ dữ liệu EDGAR). Phương pháp này, được gọi là Phân tích Tiềm năng Nguồn gốc (Potential Source Contribution Function - PSCF), là một kỹ thuật tiêu chuẩn trong nghiên cứu chất lượng không khí.
3.  **Chiến lược xác thực**: Kết quả từ proxy (dù được sửa đổi hay thay thế) có thể được so sánh với kết quả từ các nghiên cứu phân bổ nguồn sử dụng mô hình hóa học-vận chuyển (CTM) hoặc mô hình receptor (PMF) cho khu vực Hà Nội. Mục tiêu là để xem liệu proxy có thể tái tạo lại một cách hợp lý tỷ lệ đóng góp tương đối của các khu vực nguồn khác nhau hay không.

---

## Kết luận và Tóm tắt Khuyến nghị

Phân tích này cho thấy các proxy hiện tại có mức độ tin cậy khác nhau, từ **Rất Thấp** (Phơi nhiễm Ngược gió) đến **Trung bình** (Độ ổn định Khí quyển). Một chủ đề chung là các proxy hiện tại có xu hướng là các công thức tĩnh, đơn giản hóa quá mức, nắm bắt được các mối quan hệ định tính nhưng thiếu cơ sở vật lý và độ chính xác định lượng. Proxy Phơi nhiễm Ngược gió có sai sót cơ bản nhất vì nó không đo lường hiện tượng mà nó định mô tả.

| Proxy | Mức độ Tin cậy Hiện tại | Khuyến nghị Chính | 
| :--- | :--- | :--- | 
| PBLH | Thấp đến Trung bình | Chuyển sang các tham số hóa riêng biệt cho ngày/đêm hoặc sử dụng đầu ra từ mô hình tái phân tích (ví dụ: ERA5) đã được hiệu chỉnh. | 
| Độ ổn định Khí quyển | Trung bình | Sửa đổi sơ đồ Pasquill-Gifford để tính đến hiệu ứng đảo nhiệt đô thị (UHI). | 
| Nước lỏng trong Sol khí (ALW) | Thấp | Kết hợp sự phụ thuộc vào nồng độ khối lượng PM2.5 và sử dụng một hàm phi tuyến của RH. | 
| Phát hiện Đợt không khí lạnh | Thấp đến Trung bình | Định nghĩa lại proxy dựa trên *sự thay đổi* của nhiệt độ và áp suất trong 24 giờ. | 
| Phơi nhiễm Ngược gió | Rất Thấp | Thay thế hoàn toàn bằng một phương pháp dựa trên quỹ đạo ngược (ví dụ: HYSPLIT/PSCF). | 

Việc thực hiện các khuyến nghị này sẽ cải thiện đáng kể độ tin cậy khoa học và độ chính xác của các proxy trong Đồ thị Tri thức, dẫn đến sự hiểu biết sâu sắc hơn về các yếu tố điều khiển chất lượng không khí ở Hà Nội.

---

## Tài liệu tham khảo

[1] Su, T., Li, Z., & Kahn, R. (2018). Relationships between the planetary boundary layer height and surface pollutants derived from lidar observations over China: regional pattern and influencing factors. *Atmospheric Chemistry and Physics, 18*(21), 15921-15935. [https://doi.org/10.5194/acp-18-15921-2018](https://doi.org/10.5194/acp-18-15921-2018)

[2] Ngoc, B. A. P., Delbarre, H., Deboudt, K., Dieudonné, E., Tran, D. N., Thanh, S. L., ... & Ravetta, F. (2021). Key factors explaining severe air pollution episodes in Hanoi during 2019 winter season. *Atmospheric Pollution Research, 12*(6), 101068. [https://doi.org/10.1016/j.apr.2021.101068](https://doi.org/10.1016/j.apr.2021.101068)

[3] Arya, S. P. S. (1981). Parameterizing the height of the stable atmospheric boundary layer. *Journal of Applied Meteorology, 20*(10), 1192-1202. [https://doi.org/10.1175/1520-0450(1981)020<1192:PTHOTS>2.0.CO;2](https://doi.org/10.1175/1520-0450(1981)020<1192:PTHOTS>2.0.CO;2)

[4] Pasquill, F. (1961). The estimation of the dispersion of windborne material. *Meteorological Magazine, 90*(1063), 33-49.

[5] U.S. Environmental Protection Agency. (n.d.). *Pasquill Stability Classes*. NOAA ARL. [https://www.ready.noaa.gov/READYpgclass.php](https://www.ready.noaa.gov/READYpgclass.php)

[6] Bian, Y. X., Zhao, C. S., Ma, N., Chen, J., & Xu, W. Y. (2014). A study of aerosol liquid water content based on hygroscopicity measurements at high relative humidity in the North China Plain. *Atmospheric Chemistry and Physics, 14*(12), 6417-6426. [https://doi.org/10.5194/acp-14-6417-2014](https://doi.org/10.5194/acp-14-6417-2014)

[7] Kreidenweis, S. M., Petters, M. D., & DeMott, P. J. (2008). Single-parameter estimates of aerosol water content. *Environmental Research Letters, 3*(3), 035002. [https://doi.org/10.1088/1748-9326/3/3/035002](https://doi.org/10.1088/1748-9326/3/3/035002)

[8] Abdillah, M. R., Kanno, Y., Iwasaki, T., & Matsumoto, J. (2021). Cold Surge Pathways in East Asia and Their Tropical Impacts. *Journal of Climate, 34*(1), 157-170. [https://doi.org/10.1175/JCLI-D-20-0552.1](https://doi.org/10.1175/JCLI-D-20-0552.1)

[9] Wongsaming, P., & Exell, R. H. B. (2011). Criteria for Forecasting Cold Surges Associated with Strong High Pressure Areas over Thailand during the Winter Monsoon. *Journal of Sustainable Energy & Environment, 2*, 145-156.

[10] Kim, E., Kim, B. U., Kim, H. C., & Kim, S. (2021). Direct and cross impacts of upwind emission control on downwind PM2.5 under various NH3 conditions in Northeast Asia. *Environmental Pollution, 268*, 115794. [https://doi.org/10.1016/j.envpol.2020.115794](https://doi.org/10.1016/j.envpol.2020.115794)
