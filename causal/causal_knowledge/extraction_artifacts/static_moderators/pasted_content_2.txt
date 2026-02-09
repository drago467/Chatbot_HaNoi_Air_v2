# PROMPT 12: STATIC FACTORS AS MODERATORS
# Focused Task: Extract causal relationships static factors as MODERATOR/INDIRECT_CAUSE affecting PM2.5 sensitivity
# Version: 2.0 - For Manus Auto-Discovery
# Category: static_factors

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## ROLE
Bạn là chuyên gia **GIS/địa lý đô thị và chất lượng không khí**, quen làm việc với:
- bản đồ sử dụng đất (LULC),
- mật độ dân số, mạng lưới đường, khu công nghiệp,
- mô hình hóa vai trò của các yếu tố tĩnh đối với PM2.5 (baseline và sensitivity).

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers/báo cáo khoa học và extract causal relationships về các **yếu tố tĩnh** (dân cư, đường xá, khu công nghiệp, LULC, địa hình/DEM) ảnh hưởng đến PM2.5 theo 2 hướng:

1) **Ảnh hưởng nền** (baseline risk): khu vực có đặc điểm tĩnh nào thường có PM2.5 cao hơn vì cơ chế hợp lý.  
2) **Vai trò MODERATOR**: yếu tố tĩnh làm mạnh/yếu các quan hệ khác (emissions/meteorology → PM2.5).

Mục tiêu: mô hình hóa static factors theo hướng **MODERATOR** thay vì chỉ “direct cause” một bước.

## CATEGORY DEFINITION
**Category**: `static_factors`

**Focus**: Urban form & geography moderators of PM2.5.

## IN-SCOPE (Allowed Relationships)

### A) Population / urbanization
1. **population_density → pm25** (INDIRECT_CAUSE; mechanism must be emissions/activity mediated)
2. **urban_expansion/built_up_fraction → pm25** (INDIRECT_CAUSE)

### B) Roads / near-road exposure
3. **road_network_density → pm25**
4. **distance_to_major_road → pm25 (negative_exponential_decay)**

### C) Industrial zones
5. **industrial_zones_proximity → pm25**
6. **downwind_of_industrial_zones (static+wind geometry if paper treats as spatial factor) → pm25**

### D) LULC / vegetation moderators
7. **lulc_construction_land → pm25**
8. **lulc_vegetation → pm25 (decrease via dry deposition)**

### E) Topography / valley-basin trapping (moderator for stagnation/inversion)
9. **dem_topography_valley_basin → stagnation/inversion_persistence → pm25** (prefer MEDIATOR chain)
10. **topographic_trapping → reduced_dispersion → pm25**

### Allowed Intermediate Nodes
- `dry_deposition`, `reduced_dispersion`, `stagnation`, `inversion_persistence`
- `near_road_exposure`, `urban_activity_intensity`

### Preferred Relationship Types
- Use `MODERATOR` when the paper explicitly says static factor increases sensitivity of PM2.5 to emissions/meteorology.
- Use `INDIRECT_CAUSE` when mechanism is mediated (e.g., population density → more traffic → PM2.5).
- Use `DIRECT_CAUSE` only if the paper clearly justifies a direct mechanism (rare for static).

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Detailed emission mechanisms (→ prompt_04)
- ❌ emission factor, inventory numbers
- Action: handoff_to_other_prompts ["emission_sources"]

### Detailed meteorology physics (→ prompt_01)
- ❌ inversion micro-physics not tied to topography moderators
- Action: handoff_to_other_prompts ["meteorological_pathways"]

## DISCOVERY PHASE

### Search Strategy (run multiple queries)
1. "urban expansion land use land cover PM2.5 Hanoi Vietnam"
2. "distance to road PM2.5 exponential decay near-road exposure"
3. "industrial zones proximity PM2.5 hotspots Hanoi"
4. "urban vegetation dry deposition PM2.5 reduction"
5. "valley basin topography cold air pool PM2.5 trapping"
6. "population density road density PM2.5 spatial drivers Hanoi"

### Source Requirements
- ≥ 6 Tier-1 sources OR saturation reached
- GIS/remote-sensing papers allowed if they provide causal mechanism text (not only correlations)

### Saturation Rule
Dừng khi 3 nguồn liên tiếp không bổ sung thêm cơ chế moderator hoặc điều kiện mới (distance decay, vegetation deposition, topographic trapping).

