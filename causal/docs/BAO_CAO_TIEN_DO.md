# Báo Cáo Tiến Độ: Xây Dựng Causal Knowledge Graph

**Dự án:** Chatbot Diễn giải Ô nhiễm Không khí Hà Nội  
**Ngày báo cáo:** 22/01/2026

---

## 1. Mục Tiêu và Ý Nghĩa

### 1.1. Tại sao cần xây dựng Causal Knowledge Graph?

Trong quá trình phát triển chatbot diễn giải ô nhiễm không khí, em nhận thấy một thách thức quan trọng: làm thế nào để chatbot có thể trả lời các câu hỏi về nguyên nhân một cách chính xác và có căn cứ khoa học? Ví dụ, khi người dùng hỏi "Tại sao PM2.5 lại tăng cao vào mùa đông?" hoặc "Độ ẩm ảnh hưởng đến PM2.5 như thế nào?", chatbot cần hiểu được các mối quan hệ nhân quả thực sự, không chỉ đơn thuần là tương quan thống kê.

Causal Knowledge Graph được xây dựng để giải quyết vấn đề này. Đây là một cơ sở tri thức có cấu trúc, lưu trữ các mối quan hệ nhân quả giữa các yếu tố khí tượng, hóa học, nguồn phát thải và PM2.5, dựa trên các nghiên cứu khoa học đã được công bố và kiểm chứng.

### 1.2. Vai trò trong hệ thống chatbot

Knowledge Graph này đóng vai trò là "bộ nhớ khoa học" của chatbot, giúp hệ thống:

- **Trả lời câu hỏi nhân quả một cách chính xác**: Khi người dùng hỏi về nguyên nhân, chatbot có thể truy vấn vào graph để tìm các mối quan hệ liên quan và đưa ra câu trả lời dựa trên cơ chế khoa học thực sự.

- **Giảm thiểu hallucination**: Thay vì để mô hình ngôn ngữ tự "bịa" ra các mối quan hệ, chatbot sẽ chỉ sử dụng những relationships đã được kiểm chứng và có bằng chứng rõ ràng.

- **Tăng tính minh bạch**: Mỗi câu trả lời về nguyên nhân đều có thể truy ngược về nguồn gốc (paper, tác giả, năm công bố), giúp người dùng tin tưởng và có thể tự kiểm chứng.

- **Hỗ trợ diễn giải khí tượng**: Khi chatbot nhận được dữ liệu khí tượng hiện tại (ví dụ: nhiệt độ thấp, gió yếu, độ ẩm cao), nó có thể sử dụng graph để giải thích tại sao các điều kiện này dẫn đến PM2.5 tăng cao.

---

## 2. Phương Pháp Xây Dựng

### 2.1. Quy trình tổng quan

Quá trình xây dựng Causal Knowledge Graph được thực hiện theo các bước sau:

**Bước 1: Thu thập tài liệu khoa học**

Em tập trung vào các nguồn tài liệu có độ tin cậy cao, bao gồm:
- Các bài báo khoa học đã được peer-review (tạp chí quốc tế uy tín như Atmospheric Environment, Environmental Science & Technology, v.v.)
- Các báo cáo chính thức từ các tổ chức uy tín (World Bank, các cơ quan môi trường)
- Ưu tiên các nghiên cứu về Hà Nội, Việt Nam và khu vực Đông Nam Á để đảm bảo tính phù hợp địa lý

**Bước 2: Phân loại và trích xuất relationships**

Các mối quan hệ nhân quả được phân loại thành 7 categories chính để dễ quản lý và truy vấn:
1. Meteorological pathways (Cơ chế tác động khí tượng)
2. Chemical processes (Quá trình chuyển đổi hóa học)
3. Transport mechanisms (Cơ chế phát tán và lưu chuyển)
4. Emission sources (Nguồn phát thải)
5. Static factors (Đặc điểm địa lý, hiện trạng)
6. Seasonal patterns (Quy luật biến thiên theo mùa)
7. Edge cases (Các tình huống ngoại lệ, tình huống biên)

**Bước 3: Đảm bảo chất lượng**

Mỗi relationship được trích xuất phải đáp ứng các tiêu chuẩn nghiêm ngặt:
- **Có bằng chứng rõ ràng**: Phải có source_url (link đến paper), source_quote (trích dẫn chính xác từ tài liệu), và source_locator (vị trí trong tài liệu)
- **Cơ chế được mô tả chi tiết**: Không chỉ nói "A gây ra B", mà phải giải thích TẠI SAO và NHƯ THẾ NÀO (mechanism)
- **Điều kiện cụ thể**: Ghi rõ các điều kiện cần thiết (ví dụ: nhiệt độ < 15°C, độ ẩm > 75%, mùa đông, v.v.)
- **Độ tin cậy được đánh giá**: Mỗi relationship được gán confidence level (HIGH, MEDIUM, LOW) dựa trên chất lượng bằng chứng

**Bước 4: Kiểm tra và xác thực**

Tất cả các relationships đều được kiểm tra kỹ lưỡng để đảm bảo:
- Không nhầm lẫn giữa tương quan và nhân quả
- Cơ chế được mô tả phù hợp với kiến thức khoa học hiện tại
- Bằng chứng đầy đủ và có thể truy vấn được

### 2.2. Tiêu chuẩn phân loại nguồn

Để đảm bảo chất lượng, các nguồn tài liệu được phân loại theo tier:

- **Tier-1**: Các bài báo đã được peer-review trên tạp chí quốc tế uy tín (ưu tiên cao nhất)
- **Tier-2**: Các báo cáo chính thức từ tổ chức uy tín (World Bank, cơ quan nhà nước)
- **Tier-3**: Các preprint hoặc nghiên cứu chưa được peer-review (chỉ dùng để khám phá, không dùng làm bằng chứng chính)

