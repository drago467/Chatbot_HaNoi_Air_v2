# PROMPT 01: METEOROLOGICAL PATHWAYS
# Focused Task: Extract causal relationships giữa các biến khí tượng và PM2.5
# Version: 2.0 - For Manus Auto-Discovery
# Category: meteorological_pathways

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers khoa học và extract causal relationships về các pathways khí tượng ảnh hưởng đến PM2.5, đặc biệt tập trung vào Hà Nội, Việt Nam và khu vực Đông Nam Á.

## CATEGORY DEFINITION
**Category**: `meteorological_pathways`

**Focus**: Các quá trình khí tượng ảnh hưởng đến sự tích tụ, khuếch tán, và vận chuyển của PM2.5 thông qua các cơ chế vật lý khí quyển.

## IN-SCOPE (Allowed Relationships)

### Core Meteorological Variables → Processes → PM2.5:
1. **Temperature → Inversion → PBLH → PM2.5**
   - Radiation inversion (ban đêm)
   - Subsidence inversion (áp cao)
   - Frontal inversion (cold front)

2. **Wind Speed → Dispersion → PM2.5**
   - Horizontal dispersion
   - Vertical mixing
   - Turbulent diffusion

3. **Wind Direction → Transport → PM2.5**
   - Regional transport
   - Long-range transport
   - Back-trajectory analysis

4. **Humidity → Processes → PM2.5**
   - Humidity → Wet Deposition → PM2.5 (via precipitation)
   - Humidity → Aerosol Liquid Water → Chemical Reactions → PM2.5 (if chemical pathways mentioned, note for handoff)

5. **Precipitation → Wet Deposition → PM2.5**
   - Rain scavenging
   - Snow scavenging

6. **Cloud Cover → Solar Radiation → PBLH → PM2.5**
   - Reduced solar radiation → Lower PBLH → Higher PM2.5

7. **Pressure → Atmospheric Stability → PM2.5**
   - High pressure → Subsidence → Inversion → PM2.5

8. **Solar Radiation → PBLH Development → PM2.5**
   - Daytime heating → PBLH growth → Better dispersion → Lower PM2.5

9. **Stability Index / LTS → Atmospheric Stability → PM2.5**
   - Lower Tropospheric Stability → Inversion → PM2.5

10. **Cold Surge → Weather Pattern → PM2.5**
    - Non-linear, delayed effect (initial decrease, then increase)

11. **Visibility → Fog/Mist → PM2.5** (measurement artifact only)
    - Hygroscopic growth → Measurement increase (not real increase)

12. **Dew Point → Condensation → PM2.5**
    - Condensation on particles → Size increase

### Allowed Intermediate Nodes:
- `inversion` (temperature inversion)
- `pblh` (planetary boundary layer height)
- `dispersion` (atmospheric dispersion)
- `atmospheric_stability` (stability conditions)
- `wet_deposition` (precipitation scavenging)
- `dry_deposition` (gravitational settling)
- `transport` (advection, regional transport)
- `aerosol_liquid_water` (only if mentioned in meteorological context)

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Chemical Processes (→ prompt_02):
- ❌ SO2 + NO2 + Humidity → SIA Formation → PM2.5
- ❌ NO2 + O3 + Solar Radiation → Nitrate Formation → PM2.5
- ❌ VOCs + NOx → O3 → Secondary Aerosols
- ❌ NH3 + HNO3 → Ammonium Nitrate → PM2.5
- **Action**: If encountered, note in `handoff_to_other_prompts: ["chemical_processes"]`

### Emission Sources (→ prompt_04):
- ❌ Traffic → NOx → PM2.5
- ❌ Industry → SO2 → PM2.5
- ❌ Biomass Burning → PM2.5 Primary
- **Action**: If encountered, note in `handoff_to_other_prompts: ["emission_sources"]`

### Static Factors (→ prompt_05):
- ❌ Urban Density → Emissions → PM2.5
- ❌ Topography → Air Flow → PM2.5
- **Action**: If encountered, note in `handoff_to_other_prompts: ["static_factors"]`

### Transport Details (→ prompt_03):
- ❌ Detailed back-trajectory analysis with source attribution
- ❌ Cross-boundary transport mechanisms
- **Note**: Basic wind direction → transport is IN-SCOPE, but detailed transport analysis → prompt_03

## DISCOVERY PHASE

### Search Strategy

**Primary Search Queries** (execute multiple searches):
1. "temperature inversion PM2.5 Hanoi Vietnam"
2. "planetary boundary layer height PM2.5 Southeast Asia"
3. "atmospheric dispersion PM2.5 monsoon"
4. "cold surge air pollution Vietnam"
5. "wet deposition PM2.5 precipitation"
6. "atmospheric stability PM2.5 inversion"

**Geographic Focus**:
- Primary: Hanoi, Vietnam, Red River Delta
- Secondary: Southeast Asia monsoon urban areas
- Tertiary: Similar climates (subtropical monsoon, high humidity)

**Temporal Focus**:
- Papers from 2015-2024 (preferred)
- Foundational papers (pre-2015) if still relevant
- Note if findings are time-specific

