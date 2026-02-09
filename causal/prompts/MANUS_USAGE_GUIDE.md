# Hướng dẫn Sử dụng Prompts với Manus Web Interface
# Version: 1.0

## Tổng quan

Manus là web interface cho LLM agents, cho phép bạn:
- Load và combine multiple prompts
- Process documents (PDFs, text files)
- Extract structured data (JSON)
- Chain multiple extraction steps

## Cấu trúc Workflow với Manus

### Workflow 1: Single Document Extraction (Đơn giản)

**Khi nào dùng**: Paper chỉ tập trung vào một aspect (ví dụ: chỉ về khí tượng)

**Bước 1: Chọn Prompt phù hợp**
- Paper về khí tượng → Dùng `prompt_01_meteorological_pathways.md`
- Paper về hóa học → Dùng `prompt_02_chemical_processes.md`
- Paper về vận chuyển → Dùng `prompt_03_transport_mechanisms.md`
- Paper về nguồn phát thải → Dùng `prompt_04_emission_sources.md`
- Paper về địa lý/GIS → Dùng `prompt_05_static_factors.md`
- Paper về biến đổi theo mùa → Dùng `prompt_06_seasonal_patterns.md`
- Paper có edge cases → Dùng `prompt_07_edge_cases.md`

**Bước 2: Format Input cho Manus**

Trong Manus, bạn sẽ có một text input box. Format như sau:

```
[Copy toàn bộ nội dung từ prompt file đã chọn]

---

DOCUMENT TEXT:
[Paste đoạn văn bản từ paper cần extract]

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

**Ví dụ cụ thể**:

```
# PROMPT 01: METEOROLOGICAL PATHWAYS
# Focus: Causal relationships giữa các biến khí tượng và PM2.5

## ROLE
Bạn là chuyên gia về khí tượng học và ô nhiễm không khí...

[Copy toàn bộ nội dung prompt_01_meteorological_pathways.md]

---

DOCUMENT TEXT:
Temperature inversions occur when the ground loses heat rapidly at night, 
cooling the air near the surface while upper layers remain warm. This creates 
a stable layer that traps pollutants near the ground. In Hanoi, winter 
temperatures below 15°C combined with clear skies and light winds (< 2 m/s) 
frequently lead to radiation inversions, resulting in low PBLH (< 500m) and 
high PM2.5 concentrations.

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

### Workflow 2: Multi-Aspect Extraction (Phức tạp)

**Khi nào dùng**: Paper cover nhiều aspects (ví dụ: vừa về khí tượng, vừa về hóa học)

**Cách 1: Sequential Extraction (Khuyến nghị)**

**Bước 1**: Extract với Prompt 01 (Meteorological)
- Input: Prompt 01 + Document text
- Output: JSON relationships về khí tượng

**Bước 2**: Extract với Prompt 02 (Chemical)
- Input: Prompt 02 + Document text (cùng document)
- Output: JSON relationships về hóa học

**Bước 3**: Merge kết quả
- Combine các JSON outputs lại

**Cách 2: Combined Prompt (Nâng cao)**

Tạo một combined prompt trong Manus:

```
# COMBINED EXTRACTION PROMPT
# Extract cả Meteorological và Chemical relationships

[Copy ROLE và TASK từ prompt_00_master_template.md]

## EXTRACTION TASKS

### Task 1: Meteorological Pathways
[Copy SPECIFIC FOCUS từ prompt_01_meteorological_pathways.md]
[Copy KEY MECHANISMS từ prompt_01]

### Task 2: Chemical Processes
[Copy SPECIFIC FOCUS từ prompt_02_chemical_processes.md]
[Copy KEY MECHANISMS từ prompt_02]

## OUTPUT FORMAT
Extract relationships cho cả 2 tasks, output JSON với structure:
{
  "meteorological_relationships": [...],
  "chemical_relationships": [...],
  "entities_mentioned": [...],
  "missing_info": "..."
}

---

DOCUMENT TEXT:
[Paste document text]

---

Hãy extract causal relationships cho cả 2 tasks trên.
```