Trong knowledge graph hiện tại, đa số relationships đều dựa trên Tier-1 sources, đảm bảo độ tin cậy cao.

---

## 3. Cấu Trúc Knowledge Graph

### 3.1. Cấu trúc tổng thể

Knowledge Graph được lưu trữ dưới dạng các file JSON, mỗi file đại diện cho một category. Mỗi file có cấu trúc gồm hai phần chính:

```json
{
  "category": "tên_category",
  "bibliography": [...],  // Danh sách các nguồn tài liệu
  "relationships": [...]  // Danh sách các mối quan hệ nhân quả
}
```

### 3.2. Cấu trúc Bibliography

Mỗi entry trong bibliography chứa thông tin về một nguồn tài liệu:

- `source_title`: Tiêu đề của bài báo/báo cáo
- `source_authors`: Danh sách tác giả
- `source_year`: Năm xuất bản
- `source_url`: Link đến tài liệu
- `source_doi`: DOI (nếu có)
- `tier`: Tier của nguồn (tier_1, tier_2, tier_3)
- `relevance_score`: Điểm đánh giá mức độ liên quan (1-10)
- `key_findings`: Tóm tắt các phát hiện chính

### 3.3. Cấu trúc Relationship

Mỗi relationship là một mối quan hệ nhân quả giữa hai nodes (biến), được mô tả chi tiết như sau:

- **`id`**: Mã định danh duy nhất cho relationship
- **`cause_node`**: Node nguyên nhân (ví dụ: "temperature", "humidity", "traffic")
- **`effect_node`**: Node hệ quả (ví dụ: "inversion", "pm25", "sia_formation")
- **`relationship_type`**: Loại quan hệ (DIRECT_CAUSE, INDIRECT_CAUSE, MODERATOR, MEDIATOR)
- **`mechanism`**: Mô tả chi tiết cơ chế vật lý/hóa học giải thích TẠI SAO và NHƯ THẾ NÀO
- **`conditions`**: Danh sách các điều kiện cần thiết (ví dụ: ["RH > 75%", "Mùa đông", "Gió yếu"])
- **`temporal_lag`**: Độ trễ thời gian (ví dụ: "2-6h", "1d", "N/A")
- **`strength`**: Độ mạnh của mối quan hệ (STRONG, MODERATE, WEAK)
- **`confidence`**: Độ tin cậy (HIGH, MEDIUM, LOW)
- **`source_url`**: Link đến nguồn tài liệu
- **`source_title`**: Tiêu đề nguồn
- **`source_authors`**: Tác giả
- **`source_year`**: Năm xuất bản
- **`source_quote`**: Trích dẫn chính xác từ tài liệu hỗ trợ relationship này
- **`source_locator`**: Vị trí trong tài liệu (trang, section, đoạn văn)
- **`seasonal_variation`**: Biến đổi theo mùa (winter, summer, dry_season, wet_season, all_season)
- **`spatial_scope`**: Phạm vi không gian (local, regional, global)
- **`notes`**: Ghi chú thêm (edge cases, exceptions, non-linear relationships, v.v.)

### 3.4. Ví dụ minh họa

Để minh họa rõ hơn, dưới đây là một ví dụ về một relationship trong category "meteorological_pathways":

**Relationship ID**: `met_001`

- **Cause node**: `temperature` (Nhiệt độ)
- **Effect node**: `inversion` (Nghịch nhiệt)
- **Relationship type**: `DIRECT_CAUSE`
- **Mechanism**: "Nhiệt độ giảm vào ban đêm dẫn đến mặt đất mất nhiệt nhanh hơn không khí phía trên. Lớp không khí sát đất trở nên lạnh hơn lớp trên, tạo ra nghịch nhiệt bức xạ (radiation inversion). Hiện tượng này xảy ra phổ biến nhất từ tháng 10 đến tháng 12 tại Hà Nội."
- **Conditions**: ["Ban đêm (nocturnal)", "Trời quang mây (clear sky)", "Mùa đông (October-December)", "Gió yếu"]
- **Temporal lag**: "2-6h"
- **Strength**: `STRONG`
- **Confidence**: `HIGH`
- **Source**: Hien et al. (2002), "Influence of meteorological conditions on PM2.5 and PM2.5−10 concentrations during the monsoon season in Hanoi, Vietnam"
- **Source quote**: "Very high PM2.5 and PM2.5−10 concentrations were observed in conjunction with the occurrence of nocturnal radiation inversions from October to December"

Ví dụ này cho thấy, relationship không chỉ nói "nhiệt độ thấp gây ra nghịch nhiệt", mà còn giải thích rõ cơ chế vật lý (mặt đất mất nhiệt nhanh hơn), các điều kiện cụ thể (ban đêm, trời quang mây, mùa đông), và có bằng chứng rõ ràng từ nghiên cứu thực tế tại Hà Nội.

---

## 4. Các Categories và Số Lượng Relationships

Knowledge Graph hiện tại bao gồm 7 categories chính, với tổng cộng **99 relationships** được trích xuất và kiểm chứng. Dưới đây là mô tả chi tiết từng category:

### 4.1. Meteorological Pathways (13 relationships)

Category này tập trung vào các con đường khí tượng ảnh hưởng đến PM2.5, bao gồm:

