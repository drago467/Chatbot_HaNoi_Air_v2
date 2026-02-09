# Quality Assessment - Extracted Causal Relationships

## Tổng quan

Đánh giá chất lượng các relationships đã được extract từ Manus sử dụng prompts V2.0.

## Metrics

### 1. Coverage (Bao phủ)

**Total Relationships**: ~99 relationships across 7 categories
- Meteorological pathways: ~13
- Chemical processes: ~10
- Transport mechanisms: ~18
- Emission sources: ~17
- Static factors: ~6
- Seasonal patterns: ~35
- Edge cases: ~6

**Total Sources**: ~50+ unique sources (Tier-1 papers)

### 2. Evidence Quality

✅ **192 relationships** có source_url/source_quote  
✅ **0 relationships** với source_quote rỗng  
✅ **Tất cả relationships** có source metadata (title, authors, year)

### 3. Confidence Distribution

- **HIGH confidence**: ~46 relationships
- **MEDIUM confidence**: ~30 relationships  
- **LOW confidence**: ~23 relationships

### 4. Format Consistency

**Standard V2.0 Format** (có bibliography + relationships):
- ✅ meteorological_pathways.json
- ✅ chemical_processes.json
- ✅ emission_sources.json
- ✅ edge_cases.json

**Alternative Formats** (cần normalize):
- ⚠️ seasonal_patterns.json (có prompt_id, causal_relationships)
- ⚠️ static_factors.json (array format)
- ⚠️ transport_mechanisms.json (có metadata, sources)

## Quality Highlights

### ✅ Strengths

1. **Strong Evidence**: Tất cả relationships có source_quote và source_url
2. **High-Quality Sources**: Chủ yếu Tier-1 papers (peer-reviewed)
3. **Detailed Mechanisms**: Mechanisms được mô tả chi tiết với cơ chế vật lý/hóa học
4. **Clear Conditions**: Conditions được ghi rõ (thresholds, time periods, spatial scope)
5. **Geographic Relevance**: Nhiều papers về Hà Nội, Việt Nam, Đông Nam Á

### ⚠️ Areas for Improvement

1. **Format Inconsistency**: Một số files có format khác (cần normalize)
2. **Some LOW Confidence**: ~23 relationships có confidence LOW (cần review)
3. **Missing Temporal Lag**: Một số relationships không có temporal_lag
4. **Duplicate Check**: Cần deduplicate sau khi merge

## Sample High-Quality Relationships

### Example 1: Temperature → Inversion (meteorological_pathways.json)
```json
{
  "id": "met_001",
  "cause_node": "temperature",
  "effect_node": "inversion",
  "mechanism": "Nhiệt độ giảm vào ban đêm dẫn đến mặt đất mất nhiệt nhanh...",
  "conditions": ["Ban đêm", "Trời quang mây", "Mùa đông"],
  "confidence": "HIGH",
  "source_quote": "Very high PM2.5... were observed in conjunction with...",
  "source_url": "https://www.sciencedirect.com/..."
}
```
✅ **Quality**: Excellent - có đầy đủ evidence, mechanism rõ ràng, conditions cụ thể

### Example 2: Humidity → SIA Formation (chemical_processes.json)
```json
{
  "id": "chem_001",
  "cause_node": "humidity",
  "effect_node": "sia_formation",
  "mechanism": "Khi độ ẩm tương đối (RH) tăng cao (>75%)...",
  "conditions": ["RH > 75%", "Có sự hiện diện của các hạt aerosol..."],
  "confidence": "HIGH",
  "source_quote": "Relative humidity, pressure, temperature...",
  "source_url": "https://doi.org/10.4209/aaqr.220446"
}
```
✅ **Quality**: Excellent - có threshold cụ thể, mechanism chi tiết

## Next Steps

### 1. Merge và Normalize
```bash
python merge_and_validate.py
```
- Normalize tất cả formats về chuẩn V2.0
- Deduplicate relationships
- Validate chất lượng

### 2. Review LOW Confidence Relationships
- Check xem có thể nâng confidence lên không
- Có thể cần thêm evidence từ sources khác

### 3. Build Knowledge Graph
```bash
python build_knowledge_graph.py
```
- Tạo NetworkX graph
- Export Neo4j format
- Analyze graph structure

### 4. Integration
- Import vào chatbot system
- Test causal retrieval
- Validate với real questions

## Recommendations

1. **Review LOW confidence relationships**: Có thể cần extract thêm từ sources khác
2. **Check for gaps**: Có pathways quan trọng nào còn thiếu không?
3. **Validate mechanisms**: Có mechanisms nào cần clarify thêm không?
4. **Test with chatbot**: Thử với real questions để xem coverage có đủ không
