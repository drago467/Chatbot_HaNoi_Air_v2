## PROMPT 07: EDGE CASES AND EXCEPTIONS
# Focused Task: Extract causal edge cases/exceptions để tránh trả lời sai/hallucination
# Version: 2.0 - For Manus Auto-Discovery
# Category: edge_cases

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm sources khoa học và extract các **trường hợp ngoại lệ** (exceptions), quan hệ **phi tuyến** (threshold/reversal), và **measurement artifacts** trong PM2.5 để chatbot không áp dụng sai “rule” phổ biến.

## CATEGORY DEFINITION
**Category**: `edge_cases`

**Focus**: Những tình huống mà quan hệ thường gặp bị đảo ngược / không còn đúng, và điều kiện chính xác để kích hoạt ngoại lệ.

## IN-SCOPE (Allowed Edge Cases)

### Humidity-related exceptions
1. **humidity very high + fog → hygroscopic_growth → pm25_measured increases** (measurement artifact)
2. **humidity moderate/high → promotes aqueous chemistry → pm25 increases** (phi tuyến, cần điều kiện cụ thể)
3. **humidity high + precipitation → wet_deposition dominates → pm25 decreases** (reversal vs chemistry)

### Wind-related exceptions
4. **wind_speed high + wind_direction from polluted source region → transport dominates → pm25 not decrease / increase**
5. **wind_speed low + local emissions high → stagnation → pm25 spikes** (nếu là edge case ngưỡng)

### Precipitation-related exceptions
6. **light precipitation/drizzle → insufficient scavenging → humidity up → pm25 not decrease**
7. **post-rain resuspension / activity rebound → pm25 increases** (nếu nguồn có nói)

### Temperature-related exceptions
8. **high temperature + strong photochemistry → secondary formation → pm25 increases** (khi có VOCs/NOx)
9. **low temperature → NH4NO3 stability → pm25 increases** (nhưng chemistry detail handoff)

### Cold surge / synoptic pattern exceptions
10. **cold_surge → initial pm25 decrease then delayed increase** (reversal/delay)

### Confounding / Interaction
11. Multi-factor interactions where direction changes depending on third variable:
   - humidity effect depends on precipitation and precursors
   - wind effect depends on direction/source regions

### Allowed Intermediate Nodes
- `hygroscopic_growth`, `pm25_measured`, `measurement_artifact`
- `threshold_effect`, `reversal_effect`, `interaction_effect`

## OUT-OF-SCOPE (Handoff)
- Detailed chemical pathways (→ prompt_02)
- Standard meteorology pathways without being an exception (→ prompt_01)
- Standard emissions without being an exception (→ prompt_04)

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "hygroscopic growth humidity PM2.5 measurement artifact"
2. "U-shaped relationship humidity PM2.5 aerosol liquid water"
3. "light rain drizzle PM2.5 not decrease scavenging"
4. "strong wind transport pollution increase PM2.5 receptor"
5. "cold surge delayed PM2.5 increase mechanism"
6. "high temperature photochemistry secondary aerosol PM2.5 increase"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Accept Tier-2 for measurement/instrumentation docs (authoritative)

## EXTRACTION PHASE

### Extraction Rules
1. Mỗi edge case phải có:
   - điều kiện kích hoạt (thresholds + context)
   - “what rule it breaks” trong notes
   - quote/URL/locator bắt buộc
2. Phải ghi rõ loại edge case:
   - `measurement_artifact` vs `real_physical_exception`