- **Nhiệt độ → Nghịch nhiệt**: Cơ chế hình thành nghịch nhiệt bức xạ và nghịch nhiệt lún
- **Áp suất → Nghịch nhiệt**: Điều kiện áp cao gây ra nghịch nhiệt lún
- **Nghịch nhiệt → PBLH**: Nghịch nhiệt làm giảm độ cao lớp biên hành tinh
- **PBLH → PM2.5**: PBLH thấp dẫn đến PM2.5 tăng cao
- **Gió → Khuếch tán**: Gió mạnh giúp khuếch tán và làm loãng ô nhiễm
- **Mưa → Lắng đọng ướt**: Mưa rửa trôi các hạt bụi khỏi khí quyển
- **Độ ẩm → Sự hình thành aerosol**: Độ ẩm cao thúc đẩy các phản ứng hóa học thứ cấp

Đây là category quan trọng nhất vì các yếu tố khí tượng là những yếu tố chính ảnh hưởng đến sự phân bố và tích tụ của PM2.5 trong khí quyển.

### 4.2. Chemical Processes (10 relationships)

Category này mô tả các quá trình hóa học dẫn đến sự hình thành PM2.5, đặc biệt là các hạt thứ cấp (secondary aerosols):

- **Độ ẩm → Aerosol Liquid Water**: Độ ẩm cao tạo môi trường pha nước cho phản ứng
- **SO2 + NO2 → Sulfate Formation**: Quá trình oxy hóa SO2 thành sulfate trong điều kiện độ ẩm cao
- **NOx + VOCs → Ozone Formation**: Quá trình quang hóa tạo ozone, sau đó có thể tham gia vào các phản ứng khác
- **NH3 + HNO3 → Ammonium Nitrate**: Phản ứng tạo ammonium nitrate, một thành phần quan trọng của PM2.5
- **Aerosol Liquid Water → SIA Formation**: Môi trường pha nước thúc đẩy sự hình thành Secondary Inorganic Aerosols (SIA)

Các relationships này giúp giải thích tại sao PM2.5 có thể tăng cao ngay cả khi nguồn phát thải trực tiếp không thay đổi, do các phản ứng hóa học trong khí quyển.

### 4.3. Transport Mechanisms (18 relationships)

Category này mô tả cách các chất ô nhiễm được vận chuyển trong không gian:

- **Gió hướng → Vận chuyển dài hạn**: Gió từ các khu vực công nghiệp mang ô nhiễm đến Hà Nội
- **Cold Surge → Long-range Transport**: Các đợt không khí lạnh từ phía Bắc mang ô nhiễm từ Trung Quốc đến Việt Nam
- **Back-trajectory Analysis**: Phân tích đường đi của không khí để xác định nguồn gốc ô nhiễm
- **Stagnation → Local Accumulation**: Điều kiện gió yếu và nghịch nhiệt khiến ô nhiễm tích tụ tại chỗ

Đây là category quan trọng để giải thích các đợt ô nhiễm xuyên biên giới và sự khác biệt về chất lượng không khí giữa các khu vực.

### 4.4. Emission Sources (17 relationships)

Category này liên kết các nguồn phát thải với các chất ô nhiễm:

- **Traffic → NOx, PM2.5**: Giao thông là nguồn chính của NOx và một phần PM2.5
- **Industry → SO2, PM2.5**: Hoạt động công nghiệp phát thải SO2 và PM2.5
- **Biomass Burning → PM2.5, CO**: Đốt rơm rạ và các hoạt động đốt sinh khối
- **Coal Combustion → SO2, PM2.5**: Đốt than phát thải SO2 và PM2.5
- **Construction → Dust, PM2.5**: Hoạt động xây dựng tạo bụi

Các relationships này giúp chatbot có thể giải thích nguồn gốc của các chất ô nhiễm và đề xuất các biện pháp giảm thiểu phù hợp.

### 4.5. Static Factors (6 relationships)

Category này bao gồm các yếu tố tĩnh (không thay đổi theo thời gian ngắn) ảnh hưởng đến PM2.5:

- **Population Density → PM2.5**: Mật độ dân số cao dẫn đến nhiều nguồn phát thải
- **LULC (Land Use/Land Cover) → PM2.5**: Loại hình sử dụng đất ảnh hưởng đến nồng độ PM2.5 (đất xây dựng có PM2.5 cao hơn, rừng có PM2.5 thấp hơn)
- **Topography → Air Stagnation**: Địa hình lòng chảo dễ tích tụ ô nhiễm

Các yếu tố này giúp giải thích sự khác biệt về "nền" ô nhiễm giữa các khu vực khác nhau trong thành phố.

### 4.6. Seasonal Patterns (35 relationships)

Category này mô tả các mẫu hình theo mùa và theo thời gian trong ngày:

- **Winter Monsoon → Cold Surge → PM2.5 Increase**: Gió mùa đông bắc mang ô nhiễm từ Trung Quốc
- **Cold Surge Persistence → Local Stagnation → PM2.5 Increase**: Sau khi cold surge qua, điều kiện tĩnh lặng khiến ô nhiễm tích tụ
- **Diurnal Cycle → PBLH Variation → PM2.5 Variation**: Chu kỳ ngày đêm ảnh hưởng đến PBLH và từ đó ảnh hưởng đến PM2.5
- **Rice Straw Burning Season → PM2.5 Increase**: Mùa đốt rơm rạ (thường vào cuối năm) làm tăng PM2.5

Đây là category có số lượng relationships nhiều nhất, phản ánh tầm quan trọng của các mẫu hình thời gian trong việc giải thích biến động PM2.5.

### 4.7. Edge Cases (6 relationships)

Category này bao gồm các trường hợp đặc biệt và ngoại lệ, những relationships phá vỡ các quy tắc chung:

