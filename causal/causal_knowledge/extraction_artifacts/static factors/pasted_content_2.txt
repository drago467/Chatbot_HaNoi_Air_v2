## PROMPT 05: STATIC FACTORS
# Focused Task: Extract causal relationships về yếu tố tĩnh (GEE/DEM/LULC/dân cư) ảnh hưởng PM2.5
# Version: 2.0 - For Manus Auto-Discovery
# Category: static_factors

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm sources khoa học và extract causal relationships về các yếu tố tĩnh: **dân cư, sử dụng đất (LULC), mạng lưới đường, khu công nghiệp, địa hình từ DEM (valley/basin, TWI, slope, elevation)** và cách chúng làm thay đổi nền/khả năng tích tụ/khả năng phát thải tại chỗ liên quan PM2.5.

## CATEGORY DEFINITION
**Category**: `static_factors`

**Focus**: Static context nodes/edges dùng cho offline processing (GEE + DEM) và giải thích khác biệt không gian giữa phường/xã.

## IN-SCOPE (Allowed Relationships)

### Population / Urban Form
1. **population_density → emission_intensity → pm25** (INDIRECT_CAUSE; cần cơ chế cụ thể)
2. **urban_land_use → local_emission_sources → pm25**
3. **urban_density → traffic_activity_potential → pm25** (nếu paper nói theo cơ chế)

### Road Network Proximity
4. **distance_to_roads → traffic_exposure → pm25**
5. **road_density → traffic_exposure → pm25**

### Industrial/Construction Spatial Context
6. **industrial_zones → local_emissions → pm25**
7. **distance_to_industrial_zones → exposure → pm25**

### Vegetation / Green Space
8. **vegetation → dry_deposition → pm25** (thường weak; cần evidence rõ)
9. **vegetation → barrier_effect → pm25** (nếu được nguồn support)

### DEM/Topography Derived
10. **topography (basin/valley_bottom) → air_trapping → pm25**
11. **elevation/slope → air_flow_modulation → pm25** (nếu có)
12. **topographic_wetness_index → air_trapping → pm25** (TWI như proxy lòng chảo)

### Allowed Intermediate Nodes
- `emission_intensity`, `local_emission_sources`, `traffic_exposure`, `local_emissions`, `exposure`
- `air_trapping`, `air_flow_modulation`, `dry_deposition`, `barrier_effect`

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Time-varying emissions (→ prompt_04)
- ❌ traffic rush hour, day-to-day emission variation
- Action: handoff_to_other_prompts ["emission_sources"]

### Meteorology/chemistry (→ prompt_01/prompt_02)
- ❌ inversion/pblh/wind/humidity chemistry details
- Action: handoff accordingly