### Source Requirements

**Minimum Sources**:
- ≥ 6 Tier-1 sources (peer-reviewed papers) OR saturation reached
- Can include Tier-2 sources (official reports) for additional coverage

**Saturation Criteria**:
- Stop when 3 consecutive new sources add NO new mechanisms/relationships
- All major pathways in IN-SCOPE have been covered
- Quality threshold met: At least 6 Tier-1 sources with strong evidence

**Source Quality**:
- Tier-1: Peer-reviewed journals (Atmospheric Environment, ACP, ES&T, JGR, etc.)
- Tier-2: Official reports (Copernicus/CAMS, ECMWF, WMO, EPA, MONRE)
- Tier-3: Preprints, conference papers (use with caution)
- Tier-4: Wikipedia, blogs (discovery only, NOT as evidence)

### Bibliography Collection

For each source found, collect:
- Full title
- Authors
- Year
- URL/DOI
- Tier classification
- Relevance score (1-10)
- Key findings summary

## EXTRACTION PHASE

### Extraction Rules

1. **Only extract relationships in IN-SCOPE**
2. **Each relationship MUST have**:
   - Explicit mechanism (WHY + HOW)
   - Source quote supporting the relationship
   - Source metadata (URL, title, authors, year)
   - Conditions (thresholds, time periods, spatial scope)
   - Confidence assessment based on evidence quality

3. **If relationship is OUT-OF-SCOPE**:
   - Do NOT extract
   - Note in `handoff_to_other_prompts`

4. **If mechanism unclear**:
   - Do NOT invent
   - Note in `missing_info`
   - Set confidence = LOW if weak evidence

5. **If contradictory findings**:
   - Extract both with different confidence levels
   - Note in `contradictions` field

### Quality Filters

**Reject if**:
- Only correlation mentioned (no mechanism)
- Mechanism unclear or inferred
- No source quote available
- Source is Tier-4 (Wikipedia, blogs)

**Accept if**:
- Mechanism explicit and detailed
- Source quote directly supports relationship
- Source is Tier-1 or Tier-2
- Conditions clearly stated

### Maximum Relationships per Source

- Limit: 5-10 relationships per source (focus on strongest evidence)
- Prioritize relationships with:
  - Explicit mechanisms
  - Quantitative data
  - Clear conditions
  - High relevance to Hanoi/SE Asia

## OUTPUT FORMAT

```json
{
  "category": "meteorological_pathways",
  "bibliography": [
    {
      "source_title": "Full title",
      "source_authors": "Author1, Author2",
      "source_year": "2020",
      "source_url": "https://doi.org/...",
      "source_doi": "10.xxxx/...",
      "tier": "tier_1",
      "relevance_score": 9,
      "key_findings": "Brief summary"
    }
  ],
  "relationships": [
    {
      "id": "met_001",
      "cause_node": "temperature",
      "effect_node": "inversion",
      "relationship_type": "DIRECT_CAUSE",
      "mechanism": "Nhiệt độ giảm vào ban đêm → Mặt đất mất nhiệt nhanh → Lớp không khí sát đất lạnh hơn lớp trên → Nghịch nhiệt bức xạ hình thành",
      "conditions": [
        "Ban đêm (sau 18h)",
        "Trời quang mây",
        "Gió yếu (< 2 m/s)",
        "Mùa đông"
      ],
      "temporal_lag": "2-6h",
      "strength": "STRONG",
      "confidence": "HIGH",
      "source_url": "https://doi.org/...",
      "source_title": "...",
      "source_authors": "...",
      "source_year": "2020",
      "source_quote": "Radiation inversion occurs when the ground loses heat rapidly at night...",
      "source_locator": "Page 5, Section 2.1",
      "seasonal_variation": "winter",
      "spatial_scope": "local",
      "notes": "Most common type of inversion in Hanoi during winter"
    }
  ],
  "handoff_to_other_prompts": [
    "chemical_processes",
    "emission_sources"
  ],
  "missing_info": "Mechanism for frontal inversion in Hanoi needs more research",
  "contradictions": []
}
```

## VALIDATION CHECKLIST

Before output, verify:
- [ ] All relationships are IN-SCOPE?
- [ ] Each relationship has source_url, source_quote, source_title?
- [ ] Mechanism explains WHY + HOW?
- [ ] Conditions are specific (thresholds, time, spatial)?
- [ ] Confidence matches evidence quality?
- [ ] Bibliography has ≥6 Tier-1 sources OR saturation reached?
- [ ] OUT-OF-SCOPE relationships noted in handoff?
- [ ] No relationships without evidence?
- [ ] Nodes standardized (snake_case, English)?

## WORKFLOW SUMMARY

1. **Discovery**: Search for papers using multiple queries
2. **Collection**: Build bibliography with Tier classification
3. **Saturation Check**: Continue until ≥6 Tier-1 sources OR saturation
4. **Extraction**: Extract relationships with evidence
5. **Validation**: Check quality and completeness
6. **Output**: Generate JSON with bibliography + relationships

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for papers about meteorological pathways affecting PM2.5 in Hanoi, Vietnam and Southeast Asia.