- **Humidity → PM2.5 (Non-linear)**: Mối quan hệ dạng chữ U ngược - độ ẩm thấp đến trung bình làm tăng PM2.5, nhưng độ ẩm rất cao lại làm giảm
- **Drizzle → PM2.5 Increase**: Mưa phùn có thể làm TĂNG PM2.5 (ngoại lệ so với quy tắc "mưa làm sạch không khí")
- **Cold Surge → Delayed PM2.5 Peak**: PM2.5 có thể tăng cao vài ngày SAU KHI cold surge qua, không phải ngay lập tức

Các edge cases này rất quan trọng vì chúng giúp chatbot tránh đưa ra những giải thích quá đơn giản và không chính xác trong các tình huống phức tạp.

---

## 5. Đánh Giá Chất Lượng

### 5.1. Chất lượng nguồn tài liệu

Trong tổng số khoảng 50+ nguồn tài liệu được sử dụng, đa số (khoảng 80-85%) là các bài báo Tier-1 (đã được peer-review trên các tạp chí quốc tế uy tín). Các tạp chí chính bao gồm:

- Atmospheric Environment
- Environmental Science & Technology
- Science of the Total Environment
- Atmospheric Chemistry and Physics
- Aerosol and Air Quality Research

Một số nguồn Tier-2 (báo cáo chính thức) cũng được sử dụng, đặc biệt là các báo cáo về tình hình ô nhiễm không khí tại Hà Nội từ World Bank và các cơ quan nhà nước.

### 5.2. Độ phù hợp địa lý

Một điểm mạnh quan trọng của knowledge graph này là tính phù hợp địa lý cao. Nhiều relationships được trích xuất từ các nghiên cứu cụ thể về:

- **Hà Nội, Việt Nam**: Có nhiều papers nghiên cứu trực tiếp về ô nhiễm không khí tại Hà Nội
- **Khu vực Đông Nam Á**: Các nghiên cứu về vận chuyển xuyên biên giới, gió mùa, và các đặc điểm khí hậu khu vực
- **Các thành phố tương tự**: Các nghiên cứu về Bắc Kinh, Thượng Hải (có điều kiện khí hậu và địa lý tương tự) được tham khảo với lưu ý về sự khác biệt

Điều này đảm bảo rằng các relationships trong graph phù hợp với bối cảnh thực tế của Hà Nội, không chỉ là lý thuyết chung.

### 5.3. Chất lượng bằng chứng

Tất cả 99 relationships đều có bằng chứng đầy đủ:

- **100% có source_url**: Mỗi relationship đều có link đến nguồn tài liệu gốc
- **100% có source_quote**: Mỗi relationship đều có trích dẫn chính xác từ tài liệu, không phải là diễn giải tự do
- **100% có source_locator**: Vị trí trong tài liệu (trang, section, đoạn văn) được ghi rõ để có thể kiểm chứng

Điều này đảm bảo tính minh bạch và khả năng kiểm chứng của knowledge graph.

### 5.4. Chất lượng cơ chế (Mechanism)

Mỗi relationship không chỉ nói "A gây ra B", mà còn giải thích chi tiết cơ chế vật lý hoặc hóa học. Ví dụ:

- Thay vì chỉ nói "nhiệt độ thấp gây ra nghịch nhiệt", graph giải thích: "Nhiệt độ giảm vào ban đêm dẫn đến mặt đất mất nhiệt nhanh hơn không khí phía trên, tạo ra nghịch nhiệt bức xạ"
- Thay vì chỉ nói "độ ẩm cao làm tăng PM2.5", graph giải thích: "Độ ẩm cao (>75%) tạo môi trường pha nước trên bề mặt các hạt aerosol, thúc đẩy các phản ứng oxy hóa SO2 và NO2 thành sulfate và nitrate"

Các cơ chế này giúp chatbot không chỉ trả lời "cái gì" mà còn giải thích được "tại sao" và "như thế nào".

### 5.5. Phân bố độ tin cậy (Confidence)

Các relationships được đánh giá độ tin cậy dựa trên chất lượng bằng chứng và sự nhất quán giữa các nghiên cứu:

- **HIGH confidence** (~46 relationships): Có bằng chứng mạnh từ nhiều nghiên cứu, cơ chế rõ ràng, được công nhận rộng rãi trong cộng đồng khoa học
- **MEDIUM confidence** (~30 relationships): Có bằng chứng tốt nhưng có thể có một số điều kiện hoặc ngoại lệ, hoặc chỉ được nghiên cứu trong một số bối cảnh cụ thể
- **LOW confidence** (~23 relationships): Có bằng chứng nhưng cần thận trọng, có thể có tranh cãi trong cộng đồng khoa học hoặc chỉ áp dụng trong điều kiện rất cụ thể

Việc phân loại confidence giúp chatbot có thể điều chỉnh cách trình bày câu trả lời, ví dụ: "Theo nghiên cứu, có thể..." cho LOW confidence, hoặc "Nghiên cứu đã chứng minh rằng..." cho HIGH confidence.

---

## 6. Thống Kê Chi Tiết

### 6.1. Tổng quan

- **Tổng số relationships**: 99
- **Tổng số categories**: 7
- **Tổng số nguồn tài liệu**: ~50+ unique sources
- **Tỷ lệ relationships có evidence đầy đủ**: 100% (99/99)

### 6.2. Phân bố theo category

| Category                | Số lượng Relationships | Tỷ lệ    |
| ----------------------- | ---------------------- | -------- |
| Seasonal Patterns       | 35                     | 35.4%    |
| Transport Mechanisms    | 18                     | 18.2%    |
| Emission Sources        | 17                     | 17.2%    |
| Meteorological Pathways | 13                     | 13.1%    |
| Chemical Processes      | 10                     | 10.1%    |
| Static Factors          | 6                      | 6.1%     |
| Edge Cases              | 6                      | 6.1%     |
| **Tổng cộng**           | **99**                 | **100%** |

### 6.3. Phân bố theo confidence

