# PROMPT 03: TRANSPORT MECHANISMS
# Focused Task: Extract causal relationships về vận chuyển và lan truyền ô nhiễm
# Version: 2.0 - For Manus Auto-Discovery
# Category: transport_mechanisms

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers khoa học và extract causal relationships về các cơ chế vận chuyển và lan truyền ô nhiễm (advection, back-trajectory, regional transport), đặc biệt tập trung vào Hà Nội, Việt Nam và vận chuyển xuyên biên giới trong khu vực Đông Nam Á.

## CATEGORY DEFINITION
**Category**: `transport_mechanisms`

**Focus**: Các quá trình vận chuyển ô nhiễm trong khí quyển (advection, diffusion, back-trajectory analysis) và ảnh hưởng đến PM2.5 tại điểm nhận.

## IN-SCOPE (Allowed Relationships)

### Transport Pathways:

1. **Wind Direction + Emission Sources → Regional Transport → PM2.5**
   - Advection from source regions
   - Source attribution via back-trajectory

2. **Wind Speed → Transport Distance → PM2.5**
   - Transport distance calculation
   - Effect on PM2.5 at receptor

3. **Cold Surge → Wind Pattern → PM2.5** (non-linear, delayed)
   - Initial decrease (strong winds)
   - Delayed increase (stabilization)

4. **Long-range Transport → Background Pollution → PM2.5**
   - Cross-boundary transport
   - Transboundary pollution

5. **Topography → Air Flow → PM2.5 Accumulation**
   - Valley flow
   - Mountain blocking
   - Channeling effects

6. **Back-trajectory Analysis → Source Identification → PM2.5**
   - Air mass origin
   - Pathway identification
   - Source attribution

7. **Wind Direction + Industrial Areas → Transport → PM2.5**
   - Industrial plume transport
   - Specific source regions

8. **Wind Direction + Biomass Burning → Transport → PM2.5**
   - Biomass burning plume transport
   - Seasonal patterns

### Allowed Intermediate Nodes:
- `transport` (general transport)
- `regional_transport` (regional scale)
- `long_range_transport` (cross-boundary)
- `back_trajectory` (trajectory analysis)
- `air_flow` (atmospheric flow patterns)
- `plume` (pollution plume)

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Meteorological Processes (→ prompt_01):
- ❌ Wind Speed → Dispersion → PM2.5 (local dispersion)
- ❌ Temperature → Inversion → PBLH → PM2.5
- **Action**: If encountered, note in `handoff_to_other_prompts: ["meteorological_pathways"]`

### Emission Sources (→ prompt_04):
- ❌ Traffic → NOx emissions
- ❌ Industry → SO2 emissions
- ❌ Source emission factors
- **Note**: Transport OF emissions is IN-SCOPE, but emission rates themselves → prompt_04

### Chemical Processes (→ prompt_02):
- ❌ Chemical reactions during transport
- ❌ Secondary aerosol formation during transport
- **Note**: Focus on physical transport, not chemical transformation

## DISCOVERY PHASE

### Search Strategy

**Primary Search Queries**:
1. "back trajectory analysis PM2.5 Hanoi Vietnam"
2. "regional transport air pollution Southeast Asia"
3. "cross boundary transport PM2.5 Vietnam China"
4. "wind direction transport industrial sources"
5. "topography air flow pollution accumulation"
6. "cold surge transport air pollution Vietnam"

**Geographic Focus**:
- Primary: Hanoi, Vietnam, Red River Delta
- Secondary: Cross-boundary transport (Vietnam-China, Vietnam-Laos-Thailand)
- Tertiary: Regional transport in Southeast Asia

**Temporal Focus**:
- Papers from 2015-2024 (preferred)
- Foundational transport papers (pre-2015) if still relevant

### Source Requirements

**Minimum Sources**:
- ≥ 6 Tier-1 sources OR saturation reached

**Saturation Criteria**:
- Stop when 3 consecutive new sources add NO new mechanisms
- All major pathways covered
- Quality threshold: ≥6 Tier-1 sources

## EXTRACTION PHASE

### Extraction Rules

1. **Only extract relationships in IN-SCOPE**
2. **Each relationship MUST have**:
   - Explicit transport mechanism (advection, diffusion, trajectory)
   - Source quote supporting the relationship
   - Source metadata
   - Conditions (wind direction, speed, distance, topography)
   - Spatial scope (local, regional, cross-boundary)

3. **Transport Mechanism Requirements**:
   - Must specify transport type (advection, diffusion, trajectory)
   - Must identify source region if applicable
   - Must explain transport distance/time

## OUTPUT FORMAT

```json
{
  "category": "transport_mechanisms",
  "bibliography": [...],
  "relationships": [
    {
      "id": "trans_001",
      "cause_node": "wind_direction",
      "effect_node": "pm25",
      "relationship_type": "MODERATOR",
      "mechanism": "Gió từ hướng có nguồn phát thải công nghiệp → Vận chuyển pollutants → PM2.5 tăng tại điểm nhận",
      "conditions": [
        "Gió từ hướng có industrial sources",
        "Wind speed 2-5 m/s",
        "Không có precipitation",
        "Mùa đông"
      ],
      "temporal_lag": "6-24h",
      "strength": "MODERATE",
      "confidence": "HIGH",
      "source_url": "...",
      "source_title": "...",
      "source_authors": "...",
      "source_year": "...",
      "source_quote": "...",
      "source_locator": "...",
      "seasonal_variation": "winter",
      "spatial_scope": "regional",
      "notes": "..."
    }
  ],
  "handoff_to_other_prompts": [...],
  "missing_info": "...",
  "contradictions": []
}
```

## VALIDATION CHECKLIST

Before output, verify:
- [ ] All relationships are IN-SCOPE?
- [ ] Each relationship has source_url, source_quote, source_title?
- [ ] Transport mechanism explains HOW pollutants are transported?
- [ ] Spatial scope is specified (local/regional/cross-boundary)?
- [ ] Confidence matches evidence quality?
- [ ] Bibliography has ≥6 Tier-1 sources OR saturation reached?

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for papers about transport mechanisms affecting PM2.5 in Hanoi, Vietnam and Southeast Asia.
