# Manus Templates - Ready to Use

Các file trong thư mục này là templates sẵn sàng để copy-paste trực tiếp vào Manus web interface.

## Files

### 1. template_01_meteorological.txt
**Dùng cho**: Papers về khí tượng học và ô nhiễm không khí

**Cách dùng**:
1. Mở file này
2. Copy toàn bộ nội dung
3. Paste vào Manus
4. Thay `[Paste đoạn văn bản từ paper cần extract ở đây]` bằng document text thực tế
5. Run extraction

### 2. template_02_chemical.txt
**Dùng cho**: Papers về hóa học khí quyển và aerosol physics

**Cách dùng**: Tương tự template_01

### 3. template_combined_all.txt
**Dùng cho**: Papers cover nhiều aspects (khí tượng + hóa học + transport + etc.)

**Cách dùng**: 
- Dùng khi paper không chỉ tập trung vào một aspect
- Extract tất cả relationships trong một lần
- Output sẽ được phân loại theo categories

### 4. template_auto_discovery.txt
**Dùng cho**: Manus tự tìm papers và extract (End-to-end automation)

**Cách dùng**:
1. Copy template vào Manus
2. Thay `[ĐIỀN TOPIC Ở ĐÂY]` bằng topic cụ thể
3. Ví dụ: "PM2.5 pollution mechanisms in Hanoi, Vietnam"
4. Manus sẽ tự:
   - Tìm papers về topic
   - Extract relationships từ các papers
   - Tổng hợp và validate
5. Nhận final output với tất cả relationships

**Lưu ý**: 
- Manus cần có khả năng web search
- Có thể tốn thời gian và cost nếu Manus dùng API có phí
- Nên review papers được tìm thấy trước khi extract

### 5. template_auto_discovery_simple.txt
**Dùng cho**: Version đơn giản hơn của auto-discovery

**Cách dùng**: Tương tự template_auto_discovery.txt nhưng đơn giản hơn, ít steps hơn

## Workflow đề xuất

### Option 1: Single Template (Đơn giản)
```
1. Chọn template phù hợp với paper
2. Copy template vào Manus
3. Paste document text
4. Run extraction
5. Save JSON output
```

### Option 2: Sequential Extraction (Chất lượng cao)
```
1. Extract với template_01 (Meteorological)
2. Extract với template_02 (Chemical)
3. Extract với template_03 (Transport) - nếu có
4. Merge các JSON outputs lại
```

### Option 3: Combined Template (Nhanh)
```
1. Dùng template_combined_all.txt
2. Paste document text
3. Run extraction một lần
4. Review và validate output
```

### Option 4: Auto-Discovery (End-to-end)
```
1. Dùng template_auto_discovery.txt hoặc template_auto_discovery_simple.txt
2. Điền topic cần tìm kiếm
3. Manus tự tìm papers và extract
4. Review output và papers được tìm thấy
5. Validate relationships
```

## Tips

1. **Nếu document quá dài**: Chia thành sections, extract từng section
2. **Nếu output không đạt**: Thử chia nhỏ document hơn
3. **Nếu extract quá ít**: Check xem có đúng prompt không, thêm examples
4. **Nếu extract quá nhiều correlations**: Nhấn mạnh "CHỈ causal relationships"

## Validation

Sau khi extract, kiểm tra:
- [ ] Output là valid JSON?
- [ ] Có đủ relationships không?
- [ ] Mechanism có rõ ràng không?
- [ ] Conditions có đầy đủ không?
- [ ] Nodes có standardized không?

## Next Steps

Sau khi extract từ Manus:
1. Validate JSON
2. Review relationships
3. Deduplicate
4. Merge với các extractions khác
5. Build knowledge graph