### Seasonal/diurnal patterns (→ prompt_06)
- ❌ season/time_of_day explanations
- Action: handoff_to_other_prompts ["seasonal_patterns"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "urban form population density PM2.5 exposure causal mechanisms"
2. "land use land cover LULC PM2.5 urban Vietnam"
3. "distance to roads traffic-related air pollution PM2.5"
4. "topography basin valley air pollution trapping PM2.5"
5. "DEM derived indices TWI air pollution accumulation"
6. "vegetation dry deposition PM2.5 urban green space"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Tier-2 allowed: authoritative GIS/health/environment reports

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract edges IN-SCOPE.
2. Mỗi edge bắt buộc có quote/URL/locator.
3. Phải ghi rõ đây là **static factor**:
   - temporal_lag: "N/A (static factor)"
   - notes: \"Static factor; effect manifests under certain meteorological conditions\"
4. Nếu paper chỉ nói “associated with” mà không có cơ chế → reject hoặc set LOW + đưa vào missing_info.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "static_factors"`.

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for scientific sources on static factors (population/LULC/DEM) shaping PM2.5 spatial patterns relevant to Hanoi/Vietnam.

## KEY MECHANISMS TO LOOK FOR

### Urban Heat Island:
- **Urban vs Rural**: Đô thị nóng hơn → Ảnh hưởng đến PBLH và dispersion
- **Surface materials**: Vật liệu đô thị hấp thụ nhiệt → Tăng nhiệt độ

### Topographic Trapping:
- **Valley/Basin**: Không khí lạnh và ô nhiễm dễ bị đọng lại
- **Mountain blocking**: Chặn gió → Giảm dispersion
- **Channeling**: Định hướng gió theo địa hình

### Land Use Effects:
- **Urban areas**: Nhiều nguồn phát thải (traffic, industry)
- **Vegetation**: Lắng đọng bụi, hấp thụ pollutants
- **Industrial zones**: Nguồn phát thải tập trung

### Source Proximity:
- **Distance to roads**: Gần đường giao thông → Nhiều exposure
- **Distance to industry**: Gần khu công nghiệp → Nhiều exposure

## EXAMPLES OF GOOD EXTRACTIONS

### Example 1: Urban Density → Emission Sources → PM2.5
```json
{
  "id": "urban_density_emissions_pm25_001",
  "cause_node": "urban_density",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Mật độ đô thị cao → Nhiều nguồn phát thải tập trung (giao thông, công nghiệp, xây dựng) → Tổng lượng phát thải cao → PM2.5 cao hơn",
  "conditions": [
    "Urban areas",
    "High population density",
    "Nhiều hoạt động đô thị"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Urban areas with high population density have more emission sources, leading to higher PM2.5 concentrations",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Static factor: affects all time periods. Effect is indirect through increased emission sources"
}
```

### Example 2: Valley/Basin Topography → Air Trapping → PM2.5
```json
{
  "id": "valley_topography_pm25_001",
  "cause_node": "valley_bottom",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Địa hình lòng chảo/thung lũng → Không khí lạnh và ô nhiễm dễ bị đọng lại (cold air pooling) → Ít khuếch tán → PM2.5 tích tụ. Đồng thời, địa hình này làm chậm tốc độ gió bề mặt",
  "conditions": [
    "Valley/basin topography",
    "Stable atmospheric conditions",
    "Gió yếu",
    "Mùa đông (nhiệt độ thấp)"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Basin-like topography of Hanoi facilitates pollutant accumulation during stable conditions",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "Static factor: affects all time periods when conditions are met. Hanoi's basin topography is a key factor in winter pollution episodes"
}
```

### Example 3: Distance to Roads → Traffic Exposure → PM2.5
```json
{
  "id": "distance_roads_traffic_pm25_001",
  "cause_node": "distance_to_roads",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Gần đường giao thông → Nhiều exposure trực tiếp với emissions từ traffic (NOx, PM2.5 primary) → PM2.5 cao hơn. Khoảng cách càng xa → Nồng độ giảm do dispersion",
  "conditions": [
    "Urban areas",
    "Major roads with high traffic volume",
    "Không có rào chắn (vegetation, buildings)"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Proximity to major roads increases exposure to traffic emissions",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Static factor: distance is fixed, but effect varies with traffic volume (which is temporal)"
}
```

### Example 4: Vegetation → Deposition → PM2.5
```json
{
  "id": "vegetation_deposition_pm25_001",
  "cause_node": "vegetation",
  "effect_node": "pm25",
  "relationship_type": "DIRECT_CAUSE",
  "mechanism": "Thực vật → Lắng đọng khô (dry deposition) trên lá cây → Hấp thụ một phần PM2.5 → PM2.5 giảm. Đồng thời, cây xanh có thể tạo rào chắn vật lý cho bụi",
  "conditions": [
    "High vegetation cover",
    "Dense tree canopy",
    "Không có gió mạnh"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "WEAK",
  "confidence": "LOW",
  "evidence_text": "Vegetation can remove some PM2.5 through dry deposition, but effect is limited",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Static factor: effect is relatively weak compared to emission sources. More significant for larger green spaces"
}
```

### Example 5: Industrial Zones → Emissions → PM2.5
```json
{
  "id": "industrial_zones_emissions_pm25_001",
  "cause_node": "industrial_zones",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Khu công nghiệp → Nhiều nguồn phát thải tập trung (SO2, NOx, PM2.5 primary) → Tổng lượng phát thải cao → PM2.5 cao hơn. Có thể vận chuyển đến khu vực xung quanh",
  "conditions": [
    "Proximity to industrial zones",
    "Active industrial activities",
    "Wind từ hướng industrial zones"
  ],
  "temporal_lag": "N/A (static factor for location, but emissions are temporal)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Industrial zones are major sources of SO2, NOx, and PM2.5",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Static factor: location is fixed, but emissions vary temporally. Can affect nearby areas through transport"
}
```

### Example 6: TWI (Topographic Wetness Index) → Air Flow → PM2.5
```json
{
  "id": "twi_airflow_pm25_001",
  "cause_node": "topographic_wetness_index",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "TWI cao → Khu vực có xu hướng tích tụ độ ẩm → Có thể ảnh hưởng đến air flow patterns → Không khí dễ bị đọng lại → PM2.5 tích tụ. TWI là chỉ số địa hình xác định các khu vực 'lòng chảo'",
  "conditions": [
    "High TWI values",
    "Stable atmospheric conditions",
    "Gió yếu"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "TWI identifies topographic depressions where air and pollutants can accumulate",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "Static factor: TWI is derived from DEM. High TWI indicates areas prone to accumulation"
}
```

### Example 7: Population Density → Emission Intensity → PM2.5
```json
{
  "id": "population_density_emissions_pm25_001",
  "cause_node": "population_density",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Mật độ dân cư cao → Nhiều hoạt động con người (giao thông, sưởi ấm, cooking) → Tổng lượng phát thải cao → PM2.5 cao hơn",
  "conditions": [
    "High population density",
    "Urban areas",
    "Nhiều hoạt động dân cư"
  ],
  "temporal_lag": "N/A (static factor)",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "High population density correlates with increased emissions from various sources",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Static factor: population density is relatively stable over short time periods"
}
```

## COMMON PITFALLS TO AVOID

1. **PHẢI ghi rõ đây là static factor**:
   - Temporal lag: N/A (static factor)
   - Notes: Static factor affects all time periods when conditions are met

2. **PHẢI phân biệt direct vs indirect effects**:
   - Direct: Topography → Air flow → PM2.5
   - Indirect: Population density → Emissions → PM2.5

3. **KHÔNG extract nếu không có mechanism rõ ràng**:
   - Phải giải thích TẠI SAO static factor lại ảnh hưởng đến PM2.5

4. **PHẢI ghi rõ spatial scope**:
   - Local: Ảnh hưởng tại chỗ
   - Regional: Có thể ảnh hưởng khu vực xung quanh

5. **PHẢI ghi rõ conditions khi nào effect xảy ra**:
   - Static factors không luôn luôn có effect
   - Cần điều kiện khí tượng phù hợp

## SPECIFIC VARIABLES TO EXTRACT

Đảm bảo extract relationships cho tất cả các biến sau:

### Static Factors:
- `population_density` → `emission_intensity`, `pm25`
- `urban_density` → `emission_sources`, `pm25`
- `urban_land_use` → `emission_patterns`, `pm25`
- `vegetation` → `deposition`, `pm25`
- `topography` → `air_flow`, `pm25`
- `valley_bottom` → `air_trapping`, `pm25`
- `topographic_wetness_index` → `air_flow`, `pm25`
- `distance_to_roads` → `traffic_exposure`, `pm25`
- `industrial_zones` → `emissions`, `pm25`

### Processes Affected:
- `air_flow` → `pm25`
- `air_trapping` → `pm25`
- `deposition` → `pm25`
- `emission_sources` → `pm25`
- `emission_patterns` → `pm25`
- `traffic_exposure` → `pm25`

## VALIDATION CHECKLIST

Trước khi output, kiểm tra:
- [ ] Temporal lag có được ghi là "N/A (static factor)" không?
- [ ] Mechanism có giải thích rõ cách static factor ảnh hưởng không?
- [ ] Conditions có được ghi rõ không? (static factors cần điều kiện khí tượng)
- [ ] Spatial scope có phù hợp không?
- [ ] Notes có ghi rõ đây là static factor không?