### Workflow 3: Batch Processing (Xử lý nhiều papers)

**Khi nào dùng**: Có nhiều papers cần extract

**Bước 1**: Tạo template prompt trong Manus
- Save prompt template như một "Agent Template" trong Manus

**Bước 2**: Với mỗi paper:
- Load template
- Paste document text
- Run extraction
- Save output JSON

**Bước 3**: Post-processing
- Merge tất cả JSON outputs
- Validate và deduplicate relationships

## Chi tiết Format Input cho Manus

### Template cơ bản:

```
[PROMPT CONTENT]

---

DOCUMENT TEXT:
[Your document text here]

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

### Template với Context:

```
[PROMPT CONTENT]

---

CONTEXT:
- Domain: Air Pollution (PM2.5)
- Location: Hanoi, Vietnam
- Focus: [Meteorological pathways / Chemical processes / etc.]

DOCUMENT TEXT:
[Your document text here]

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

### Template với Examples:

```
[PROMPT CONTENT]

---

EXAMPLES:
[Copy examples từ prompt file]

DOCUMENT TEXT:
[Your document text here]

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa, 
theo đúng format như các examples đã cho.
```

## Best Practices với Manus

### 1. Chia nhỏ Document

**Nếu document quá dài** (> 5000 words):
- Chia thành các sections
- Extract từng section với prompt phù hợp
- Merge kết quả sau

**Ví dụ**:
```
Section 1: Introduction & Methods → Prompt 01 (Meteorological)
Section 2: Results - Chemical Analysis → Prompt 02 (Chemical)
Section 3: Discussion - Transport → Prompt 03 (Transport)
```

### 2. Sử dụng Master Template

**Luôn bắt đầu với Master Template**:
- Copy ROLE, TASK, OUTPUT FORMAT từ `prompt_00_master_template.md`
- Sau đó thêm SPECIFIC FOCUS từ prompt cụ thể

**Format**:
```
[ROLE và TASK từ Master Template]

[SPECIFIC FOCUS từ prompt cụ thể]

[OUTPUT FORMAT từ Master Template]

---

DOCUMENT TEXT:
[Your text]
```

### 3. Validation trong Manus

**Sau khi có output**:
- Kiểm tra JSON format (valid JSON?)
- Kiểm tra có đủ fields không?
- Kiểm tra mechanism có rõ ràng không?
- Kiểm tra confidence có phù hợp không?

**Nếu output không đạt**:
- Thêm examples vào prompt
- Làm rõ requirements
- Chia nhỏ document hơn

### 4. Iterative Refinement

**Workflow**:
1. Extract lần 1 → Review output
2. Identify issues → Refine prompt
3. Extract lần 2 → Review output
4. Repeat until satisfied

## Ví dụ cụ thể: Extract từ một Paper

### Paper: "Temperature Inversion and PM2.5 in Hanoi"

**Bước 1: Chọn Prompt**
→ Prompt 01 (Meteorological Pathways)

**Bước 2: Format Input trong Manus**

```
# PROMPT 01: METEOROLOGICAL PATHWAYS
# Focus: Causal relationships giữa các biến khí tượng và PM2.5

## ROLE
Bạn là chuyên gia về khí tượng học và ô nhiễm không khí, chuyên về các quá trình 
khí tượng ảnh hưởng đến sự tích tụ và khuếch tán của chất ô nhiễm.

## SPECIFIC FOCUS
Extract các causal pathways liên quan đến:
1. Temperature → Inversion → PBLH → PM2.5
2. Wind Speed → Dispersion → PM2.5
...

## KEY MECHANISMS TO LOOK FOR
- Radiation Inversion: Nghịch nhiệt bức xạ (ban đêm, mặt đất mất nhiệt)
...

## EXAMPLES OF GOOD EXTRACTIONS
[Copy examples từ prompt file]

## OUTPUT FORMAT (JSON)
{
  "relationships": [
    {
      "id": "unique_id",
      "cause_node": "temperature",
      "effect_node": "inversion",
      ...
    }
  ],
  ...
}

---

DOCUMENT TEXT:
Temperature inversions in Hanoi occur primarily during winter nights when 
surface temperatures drop below 15°C. Clear skies and light winds (< 2 m/s) 
are necessary conditions. The inversion layer traps pollutants, leading to 
PBLH values below 500m and PM2.5 concentrations exceeding 100 µg/m³. 
This phenomenon is most severe in December and January.

---

Hãy extract causal relationships từ đoạn văn trên theo format JSON đã định nghĩa.
```