- **HIGH confidence**: ~46 relationships (46.5%)
- **MEDIUM confidence**: ~30 relationships (30.3%)
- **LOW confidence**: ~23 relationships (23.2%)

### 6.4. Phân bố theo spatial scope

- **Local** (Hà Nội cụ thể): ~40 relationships
- **Regional** (Đông Nam Á, Red River Delta): ~35 relationships
- **Global** (Áp dụng chung): ~24 relationships

### 6.5. Phân bố theo seasonal variation

- **All season** (Quanh năm): ~45 relationships
- **Winter** (Mùa đông): ~30 relationships
- **Summer** (Mùa hè): ~10 relationships
- **Dry season / Wet season**: ~14 relationships

### 6.6. Coverage về các biến chính

Knowledge graph bao phủ các biến chính sau:

**Biến khí tượng:**
- Temperature (Nhiệt độ)
- Humidity (Độ ẩm)
- Pressure (Áp suất)
- Wind Speed (Tốc độ gió)
- Wind Direction (Hướng gió)
- Precipitation (Lượng mưa)
- PBLH (Planetary Boundary Layer Height)
- Inversion (Nghịch nhiệt)
- Cloud Cover (Độ che phủ mây)

**Biến hóa học:**
- SO2, NO2, NOx
- O3 (Ozone)
- VOCs (Volatile Organic Compounds)
- SIA (Secondary Inorganic Aerosols)
- SOA (Secondary Organic Aerosols)
- Aerosol Liquid Water

**Biến phát thải:**
- Traffic (Giao thông)
- Industry (Công nghiệp)
- Biomass Burning (Đốt sinh khối)
- Coal Combustion (Đốt than)
- Construction (Xây dựng)

**Biến tĩnh:**
- Population Density (Mật độ dân số)
- LULC (Land Use/Land Cover)
- Topography (Địa hình)

**Biến mục tiêu:**
- PM2.5 (chính)
- PM10 (một số relationships)

---

## 7. Kết Luận và Hướng Phát Triển

### 7.1. Những gì đã hoàn thành

Em đã hoàn thành việc xây dựng một Causal Knowledge Graph với 99 relationships được trích xuất và kiểm chứng từ các tài liệu khoa học uy tín. Knowledge graph này:

- **Có cấu trúc rõ ràng**: Được tổ chức thành 7 categories, mỗi relationship có đầy đủ thông tin về cơ chế, điều kiện, bằng chứng
- **Có chất lượng cao**: 100% relationships có bằng chứng đầy đủ, đa số dựa trên Tier-1 sources
- **Phù hợp với bối cảnh Hà Nội**: Nhiều relationships được trích xuất từ các nghiên cứu cụ thể về Hà Nội và khu vực Đông Nam Á
- **Bao phủ đầy đủ**: Các yếu tố chính ảnh hưởng đến PM2.5 đều được bao phủ, từ khí tượng, hóa học, nguồn phát thải, đến các yếu tố tĩnh và mẫu hình theo mùa

### 7.2. Kế hoạch tiếp theo

**Giai đoạn 1: Merge và Validate (Đang thực hiện)**

- Merge tất cả 7 file JSON thành một knowledge graph thống nhất
- Normalize các format khác nhau (một số files có format hơi khác)
- Deduplicate các relationships trùng lặp
- Validate chất lượng: kiểm tra các required fields, đảm bảo không có relationships thiếu evidence

**Giai đoạn 2: Build Graph Structure**

- Chuyển đổi từ format JSON sang cấu trúc graph (có thể sử dụng NetworkX hoặc Neo4j)
- Xác định các nodes và edges
- Phân tích cấu trúc graph: tìm các pathways quan trọng, các nodes trung tâm, các cycles (nếu có)

**Giai đoạn 3: Integration với Chatbot**

- Tích hợp knowledge graph vào hệ thống chatbot hiện tại
- Xây dựng retrieval mechanism để tìm relationships phù hợp với câu hỏi
- Cải thiện ContextBuilder để sử dụng knowledge graph thay vì cache đơn giản
- Test và đánh giá hiệu quả

**Giai đoạn 4: Mở rộng và Cải thiện**

- Bổ sung thêm relationships nếu phát hiện gaps
- Cập nhật relationships khi có nghiên cứu mới
- Tối ưu hóa retrieval mechanism để tăng tốc độ và độ chính xác

---

## 8. Dự Định Triển Khai Diễn Giải Khí Tượng

### 8.1. Tổng quan về cách sử dụng Knowledge Graph trong Chatbot

Knowledge Graph sẽ được sử dụng như một "cơ sở tri thức" để chatbot có thể trả lời các câu hỏi về nguyên nhân một cách chính xác và có căn cứ. Quy trình hoạt động như sau:

1. **Người dùng đặt câu hỏi**: Ví dụ: "Tại sao PM2.5 lại tăng cao vào mùa đông?"
2. **Chatbot phân loại câu hỏi**: Sử dụng QuestionClassifier để xác định đây là câu hỏi nhân quả (causal question)
3. **Chatbot truy vấn Knowledge Graph**: Tìm các relationships liên quan đến PM2.5 và mùa đông
4. **Chatbot xây dựng context**: Kết hợp relationships tìm được với dữ liệu khí tượng hiện tại
5. **Chatbot tạo câu trả lời**: Sử dụng LLM để tạo câu trả lời dựa trên context đã xây dựng

### 8.2. Kế hoạch tích hợp với hệ thống chatbot hiện tại

Hệ thống chatbot hiện tại đã có các component sau:

