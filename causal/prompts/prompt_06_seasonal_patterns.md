## PROMPT 06: SEASONAL PATTERNS
# Focused Task: Extract causal relationships về quy luật theo mùa/ngày-đêm/sự kiện ảnh hưởng PM2.5
# Version: 2.0 - For Manus Auto-Discovery
# Category: seasonal_patterns

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về **pattern theo mùa (winter/summer/monsoon), chu kỳ ngày-đêm (diurnal), và sự kiện (holiday/harvest burning)** tác động đến PM2.5 tại Hà Nội/Vietnam/SEA.

## CATEGORY DEFINITION
**Category**: `seasonal_patterns`

**Focus**: Temporal drivers (season/time-of-day/events) và cơ chế làm thay đổi PM2.5 (thường qua meteorology/emissions). Prompt này ghi nhận “pattern causal” + điều kiện, và handoff phần cơ chế sâu sang prompt khác khi cần.

## IN-SCOPE (Allowed Relationships)

### Seasonal drivers
1. **season_winter → atmospheric_stability/inversion_frequency → pm25** (INDIRECT_CAUSE; evidence phải rõ)
2. **season_summer → pblh_growth/precipitation_frequency → pm25 (decrease)** (nếu được nguồn support)
3. **season_dry → biomass_burning_activity → pm25**
4. **season_wet → precipitation_frequency → pm25 (decrease via wet deposition)**

### Diurnal drivers
5. **time_of_day_night → inversion/pblh_low → pm25 (increase)**
6. **time_of_day_morning → pblh_minimum → pm25_peak**
7. **time_of_day_afternoon → pblh_maximum → pm25_minimum**
8. **time_of_day_rush_hour → traffic_activity → pm25** (nếu có evidence và cơ chế)

### Event-based
9. **month_harvest → open_burning_activity → pm25**
10. **holiday_period → traffic_reduction → pm25 (decrease)** (nếu có evidence)
11. **holiday_period → fireworks/burning → pm25 (increase)** (nếu có evidence)

### Allowed Intermediate Nodes
- `inversion_frequency`, `atmospheric_stability`, `pblh_low`, `pblh_growth`, `precipitation_frequency`
- `biomass_burning_activity`, `open_burning_activity`, `traffic_activity`, `traffic_reduction`, `fireworks_activity`

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Meteorological mechanisms (→ prompt_01)
- ❌ detailed inversion physics, PBLH dynamics
- Action: handoff_to_other_prompts ["meteorological_pathways"]

### Emission mechanism details (→ prompt_04)
- ❌ emission factors, source inventory details
- Action: handoff_to_other_prompts ["emission_sources"]