**Bước 3: Review Output**

Manus sẽ output JSON. Kiểm tra:
- [ ] Có extract được Temperature → Inversion không?
- [ ] Có extract được Inversion → PBLH không?
- [ ] Có extract được PBLH → PM2.5 không?
- [ ] Conditions có đầy đủ không? (winter, night, clear skies, wind < 2 m/s)
- [ ] Mechanism có rõ ràng không?

## Tips & Tricks

### 1. Sử dụng System Message trong Manus

Nếu Manus có "System Message" field:
- Paste Master Template vào System Message
- Chỉ paste SPECIFIC FOCUS vào User Message

### 2. Tạo Presets/Templates trong Manus

- Save mỗi prompt như một Template
- Tên: "Extract Meteorological", "Extract Chemical", etc.
- Reuse cho các papers khác

### 3. Batch Processing

Nếu Manus hỗ trợ batch:
- Upload nhiều documents
- Apply cùng một prompt template
- Export tất cả JSON outputs

### 4. Post-processing Script

Sau khi extract từ Manus:
- Merge JSON files
- Validate relationships
- Deduplicate (same cause → effect)
- Build knowledge graph

## Troubleshooting

### Problem: Output không đúng format JSON

**Solution**:
- Thêm explicit instruction: "Output MUST be valid JSON"
- Thêm example JSON trong prompt
- Check Manus settings (output format)

### Problem: Extract quá ít relationships

**Solution**:
- Thêm more examples vào prompt
- Làm rõ "extract ALL causal relationships"
- Chia document thành sections nhỏ hơn

### Problem: Extract quá nhiều (bao gồm correlations)

**Solution**:
- Nhấn mạnh "CHỈ extract causal relationships"
- Thêm examples về correlation vs causation
- Review và filter output manually

### Problem: Mechanism không rõ ràng

**Solution**:
- Thêm requirement: "Mechanism phải giải thích TẠI SAO và NHƯ THẾ NÀO"
- Thêm examples với good mechanisms
- Refine prompt với more specific instructions

## Checklist trước khi Extract

- [ ] Đã chọn đúng prompt phù hợp với document?
- [ ] Đã copy đầy đủ prompt content?
- [ ] Đã format input đúng template?
- [ ] Đã có examples trong prompt?
- [ ] Document text đã được clean (không có formatting issues)?
- [ ] Đã set output format là JSON trong Manus?

## Checklist sau khi Extract

- [ ] Output là valid JSON?
- [ ] Có đủ relationships không?
- [ ] Mechanism có rõ ràng không?
- [ ] Conditions có đầy đủ không?
- [ ] Confidence có phù hợp không?
- [ ] Nodes có standardized không? (snake_case, tiếng Anh)

## Next Steps

Sau khi extract từ Manus:

1. **Validate JSON**: Check format, required fields
2. **Review Relationships**: Check quality, mechanism clarity
3. **Deduplicate**: Remove duplicate relationships
4. **Merge**: Combine với các extractions khác
5. **Build Graph**: Import vào knowledge graph (Neo4j, NetworkX)
6. **Validate Graph**: Check for cycles, inconsistencies

## Resources

- Master Template: `prompt_00_master_template.md`
- All Prompts: `prompt_01_*.md` đến `prompt_07_*.md`
- Variables Checklist: `VARIABLES_CHECKLIST.md`
- README: `README.md`