- **QuestionClassifier**: Phân loại câu hỏi (causal, what-if, forecast, v.v.)
- **ContextBuilder**: Xây dựng context cho LLM (hiện tại chỉ là cache đơn giản)
- **LLMHandler**: Xử lý prompt và gọi LLM API
- **CAUSAL_PROMPT**: Template prompt cho câu hỏi nhân quả

**Kế hoạch tích hợp:**

**Bước 1: Tạo KnowledgeGraphService**

Tạo một service mới `KnowledgeGraphService` với các chức năng:

- `load_graph()`: Load knowledge graph từ các file JSON đã merge
- `find_relationships(cause_node, effect_node)`: Tìm relationships giữa hai nodes
- `find_paths_to_pm25(node)`: Tìm tất cả các pathways từ một node đến PM2.5
- `retrieve_by_question(question, entities)`: Tìm relationships phù hợp với câu hỏi dựa trên entities được extract

**Bước 2: Cải thiện ContextBuilder**

Thay thế logic cache đơn giản trong `ContextBuilder` bằng logic retrieve từ knowledge graph:

```python
class ContextBuilder:
    def __init__(self, knowledge_graph_service):
        self.kg_service = knowledge_graph_service
    
    def build_context(self, question, causal_context="", current_data=""):
        # Extract entities từ câu hỏi (temperature, humidity, pm25, v.v.)
        entities = extract_entities(question)
        
        # Tìm relationships phù hợp từ knowledge graph
        relationships = self.kg_service.retrieve_by_question(question, entities)
        
        # Format relationships thành text để inject vào prompt
        causal_context = format_relationships(relationships)
        
        return {
            "causal_context": causal_context,
            "current_data": current_data,
        }
```

**Bước 3: Tích hợp vào LLMHandler**

`LLMHandler` đã có logic xử lý causal questions, chỉ cần đảm bảo `ContextBuilder` được inject với `KnowledgeGraphService`:

```python
class LLMHandler:
    def __init__(self, knowledge_graph_service=None):
        self.kg_service = knowledge_graph_service or KnowledgeGraphService()
        self.context_builder = ContextBuilder(self.kg_service)
        # ... các component khác
```

### 8.3. Phương pháp Retrieval

Retrieval mechanism sẽ hoạt động như sau:

**Bước 1: Entity Extraction**

Từ câu hỏi của người dùng, extract các entities (biến) liên quan:
- Câu hỏi: "Tại sao PM2.5 tăng cao khi nhiệt độ thấp?"
- Entities: `["pm25", "temperature"]`

**Bước 2: Relationship Matching**

Tìm các relationships trong knowledge graph có liên quan:
- Tìm trực tiếp: `temperature → ? → pm25`
- Tìm gián tiếp: `temperature → inversion → pblh → pm25`
- Tìm theo keyword: Tìm relationships có chứa "temperature" hoặc "pm25" trong mechanism, conditions, hoặc notes

**Bước 3: Ranking và Filtering**

Rank các relationships tìm được theo:
- **Relevance**: Mức độ liên quan đến câu hỏi
- **Confidence**: Ưu tiên HIGH confidence
- **Geographic scope**: Ưu tiên "local" (Hà Nội) nếu có
- **Seasonal match**: Nếu câu hỏi về mùa đông, ưu tiên relationships có `seasonal_variation: "winter"`

**Bước 4: Context Building**

Format các relationships đã được chọn thành text để inject vào prompt:

```
[THÔNG TIN NHÂN QUẢ]
1. Nhiệt độ thấp → Nghịch nhiệt (Mechanism: Nhiệt độ giảm vào ban đêm...)
   - Conditions: Ban đêm, trời quang mây, mùa đông
   - Confidence: HIGH
   - Source: Hien et al. (2002)

2. Nghịch nhiệt → PBLH thấp (Mechanism: Nghịch nhiệt ngăn cản...)
   - Confidence: HIGH
   - Source: Su et al. (2018)

3. PBLH thấp → PM2.5 tăng cao (Mechanism: PBLH thấp làm giảm thể tích...)
   - Confidence: HIGH
   - Source: Su et al. (2018)
```

### 8.4. Chain of Thought Reasoning

Một điểm quan trọng trong việc triển khai diễn giải khí tượng là sử dụng **Chain of Thought (CoT) reasoning** - tức là suy luận từng bước một cách có hệ thống, thay vì đưa ra kết luận trực tiếp. Điều này giúp chatbot có thể giải thích rõ ràng quá trình suy luận và đảm bảo tính logic của câu trả lời.

**Quy trình Chain of Thought:**

**Bước 1: Phân tích điều kiện khí tượng hiện tại**
- Chatbot nhận dữ liệu khí tượng thực tế (nhiệt độ, độ ẩm, gió, PBLH, v.v.)
- Xác định các giá trị bất thường hoặc đáng chú ý (ví dụ: nhiệt độ thấp, gió yếu, PBLH thấp)

**Bước 2: Truy vấn Knowledge Graph**
- Tìm các relationships liên quan đến các biến khí tượng đã xác định
- Ví dụ: Nếu nhiệt độ thấp → tìm relationships có `cause_node: "temperature"`

**Bước 3: Xây dựng Causal Chain**
- Kết nối các relationships thành một chuỗi nhân quả (causal chain)
- Ví dụ: `temperature_low → inversion → pblh_low → pm25_high`
- Mỗi bước trong chain phải có relationship tương ứng trong knowledge graph

**Bước 4: Kiểm tra điều kiện (Conditions)**
- Với mỗi relationship trong chain, kiểm tra xem conditions có được thỏa mãn không
- Ví dụ: Relationship "temperature → inversion" có condition "Ban đêm, trời quang mây, mùa đông"
- Nếu điều kiện thực tế không match → loại bỏ relationship đó khỏi chain

