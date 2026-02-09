# Reasoning Guide: Retrieval + “Chain-of-Thought” cho diễn giải cơ chế

## 1) Mục tiêu
- Trả lời dạng **giải thích cơ chế** cho câu hỏi “Tại sao/How” về PM2.5.
- **Grounded**: mọi lập luận phải bám vào `data/merged_knowledge_graph.json` (edge + evidence).
- Trình bày rõ theo bước, nhưng **không lộ chain-of-thought thô**; chỉ xuất “explanation steps” ngắn gọn, có trích dẫn.

## 2) Khái niệm dữ liệu đầu vào/đầu ra

### 2.1. Input tối thiểu
- `question`: câu hỏi người dùng (VI/EN)
- `entities`: danh sách entities (node) rút ra từ câu hỏi (ví dụ `pm25`, `relative_humidity`, `cold_surge`)
- `location` (tuỳ chọn): phường/quận
- `time_context` (tuỳ chọn): “mùa đông/đêm/hôm nay”

### 2.2. Output chuẩn cho phần suy luận
Một cấu trúc có thể đưa thẳng cho LLM để viết câu trả lời:
- `selected_chains`: 1–3 causal chains (2–4 bước), mỗi bước là một relationship + evidence
- `supporting_factors`: 0–3 yếu tố bổ trợ (không bắt buộc theo chain)
- `uncertainties`: các điểm thiếu dữ liệu/điều kiện chưa kiểm tra được

## 3) Retrieval Strategy (không cần Neo4j ở giai đoạn 1)

### 3.1. Entity extraction
Ưu tiên rule-based (để tránh hallucination) + fallback LLM:
- Từ điển synonyms (đã áp dụng ở merge): `pm2.5→pm25`, `RH→relative_humidity`, …
- Nếu câu hỏi không nêu biến khí tượng cụ thể: mặc định lấy “core meteorology set”: `temperature`, `relative_humidity`, `wind_speed`, `pblh`, `precipitation` + `seasonal_patterns`

### 3.2. Candidate subgraph
Lấy subgraph nhỏ quanh `pm25`:
- `k-hop` quanh `pm25` (k=2..3) **và** quanh entity chính (nếu có)
- Lọc theo:
  - `confidence` ưu tiên `HIGH`, sau đó `MEDIUM`
  - `tier` (nếu có trong bibliography) ưu tiên tier_1/tier_2
  - `category` tuỳ câu hỏi: meteorological/seasonal/chemical/transport…

### 3.3. Candidate chains
Tạo chain ứng viên:
- Độ dài mục tiêu: 2–4 edges
- Kết thúc tại `pm25`
- Ưu tiên chain có **mechanism rõ** và **conditions cụ thể**

## 4) Ranking Strategy

### 4.1. Điểm chain (gợi ý)
Chấm theo:
- `confidence`: HIGH=2, MEDIUM=1, LOW=0
- `strength`: STRONG=2, MODERATE=1, WEAK=0
- Bonus nếu:
  - có `temporal_lag` cụ thể
  - conditions có threshold (ví dụ `RH > 75%`)
  - evidence quote rõ, không mơ hồ

### 4.2. Giới hạn để đảm bảo chất lượng
- Output tối đa **3 chains**; mỗi chain tối đa **4 bước**
- Mỗi bước phải có `source_url/source_doi` và `source_quote`

## 5) Condition-checking (giai đoạn chưa có pipeline theo giờ)

Chia điều kiện thành 2 loại:
- **Kiểm tra được ngay** (nếu có dữ liệu tối thiểu theo ngày): mùa (winter/summer), mưa/không mưa, gió mạnh/yếu (proxy), RH cao/thấp (proxy)
- **Chưa kiểm tra được**: inversion thực đo, pH aerosol, ALW định lượng… → phải đưa vào `uncertainties`

Nguyên tắc:
- Nếu không kiểm tra được điều kiện, **không loại bỏ relationship** ngay, nhưng hạ “độ chắc” khi trình bày: “cơ chế này thường mạnh khi …”

## 6) Prompt template cho LLM (grounded explanation)

### 6.1. Input format (đưa vào LLM)
Gồm 3 khối:
1) Câu hỏi người dùng\n
2) `selected_chains` (liệt kê theo bước; mỗi bước kèm evidence)\n
3) `uncertainties` (nếu có)\n

### 6.2. Output format yêu cầu
- Trả lời tiếng Việt, dễ hiểu
- Có cấu trúc:
  - “Nguyên nhân chính”
  - “Yếu tố bổ trợ”
  - “Điều kiện/ngoại lệ”
  - “Nguồn trích dẫn” (liệt kê ngắn 2–5 nguồn)
- **Không bịa**: chỉ dùng nội dung trong chains/evidence

## 7) Anti-hallucination rules (bắt buộc)
- Không được thêm “nguyên nhân mới” nếu không có trong graph.
- Không được suy diễn định lượng nếu nguồn không nói.
- Nếu thiếu dữ liệu điều kiện, phải nói rõ: “hiện chưa có dữ liệu theo giờ để kiểm tra …”