### Chemical formation (→ prompt_02)
- ❌ SIA/SOA chemistry pathways
- Action: handoff_to_other_prompts ["chemical_processes"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "seasonal variation PM2.5 Hanoi winter summer"
2. "diurnal cycle boundary layer PM2.5 urban"
3. "cold surge delayed PM2.5 Hanoi"
4. "harvest season open burning Vietnam PM2.5"
5. "holiday traffic reduction air pollution PM2.5"
6. "monsoon precipitation wet deposition PM2.5"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- Tier-2 official reports allowed (meteorological agencies, air quality reports)

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract IN-SCOPE temporal relationships.
2. Mỗi relationship bắt buộc có quote/URL/locator.
3. Nếu “season/time-of-day” chỉ được nói như pattern thống kê mà không có cơ chế → confidence tối đa MEDIUM, và ghi rõ limitation trong notes.
4. Nếu mechanism cần chi tiết (PBLH/inversion) → handoff để prompt_01 xử lý sâu.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "seasonal_patterns"`.

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for papers about seasonal/diurnal/event-driven PM2.5 patterns relevant to Hanoi/Vietnam/SEA.

## KEY MECHANISMS TO LOOK FOR

### Seasonal Variations:
- **Winter**: Nhiệt độ thấp → Nghịch nhiệt → PBLH thấp → PM2.5 cao
- **Summer**: Nhiệt độ cao → PBLH cao → PM2.5 thấp hơn
- **Dry season**: Đốt rơm rạ → Biomass burning → PM2.5 cao
- **Wet season**: Mưa nhiều → Wet deposition → PM2.5 thấp

### Diurnal Patterns:
- **Night**: Nhiệt độ giảm → Nghịch nhiệt → PBLH thấp → PM2.5 cao
- **Morning**: PBLH thấp nhất → PM2.5 đỉnh
- **Afternoon**: PBLH cao nhất → PM2.5 thấp nhất
- **Evening**: Rush hour + PBLH giảm → PM2.5 tăng

### Event-based Patterns:
- **Holidays**: Traffic giảm → PM2.5 giảm (nhưng có thể tăng do fireworks)
- **Festivals**: Fireworks, burning → PM2.5 tăng
- **Harvest seasons**: Biomass burning → PM2.5 tăng

### Cyclical Patterns:
- **Weekly**: Weekday vs Weekend traffic patterns
- **Monthly**: Agricultural cycles, heating seasons
- **Yearly**: Seasonal cycles

## EXAMPLES OF GOOD EXTRACTIONS

### Example 1: Season (Winter) → Weather Pattern → PM2.5
```json
{
  "id": "season_winter_pm25_001",
  "cause_node": "season_winter",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Mùa đông → Nhiệt độ thấp → Nghịch nhiệt thường xuyên → PBLH thấp → PM2.5 cao. Đồng thời, mùa đông → Nhu cầu sưởi ấm tăng → Phát thải tăng. Gió mùa Đông Bắc → Vận chuyển ô nhiễm từ phía Bắc",
  "conditions": [
    "Tháng 10-3",
    "Hà Nội",
    "Nhiệt độ < 20°C"
  ],
  "temporal_lag": "N/A (seasonal factor)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Winter pollution episodes in Hanoi are characterized by low temperatures, frequent inversions, and low PBLH",
  "seasonal_variation": "winter",
  "spatial_scope": "regional",
  "notes": "Seasonal factor: winter is the peak pollution season in Hanoi. Multiple mechanisms contribute: meteorological (inversion, low PBLH) and emission (heating, transport)"
}
```

### Example 2: Time of Day (Night) → PBLH → PM2.5
```json
{
  "id": "time_night_pblh_pm25_001",
  "cause_node": "time_of_day_night",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Ban đêm → Nhiệt độ giảm → Nghịch nhiệt hình thành → PBLH giảm → PM2.5 tăng. Sáng sớm → PBLH thấp nhất → PM2.5 đỉnh",
  "conditions": [
    "18h-8h",
    "Trời quang mây",
    "Gió yếu",
    "Mùa đông"
  ],
  "temporal_lag": "2-6h",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Nighttime and early morning show highest PM2.5 concentrations due to low PBLH and inversions",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "Diurnal pattern: PM2.5 peaks in early morning (6-8h) when PBLH is lowest"
}
```

### Example 3: Month (Harvest Season) → Agricultural Activity → Biomass Burning → PM2.5
```json
{
  "id": "month_harvest_biomass_pm25_001",
  "cause_node": "month_harvest",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Mùa thu hoạch (tháng 5-6, 9-10) → Đốt rơm rạ sau thu hoạch → Biomass burning → Phát thải PM2.5 sơ cấp + VOCs + NOx → PM2.5 tăng",
  "conditions": [
    "Tháng 5-6 (thu hoạch lúa xuân)",
    "Tháng 9-10 (thu hoạch lúa mùa)",
    "Rural areas",
    "Không có mưa",
    "Gió yếu đến trung bình"
  ],
  "temporal_lag": "0-6h (direct), 4-12h (SOA)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Harvest seasons show increased biomass burning activities, contributing to PM2.5",
  "seasonal_variation": "dry_season",
  "spatial_scope": "regional",
  "notes": "Monthly pattern: peaks during harvest months. Can be transported to urban areas"
}
```

### Example 4: Holiday Period → Traffic Pattern → PM2.5
```json
{
  "id": "holiday_traffic_pm25_001",
  "cause_node": "holiday_period",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Lễ hội/Tết → Traffic giảm (nhiều người về quê) → Phát thải từ traffic giảm → PM2.5 giảm. Tuy nhiên, có thể tăng do fireworks và đốt vàng mã",
  "conditions": [
    "Tết Nguyên Đán",
    "Các lễ hội lớn",
    "Urban areas"
  ],
  "temporal_lag": "1-3 days",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "During holidays, traffic decreases but fireworks and burning activities may increase",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Event-based pattern: effect depends on specific holiday activities. Traffic reduction vs fireworks/burning"
}
```

### Example 5: Time of Day (Rush Hour) → Emission Intensity → PM2.5
```json
{
  "id": "rush_hour_emissions_pm25_001",
  "cause_node": "time_of_day_rush_hour",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Rush hour (7-9h, 17-19h) → Traffic tăng → Phát thải từ traffic tăng (NOx, PM2.5 primary) → PM2.5 tăng. Đồng thời, buổi sáng PBLH thấp → Tăng tác động",
  "conditions": [
    "7-9h (morning rush)",
    "17-19h (evening rush)",
    "Weekdays",
    "Urban areas"
  ],
  "temporal_lag": "1-2h",
  "strength": "MODERATE",
  "confidence": "MEDIUM",
  "evidence_text": "Rush hour traffic increases emissions, contributing to PM2.5",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Diurnal pattern: peaks during rush hours, especially morning when PBLH is low"
}
```

### Example 6: Weekday vs Weekend → Traffic Pattern → PM2.5
```json
{
  "id": "weekday_weekend_traffic_pm25_001",
  "cause_node": "weekday",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Ngày trong tuần → Traffic cao hơn → Phát thải từ traffic cao hơn → PM2.5 cao hơn. Cuối tuần → Traffic giảm → PM2.5 giảm",
  "conditions": [
    "Weekdays (Monday-Friday)",
    "Urban areas",
    "Rush hours"
  ],
  "temporal_lag": "1-2h",
  "strength": "WEAK",
  "confidence": "LOW",
  "evidence_text": "Weekday traffic patterns differ from weekends, affecting emissions",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Weekly pattern: effect is relatively weak compared to seasonal and diurnal patterns"
}
```

### Example 7: Season (Summer) → Temperature → PBLH → PM2.5
```json
{
  "id": "season_summer_temp_pblh_pm25_001",
  "cause_node": "season_summer",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Mùa hè → Nhiệt độ cao → Đối lưu mạnh → PBLH cao → Khuếch tán tốt → PM2.5 thấp hơn. Đồng thời, mùa hè → Mưa nhiều → Wet deposition → PM2.5 giảm",
  "conditions": [
    "Tháng 5-9",
    "Hà Nội",
    "Nhiệt độ > 25°C"
  ],
  "temporal_lag": "N/A (seasonal factor)",
  "strength": "STRONG",
  "confidence": "HIGH",
  "evidence_text": "Summer shows lower PM2.5 due to higher PBLH and more precipitation",
  "seasonal_variation": "summer",
  "spatial_scope": "local",
  "notes": "Seasonal factor: summer is the cleanest season in Hanoi due to meteorological conditions"
}
```

## COMMON PITFALLS TO AVOID

1. **PHẢI ghi rõ seasonal_variation field**:
   - winter, summer, dry_season, wet_season, all_season

2. **PHẢI phân biệt seasonal vs diurnal patterns**:
   - Seasonal: Mùa đông vs mùa hè
   - Diurnal: Ban đêm vs ban ngày

3. **KHÔNG extract nếu không có mechanism giải thích tại sao mùa đó lại có effect**:
   - Phải giải thích cơ chế khí tượng hoặc emission pattern

4. **PHẢI ghi rõ temporal lag**:
   - Seasonal factors: N/A (seasonal factor)
   - Diurnal factors: 1-6h
   - Event-based: 1-3 days

5. **PHẢI ghi rõ conditions**:
   - Thời gian cụ thể (tháng, giờ)
   - Điều kiện khí tượng

## SPECIFIC VARIABLES TO EXTRACT

Đảm bảo extract relationships cho tất cả các biến sau:

### Temporal/Seasonal Factors:
- `season_winter` → `weather_pattern`, `emission_pattern`, `pm25`
- `season_summer` → `weather_pattern`, `pm25`
- `season_dry` → `biomass_burning`, `pm25`
- `season_wet` → `wet_deposition`, `pm25`
- `time_of_day_night` → `pblh`, `inversion`, `pm25`
- `time_of_day_morning` → `pblh`, `pm25`
- `time_of_day_afternoon` → `pblh`, `pm25`
- `time_of_day_evening` → `emission_intensity`, `pblh`, `pm25`
- `time_of_day_rush_hour` → `emission_intensity`, `pm25`
- `month_harvest` → `biomass_burning`, `pm25`
- `holiday_period` → `traffic_pattern`, `pm25`
- `weekday` → `traffic_pattern`, `pm25`
- `weekend` → `traffic_pattern`, `pm25`

### Patterns:
- `weather_pattern` → `pm25`
- `emission_pattern` → `pm25`
- `traffic_pattern` → `pm25`
- `diurnal_cycle` → `pblh_variation`, `pm25`

## VALIDATION CHECKLIST

Trước khi output, kiểm tra:
- [ ] Seasonal variation có được ghi rõ không?
- [ ] Temporal lag có phù hợp với pattern type không?
- [ ] Mechanism có giải thích tại sao mùa/thời gian đó lại có effect không?
- [ ] Conditions có được ghi rõ không? (tháng, giờ, điều kiện)
- [ ] Có phân biệt được seasonal vs diurnal vs event-based không?