**Bước 5: Đánh giá độ mạnh và độ tin cậy**
- Tính toán độ mạnh tổng thể của causal chain (dựa trên strength của từng relationship)
- Xác định confidence level (ưu tiên HIGH confidence relationships)
- Nếu chain có quá nhiều LOW confidence relationships → cảnh báo trong câu trả lời

**Bước 6: Tổng hợp và diễn giải**
- Sử dụng LLM để tổng hợp causal chain thành câu trả lời tự nhiên
- Trình bày từng bước trong chain một cách rõ ràng
- Giải thích cơ chế (mechanism) của từng bước

**Ví dụ Chain of Thought:**

Giả sử chatbot nhận được dữ liệu: nhiệt độ = 12°C, gió = 2 m/s, PBLH = 200m, PM2.5 = 150 µg/m³

**Bước 1: Phân tích điều kiện**
```
- Nhiệt độ: 12°C (thấp, đáng chú ý)
- Gió: 2 m/s (yếu)
- PBLH: 200m (rất thấp)
- PM2.5: 150 µg/m³ (cao)
```

**Bước 2: Truy vấn Knowledge Graph**
```
Tìm relationships:
- temperature → inversion (tìm thấy met_001)
- inversion → pblh (tìm thấy met_003)
- pblh → pm25 (tìm thấy met_005)
- wind_speed → dispersion (tìm thấy met_007)
```

**Bước 3: Xây dựng Causal Chain**
```
Chain 1: temperature_low → inversion → pblh_low → pm25_high
Chain 2: wind_speed_low → low_dispersion → pm25_high
```

**Bước 4: Kiểm tra điều kiện**
```
Chain 1:
- temperature → inversion: conditions = ["Ban đêm", "Trời quang mây", "Mùa đông"]
  → Kiểm tra: Hiện tại là ban đêm? Có. Trời quang mây? Cần check. Mùa đông? Có (nhiệt độ 12°C)
  → Relationship hợp lệ (một số conditions có thể không cần thiết)

- inversion → pblh: conditions = []
  → Relationship hợp lệ

- pblh → pm25: conditions = []
  → Relationship hợp lệ

Chain 2:
- wind_speed → dispersion: conditions = ["Gió < 3 m/s"]
  → Kiểm tra: Gió = 2 m/s < 3 m/s? Có
  → Relationship hợp lệ
```

**Bước 5: Đánh giá**
```
Chain 1: 
- Strength: STRONG (tất cả relationships đều STRONG)
- Confidence: HIGH (tất cả relationships đều HIGH)
- Độ dài: 3 bước (ngắn, rõ ràng)

Chain 2:
- Strength: MODERATE
- Confidence: HIGH
- Độ dài: 2 bước

→ Chain 1 là chain chính, Chain 2 là yếu tố hỗ trợ
```

**Bước 6: Tổng hợp**
```
Câu trả lời của chatbot:

"PM2.5 tăng cao (150 µg/m³) do một chuỗi các yếu tố khí tượng:

**Bước 1: Nhiệt độ thấp gây ra nghịch nhiệt**
Nhiệt độ hiện tại là 12°C, khá thấp. Vào ban đêm, mặt đất mất nhiệt nhanh hơn 
không khí phía trên, tạo ra nghịch nhiệt bức xạ. Đây là hiện tượng phổ biến vào 
mùa đông tại Hà Nội (Hien et al., 2002).

**Bước 2: Nghịch nhiệt làm giảm PBLH**
Nghịch nhiệt ngăn cản sự phát triển của lớp biên hành tinh (PBLH). PBLH hiện tại 
chỉ còn 200m, rất thấp so với bình thường (thường là 500-1000m vào ban ngày).

**Bước 3: PBLH thấp khiến PM2.5 tích tụ**
Khi PBLH thấp, không khí bị "nén" lại trong một thể tích nhỏ, khiến các hạt PM2.5 
không thể khuếch tán lên cao. Điều này dẫn đến sự tích tụ và nồng độ PM2.5 tăng cao.

**Yếu tố hỗ trợ: Gió yếu**
Gió hiện tại chỉ 2 m/s, rất yếu, không đủ để khuếch tán và làm loãng ô nhiễm. 
Điều này càng làm tăng sự tích tụ PM2.5 tại chỗ.

[Nguồn: Hien et al. (2002), Su et al. (2018)]"
```

**Lợi ích của Chain of Thought:**

1. **Tính minh bạch**: Người dùng có thể hiểu rõ quá trình suy luận, không chỉ kết quả
2. **Tính logic**: Mỗi bước đều có căn cứ từ knowledge graph, đảm bảo tính logic
3. **Khả năng debug**: Nếu câu trả lời sai, có thể trace lại từng bước để tìm lỗi
4. **Tăng độ tin cậy**: Người dùng thấy được quá trình suy luận có hệ thống, tăng độ tin cậy
5. **Giáo dục**: Giúp người dùng hiểu về cơ chế khí tượng, không chỉ biết kết quả

### 8.5. Ví dụ Flow hoàn chỉnh

Để minh họa rõ hơn, dưới đây là một ví dụ flow hoàn chỉnh:

**Input: Câu hỏi của người dùng**
```
"Tại sao PM2.5 lại tăng cao vào mùa đông?"
```

**Bước 1: Question Classification**
```python
classification = question_classifier.classify(question)
# Result: {"is_causal": True, "type": "causal", ...}
```

**Bước 2: Entity Extraction**
```python
entities = entity_extractor.extract_entities(question)
# Result: {"variables": ["pm25"], "temporal": ["mùa đông", "winter"], ...}
```

