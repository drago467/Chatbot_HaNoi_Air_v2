# Hướng dẫn gửi Manus cho Phase 2 - Node Normalization & Enrichment

## Files cần gửi cho Manus

### 1. Prompts (theo thứ tự)
1. **`prompt_00_master_template.md`** (bắt buộc)
   - Chứa guardrails, quy tắc naming nodes, anti-hallucination policies.
   - Manus cần đọc để hiểu quy tắc naming (snake_case, tiếng Anh) và quality standards.

2. **`prompt_21_node_normalization_and_enrichment.md`** (bắt buộc)
   - Prompt chính cho Phase 2.
   - Chứa toàn bộ tasks: fix issues, node mapping, descriptions, retrieval structure.

3. **`VARIABLES_CHECKLIST.md`** (khuyến khích, optional)
   - Reference cho canonical taxonomy.
   - Giúp Manus hiểu các biến đã được cover và naming conventions.

### 2. Data files
1. **`merged_knowledge_graph_v2.json`** (bắt buộc)
   - File đã được merge từ Phase 1.
   - Chứa toàn bộ relationships với conditions đã normalize.

2. **`node_inventory.json`** (optional, nếu đã có)
   - Nếu bạn đã chạy script `build_node_inventory.py` và có file này, gửi kèm để Manus không phải tự inventory.

---

## Message template cho Manus

### Cách 1: Ngắn gọn (khuyến nghị)

```
Bạn hãy đọc 3 prompts dưới đây (theo thứ tự: prompt_00, prompt_21, VARIABLES_CHECKLIST) và file JSON `merged_knowledge_graph_v2.json`.

Nhiệm vụ của bạn:
1. Sửa 7 issues `checkable_empty_field` (tìm các condition có `checkable = true` nhưng `field = ""`).
2. Xây taxonomy canonical nodes và mapping `original_node → canonical_node`.
3. Áp dụng mapping vào tất cả relationships (thêm `canonical_*_node`, giữ `original_*_node`).
4. Sinh descriptions cho canonical nodes.
5. (Optional) Thêm `embedding_context` metadata.

Output: File `merged_knowledge_graph_v2.json` đã được cập nhật, hoặc tách thành các file riêng (`node_mapping.json`, `node_metadata.json`) nếu bạn muốn.

Lưu ý quan trọng:
- KHÔNG được sửa `conditions` (field/operator/value/range) đã được normalize ở Phase 1, trừ các cases `checkable_empty_field`.
- Phải giữ nguyên `original_*_node`, chỉ thêm `canonical_*_node`.
- Mọi canonical node phải có description.
```

### Cách 2: Chi tiết hơn (nếu muốn rõ ràng hơn)

```
Chào bạn,

Tôi đang làm Phase 2 cho Causal Knowledge Graph (CKG) về ô nhiễm không khí ở Hà Nội. Bạn đã giúp tôi ở Phase 1 (normalize conditions từ 18 file `_clean`), giờ tôi cần bạn hỗ trợ Phase 2: chuẩn hoá nodes và enrich metadata.

Files tôi gửi kèm:
1. `prompt_00_master_template.md` - Guardrails và quy tắc naming
2. `prompt_21_node_normalization_and_enrichment.md` - Prompt chính cho Phase 2
3. `VARIABLES_CHECKLIST.md` - Reference cho canonical taxonomy
4. `merged_knowledge_graph_v2.json` - File đã merge từ Phase 1

Nhiệm vụ cụ thể:
1. Fix 7 issues `checkable_empty_field`: tìm các condition có `checkable = true` nhưng `field = ""`, map sang field hợp lệ hoặc set `checkable = false`.
2. Inventory tất cả nodes (cause/effect/intermediate) từ merged_v2.
3. Xây taxonomy canonical nodes dựa trên VARIABLES_CHECKLIST và prompt_00.
4. Tạo mapping `original_node → canonical_node` (ví dụ: "humidity" → "relative_humidity").
5. Áp dụng mapping vào relationships: thêm `canonical_cause_node`, `canonical_effect_node`, nhưng GIỮ NGUYÊN `cause_node`, `effect_node`.
6. Sinh descriptions (1-2 câu) cho mỗi canonical node.
7. (Optional) Thêm `embedding_context` metadata cho mỗi relationship để hỗ trợ retrieval.

Output mong muốn:
- File `merged_knowledge_graph_v2.json` đã được cập nhật với:
  - `canonical_*_node` trong mỗi relationship
  - Issues `checkable_empty_field` đã được sửa
  - Section `nodes` ở top-level (hoặc tách riêng thành `node_metadata.json`)

Ràng buộc quan trọng:
- KHÔNG được sửa `conditions` (field/operator/value/range/checkable) đã được normalize ở Phase 1, TRỪ các cases `checkable_empty_field`.
- Phải giữ traceability: giữ `original_*_node`, chỉ thêm `canonical_*_node`.
- Mọi canonical node phải có description.

Cảm ơn bạn!
```

---

## Checklist trước khi gửi

- [ ] Đã có `prompt_00_master_template.md`
- [ ] Đã có `prompt_21_node_normalization_and_enrichment.md`
- [ ] Đã có `VARIABLES_CHECKLIST.md` (optional nhưng khuyến khích)
- [ ] Đã có `merged_knowledge_graph_v2.json` (đã được tạo từ Phase 1)
- [ ] (Optional) Đã có `node_inventory.json` nếu đã chạy script

---

## Lưu ý khi nhận kết quả từ Manus

Sau khi Manus trả về file(s), bạn nên:

1. **Chạy lại QA script**:
   ```bash
   python causal/causal_knowledge/scripts/validate_merged_knowledge_graph_v2.py
   ```
   - Kiểm tra xem còn issues `checkable_empty_field` không.
   - Kiểm tra các rule QA khác.

2. **Spot-check một vài relationships**:
   - So sánh `conditions` giữa bản Phase 1 và Phase 2 (phải giống hệt, trừ các cases đã sửa `checkable_empty_field`).
   - Kiểm tra `canonical_*_node` có hợp lý không.
   - Kiểm tra descriptions có đầy đủ và rõ ràng không.

3. **Kiểm tra node mapping consistency**:
   - Mọi `canonical_*_node` đều tồn tại trong taxonomy `nodes`.
   - Không có node nào bị mất (mọi `original_*_node` vẫn còn).