## EXTRACTION PHASE

### Extraction Rules
1. Chỉ extract nếu mechanism rõ (traffic intensity, industrial hotspots, dry deposition, topographic trapping).
2. Evidence bắt buộc cho mỗi relationship.
3. Nếu paper chỉ chạy regression “correlated” mà không mô tả cơ chế → confidence tối đa MEDIUM; hoặc đưa vào missing_info theo guardrails.
4. Nếu paper nói static factor làm tăng/giảm sensitivity → ưu tiên `MODERATOR`.
5. Mỗi nguồn tối đa 10 relationships.

## OUTPUT FORMAT (JSON)
Use schema from `prompt_00_master_template.md`, with `category: "static_factors"`.

## EXAMPLES OF GOOD EXTRACTIONS

```json
{
  "id": "static_road_001",
  "category": "static_factors",
  "cause_node": "distance_to_major_road",
  "effect_node": "pm25",
  "relationship_type": "INDIRECT_CAUSE",
  "mechanism": "Nồng độ PM2.5 giảm nhanh khi khoảng cách tới các tuyến đường giao thông chính tăng lên, do sự pha loãng và khuếch tán của khí thải xe cộ và bụi tái huy động. Mối quan hệ thường được mô tả bằng hàm suy giảm mũ theo khoảng cách.",
  "conditions": [
    "Distance from major road increasing from 5 m to 30 m",
    "Urban roadside environment"
  ],
  "temporal_lag": "N/A",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://www.sciencedirect.com/science/article/pii/S1361920920306295",
  "source_title": "Influence of roadway emissions on near-road PM2.5: Monitoring data analysis and implications",
  "source_authors": "Zhu et al.",
  "source_year": "2020",
  "source_doi": "10.1016/j.trd.2020.102442",
  "source_quote": "PM2.5 increments decreased by about 75% between 5 m and 30 m from the edge of the roadway.",
  "source_locator": "Results",
  "seasonal_variation": "all_season",
  "spatial_scope": "local",
  "notes": "Có thể kết hợp với thông tin về traffic volume để mô hình hóa sensitivity theo khoảng cách."
}
```

```json
{
  "id": "static_topo_001",
  "category": "static_factors",
  "cause_node": "dem_topography_valley_basin",
  "effect_node": "pm25",
  "relationship_type": "MODERATOR",
  "mechanism": "Địa hình thung lũng/lòng chảo tạo điều kiện hình thành và duy trì các vũng không khí lạnh (cold-air pools), làm kéo dài thời gian tồn tại của nghịch nhiệt và hạn chế pha trộn thẳng đứng. Điều này khiến cùng một mức phát thải và điều kiện khí tượng nhưng khu vực lòng chảo có PM2.5 cao hơn vùng lân cận cao hơn.",
  "conditions": [
    "Valley/basin topography",
    "Persistent stable conditions during winter",
    "Cold-air pool episodes"
  ],
  "temporal_lag": "1-3d",
  "strength": "STRONG",
  "confidence": "HIGH",
  "source_url": "https://www.sciencedirect.com/science/article/pii/S1352231011011204",
  "source_title": "Wintertime PM2.5 concentrations during persistent, multi-day cold-air pools in a mountain valley",
  "source_authors": "Silcox et al.",
  "source_year": "2012",
  "source_doi": "10.1016/j.atmosenv.2011.10.041",
  "source_quote": "During cold-air pool events, PM2.5 concentrations can reach 100 µg m−3, and concentrations decrease by about 30% when elevation increases from 1300 m to 1600 m within the valley.",
  "source_locator": "Abstract/Results",
  "seasonal_variation": "winter",
  "spatial_scope": "local",
  "notes": "Static factor dem_topography_valley_basin làm MODERATOR cho các quan hệ inversion/stagnation → pm25."
}
```

## COMMON PITFALLS TO AVOID
- Ghi static như DIRECT_CAUSE mà không có mechanism trung gian.
- Không chuẩn hóa node (distance_to_major_road, road_network_density, industrial_zones_proximity, lulc_vegetation, dem_topography_valley_basin).
- Diễn giải chỉ dựa vào tương quan thống kê mà không có giải thích về traffic/industry/dispersion/dry deposition.