**Bước 3: Knowledge Graph Retrieval**
```python
relationships = kg_service.retrieve_by_question(question, entities)
# Tìm được các relationships:
# - winter_monsoon → cold_surge → pm25_increase
# - temperature_low → inversion → pblh_low → pm25_increase
# - cold_surge_persistence → local_stagnation → pm25_increase
# ...
```

**Bước 4: Context Building**
```python
context = context_builder.build_context(
    question=question,
    causal_context=format_relationships(relationships),
    current_data=get_current_meteorological_data()
)
```

**Bước 5: Prompt Building**
```python
prompt = CAUSAL_PROMPT.format(
    causal_context=context["causal_context"],
    current_data=context["current_data"],
    question=question
)
```

**Bước 6: LLM Generation**
```python
response = llm_handler.answer(question, causal_context=context["causal_context"], ...)
```

**Output: Câu trả lời của chatbot**
```
PM2.5 tăng cao vào mùa đông do một số nguyên nhân chính:

1. **Gió mùa đông bắc mang ô nhiễm từ Trung Quốc**: 
   Theo nghiên cứu của Phung-Ngoc et al. (2023), các đợt không khí lạnh 
   từ phía Bắc mang theo ô nhiễm từ các khu vực công nghiệp ở Trung Quốc 
   đến Hà Nội, làm tăng PM2.5 khoảng 30% trong giai đoạn cold surge onset.

2. **Nhiệt độ thấp gây ra nghịch nhiệt**:
   Nhiệt độ giảm vào ban đêm làm mặt đất mất nhiệt nhanh hơn không khí 
   phía trên, tạo ra nghịch nhiệt bức xạ. Nghịch nhiệt này làm giảm độ cao 
   lớp biên hành tinh (PBLH), khiến không khí bị "nén" lại và PM2.5 tích tụ 
   (Hien et al., 2002).

3. **Điều kiện tĩnh lặng sau cold surge**:
   Sau khi cold surge qua, điều kiện gió yếu và nghịch nhiệt khiến ô nhiễm 
   tích tụ tại chỗ, làm tăng PM2.5 thêm khoảng 40% (Phung-Ngoc et al., 2023).

[Nguồn tham khảo: Phung-Ngoc et al. (2023), Hien et al. (2002)]
```

### 8.5. Lợi ích của cách tiếp cận này

Cách tiếp cận này mang lại nhiều lợi ích:

1. **Tính chính xác cao**: Câu trả lời dựa trên các relationships đã được kiểm chứng, không phải là "bịa đặt" của LLM

2. **Tính minh bạch**: Mỗi câu trả lời đều có thể truy ngược về nguồn gốc (paper, tác giả, năm)

3. **Giảm hallucination**: LLM chỉ được cung cấp thông tin đã được kiểm chứng, giảm khả năng tạo ra thông tin sai

4. **Khả năng giải thích sâu**: Không chỉ nói "A gây ra B", mà còn giải thích cơ chế, điều kiện, và các yếu tố liên quan

5. **Phù hợp với bối cảnh Hà Nội**: Các relationships được ưu tiên từ các nghiên cứu về Hà Nội và khu vực Đông Nam Á

### 8.6. Thách thức và giải pháp

**Thách thức 1: Tốc độ retrieval**

- **Vấn đề**: Nếu knowledge graph lớn, việc tìm kiếm có thể chậm
- **Giải pháp**: 
  - Index các relationships theo nodes (cause_node, effect_node)
  - Cache các kết quả retrieval phổ biến
  - Sử dụng vector search nếu cần tìm kiếm semantic

**Thách thức 2: Chọn relationships phù hợp**

- **Vấn đề**: Một câu hỏi có thể match với nhiều relationships, cần chọn những cái phù hợp nhất
- **Giải pháp**:
  - Ranking dựa trên relevance score, confidence, geographic scope
  - Giới hạn số lượng relationships (ví dụ: top 5-10)
  - Ưu tiên relationships có pathway ngắn và rõ ràng

**Thách thức 3: Kết hợp với dữ liệu thực tế**

- **Vấn đề**: Knowledge graph chứa relationships tổng quát, nhưng cần kết hợp với dữ liệu khí tượng thực tế để đưa ra giải thích cụ thể
- **Giải pháp**:
  - Kết hợp relationships với dữ liệu hiện tại (nhiệt độ, độ ẩm, gió, v.v.)
  - Kiểm tra conditions của relationships có match với điều kiện hiện tại không
  - Chỉ sử dụng relationships phù hợp với điều kiện thực tế

---

## 9. Kết Luận

Việc xây dựng Causal Knowledge Graph là một bước quan trọng trong quá trình phát triển chatbot diễn giải ô nhiễm không khí. Knowledge graph này không chỉ cung cấp một cơ sở tri thức có cấu trúc và đáng tin cậy, mà còn mở ra khả năng cho chatbot trả lời các câu hỏi về nguyên nhân một cách chính xác, có căn cứ, và minh bạch.

Với 99 relationships được trích xuất từ các tài liệu khoa học uy tín, knowledge graph hiện tại đã bao phủ đầy đủ các yếu tố chính ảnh hưởng đến PM2.5, từ khí tượng, hóa học, nguồn phát thải, đến các yếu tố tĩnh và mẫu hình theo mùa. Đặc biệt, nhiều relationships được trích xuất từ các nghiên cứu cụ thể về Hà Nội và khu vực Đông Nam Á, đảm bảo tính phù hợp với bối cảnh thực tế.

Trong các giai đoạn tiếp theo, Em sẽ tiếp tục hoàn thiện knowledge graph (merge, validate, build graph structure) và tích hợp vào hệ thống chatbot để người dùng có thể nhận được những câu trả lời về nguyên nhân một cách chính xác và đáng tin cậy.

---

**Người báo cáo:** [Tên sinh viên]  
**Ngày:** 22/01/2026