3. Nếu chỉ suy diễn mà không có evidence → đưa vào missing_info, không tạo edge.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "edge_cases"`.

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for scientific sources on PM2.5 exceptions, non-linearities, and measurement artifacts.

## KEY MECHANISMS TO LOOK FOR

### Threshold Effects:
- **Critical thresholds**: Khi vượt qua ngưỡng, effect đảo ngược
- **Optimal ranges**: Effect chỉ đúng trong một khoảng nhất định

### Reversal Effects:
- **Initial vs delayed**: Effect ban đầu khác với effect sau
- **Conditional reversal**: Effect đảo ngược khi có điều kiện khác

### Measurement Artifacts:
- **Hygroscopic growth**: Hạt bụi hút ẩm → Tăng kích thước → Measurement tăng (nhưng không phải tăng thực sự)
- **Instrument limitations**: Giới hạn của thiết bị đo

### Confounding Factors:
- **Multiple mechanisms**: Nhiều cơ chế cùng hoạt động, có thể đối nghịch
- **Interaction effects**: Tương tác giữa các yếu tố

## EXAMPLES OF GOOD EXTRACTIONS

### Example 1: Humidity → PM2.5 (Non-linear, U-shaped)
```json
{
  "id": "humidity_pm25_nonlinear_001",
  "cause_node": "humidity",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Độ ẩm rất cao (>90%) + Sương mù → Hạt bụi hút ẩm (hygroscopic growth) → Tăng kích thước và khối lượng → PM2.5 đo được tăng (nhưng thực chất là do hút ẩm, không phải tăng thực sự). Ngược lại, độ ẩm trung bình (45-75%) → Thúc đẩy chemical reactions → PM2.5 tăng thực sự",
  "conditions": [
    "RH > 90%",
    "Sương mù",
    "Không có precipitation",
    "Có PM2.5 particles"
  ],
  "temporal_lag": "2-4h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Very high humidity with fog causes hygroscopic growth, increasing measured PM2.5 but not actual mass",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "EDGE CASE: This is a measurement artifact, not a real increase. Non-linear relationship: U-shaped curve. Low RH (<45%): low effect. Medium RH (45-75%): chemical reactions increase PM2.5. High RH (>90%): measurement artifact increases readings"
}
```

### Example 2: Wind Speed → PM2.5 (Exception: Transport from Sources)
```json
{
  "id": "wind_speed_pm25_exception_001",
  "cause_node": "wind_speed",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Gió mạnh (>5 m/s) từ hướng có nguồn phát thải lớn → Vận chuyển ô nhiễm vào → PM2.5 có thể không giảm hoặc tăng (thay vì giảm như thông thường)",
  "conditions": [
    "Wind speed > 5 m/s",
    "Wind từ hướng có strong emission sources",
    "Regional transport",
    "Không có precipitation"
  ],
  "temporal_lag": "6-24h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Strong winds from emission source directions can transport pollutants, preventing PM2.5 decrease",
  "seasonal_variation": "all_season",
  "spatial_scope": "regional",
  "notes": "EDGE CASE: Exception to general rule that strong winds decrease PM2.5. Effect depends on source location relative to wind direction"
}
```

### Example 3: Precipitation → PM2.5 (Exception: Light Rain)
```json
{
  "id": "precipitation_pm25_exception_001",
  "cause_node": "precipitation",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Mưa nhẹ (< 1mm/h) → Không đủ để rửa trôi hiệu quả → Có thể làm tăng độ ẩm → Thúc đẩy chemical reactions → PM2.5 có thể không giảm hoặc tăng nhẹ. Chỉ mưa đáng kể (> 2mm/h) mới làm PM2.5 giảm rõ rệt",
  "conditions": [
    "Light rain (< 1mm/h)",
    "Không có gió mạnh",
    "Có precursors (SO2, NO2)"
  ],
  "temporal_lag": "2-6h",
  "strength": "WEAK",
  "confidence": "LOW",
  "evidence_text": "Light rain may not effectively remove PM2.5 and could promote chemical reactions",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "EDGE CASE: Exception to general rule that precipitation decreases PM2.5. Only significant precipitation (>2mm/h) effectively removes PM2.5"
}
```

### Example 4: Temperature → PM2.5 (Exception: High Temp + High Emissions)
```json
{
  "id": "temperature_pm25_exception_001",
  "cause_node": "temperature",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Nhiệt độ cao (>30°C) + Phát thải cao + Gió yếu → Mặc dù PBLH cao nhưng phát thải quá lớn → PM2.5 vẫn có thể cao. Đồng thời, nhiệt độ cao → Thúc đẩy photochemistry → O3 tăng → Secondary aerosols → PM2.5 tăng",
  "conditions": [
    "Temperature > 30°C",
    "High emission sources",
    "Wind speed < 2 m/s",
    "High solar radiation",
    "Có precursors (VOCs, NOx)"
  ],
  "temporal_lag": "4-8h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "High temperature with high emissions and low wind can still lead to high PM2.5 despite high PBLH",
  "seasonal_variation": "summer",
  "spatial_scope": "local",
  "notes": "EDGE CASE: Exception to general rule that high temperature decreases PM2.5. Multiple mechanisms: high emissions + photochemistry can overcome PBLH effect"
}
```

### Example 5: Cold Surge → PM2.5 (Non-linear, Delayed Effect)
```json
{
  "id": "cold_surge_pm25_nonlinear_001",
  "cause_node": "cold_surge",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Đợt không khí lạnh tràn về → Giai đoạn 1 (0-2 ngày): Gió mạnh, xáo trộn → PM2.5 GIẢM. Giai đoạn 2 (2-4 ngày): Khối khí ổn định → Áp cao, gió lặng → Nghịch nhiệt → PBLH thấp → PM2.5 TĂNG VỌT",
  "conditions": [
    "Mùa đông",
    "Gió mùa Đông Bắc",
    "Sau khi cold surge ổn định (2-4 ngày)"
  ],
  "temporal_lag": "2-4 days (delayed effect)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Cold surges show non-linear effect: initial decrease followed by significant increase after stabilization",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "EDGE CASE: Non-linear relationship with delayed effect. Initial decrease (0-2 days) then increase (2-4 days). This is a reversal effect"
}
```

### Example 6: Wind Direction → PM2.5 (Exception: Clean Air from Sea)
```json
{
  "id": "wind_direction_pm25_exception_001",
  "cause_node": "wind_direction",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Gió từ biển (Đông, Đông Nam) → Mang không khí sạch → PM2.5 GIẢM (thay vì tăng như khi gió từ industrial areas). Tuy nhiên, nếu có industrial sources ở hướng biển → Vẫn có thể tăng",
  "conditions": [
    "Wind từ biển (Đông, Đông Nam)",
    "Không có industrial sources ở hướng biển",
    "Wind speed > 2 m/s"
  ],
  "temporal_lag": "6-12h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Winds from the sea typically bring cleaner air, reducing PM2.5",
  "seasonal_variation": "all_season",
  "spatial_scope": "regional",
  "notes": "EDGE CASE: Exception to general rule that wind direction from sources increases PM2.5. Sea winds bring clean air"
}
```

### Example 7: Multiple Factors Interaction (Confounding)
```json
{
  "id": "multiple_factors_confounding_001",
  "cause_node": "humidity",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Độ ẩm cao (>75%) + Có precursors (SO2, NO2) + Nhiệt độ thấp + Gió yếu → Chemical reactions tăng → PM2.5 tăng. NHƯNG nếu có mưa → Wet deposition → PM2.5 giảm. Effect phụ thuộc vào sự tương tác của nhiều yếu tố",
  "conditions": [
    "RH > 75%",
    "Có SO2 và NO2",
    "Temperature < 15°C",
    "Wind speed < 2 m/s",
    "KHÔNG có precipitation"
  ],
  "temporal_lag": "4-12h",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "High humidity promotes chemical reactions, but effect depends on other factors (precursors, temperature, wind, precipitation)",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "EDGE CASE: Confounding factors. High humidity can increase PM2.5 (chemical reactions) OR decrease PM2.5 (wet deposition), depending on other conditions"
}
```

## COMMON PITFALLS TO AVOID

1. **PHẢI ghi rõ đây là exception/edge case** trong notes field:
   - "EDGE CASE: Exception to general rule..."
   - "EDGE CASE: Non-linear relationship..."
   - "EDGE CASE: Measurement artifact..."

2. **PHẢI giải thích tại sao đây là exception**:
   - Điều kiện nào làm effect đảo ngược?
   - Mechanism nào khác với quy luật thông thường?

3. **PHẢI ghi rõ conditions cụ thể**:
   - Edge cases thường chỉ đúng trong điều kiện đặc biệt
   - Phải ghi rõ thresholds và conditions

4. **PHẢI phân biệt measurement artifact vs real effect**:
   - Measurement artifact: Không phải tăng thực sự
   - Real effect: Tăng thực sự do mechanism khác

5. **PHẢI ghi rõ non-linear relationships**:
   - Threshold effects
   - Reversal effects
   - U-shaped curves

## SPECIFIC VARIABLES TO EXTRACT

Đảm bảo extract edge cases cho:

### Non-linear Relationships:
- `humidity` → `pm25` (U-shaped, measurement artifact)
- `wind_speed` → `pm25` (exception: transport from sources)
- `precipitation` → `pm25` (exception: light rain)
- `temperature` → `pm25` (exception: high temp + high emissions)
- `cold_surge` → `pm25` (non-linear, delayed effect)
- `wind_direction` → `pm25` (exception: clean air from sea)

### Measurement Artifacts:
- `humidity` → `hygroscopic_growth` → `pm25` (measurement artifact)
- `fog` → `pm25` (measurement artifact)

### Confounding Factors:
- Multiple factors interaction
- Conditional reversals

## VALIDATION CHECKLIST

Trước khi output, kiểm tra:
- [ ] Notes có ghi rõ đây là EDGE CASE không?
- [ ] Mechanism có giải thích tại sao đây là exception không?
- [ ] Conditions có đầy đủ không? (edge cases cần conditions cụ thể)
- [ ] Có phân biệt được measurement artifact vs real effect không?
- [ ] Non-linear relationships có được ghi rõ không?
