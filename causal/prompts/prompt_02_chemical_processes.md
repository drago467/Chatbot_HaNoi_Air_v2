# PROMPT 02: CHEMICAL PROCESSES
# Focused Task: Extract causal relationships về các phản ứng hóa học hình thành PM2.5
# Version: 2.0 - For Manus Auto-Discovery
# Category: chemical_processes

## SYSTEM CONTEXT
[Include prompt_00_master_template.md as system guardrails]

## TASK OVERVIEW
Bạn sẽ tự động tìm kiếm papers khoa học và extract causal relationships về các phản ứng hóa học hình thành secondary aerosols (SIA, SOA) và ảnh hưởng đến PM2.5, đặc biệt tập trung vào Hà Nội, Việt Nam và khu vực Đông Nam Á với độ ẩm cao.

## CATEGORY DEFINITION
**Category**: `chemical_processes`

**Focus**: Các phản ứng hóa học khí quyển (aqueous-phase, heterogeneous, photochemical) hình thành sol khí thứ cấp từ các tiền chất khí.

## IN-SCOPE (Allowed Relationships)

### Precursor → Chemical Reaction → Secondary Aerosol → PM2.5:

1. **SO2 + NO2 + Humidity → SIA Formation → PM2.5**
   - Aqueous-phase oxidation
   - SO2 → SO4^2- (sulfate)
   - NO2 → NO3^- (nitrate)

2. **SO2 + O3/H2O2 → Sulfate Formation → PM2.5**
   - Aqueous-phase oxidation with oxidants
   - Metal catalysis (Mn2+, Fe3+)

3. **NO2 + O3 + Solar Radiation → Nitrate Formation → PM2.5**
   - Photochemical + heterogeneous pathways
   - NO2 → HNO3 → NH4NO3

4. **NH3 + HNO3 → Ammonium Nitrate Formation → PM2.5**
   - Heterogeneous reaction
   - Temperature-dependent equilibrium

5. **VOCs + NOx + Solar Radiation → O3 Formation → Secondary Aerosols**
   - Photochemical smog formation
   - O3 as intermediate

6. **VOCs + OH Radical → SOA Formation → PM2.5**
   - Organic aerosol formation
   - Low volatility compounds

7. **NOx + VOCs + Solar Radiation → O3 → Secondary Aerosols**
   - NOx cycling
   - Radical chemistry

8. **Temperature → Chemical Reaction Rate → PM2.5**
   - Temperature dependence of reactions
   - NH4NO3 volatility

9. **Humidity → Aerosol Liquid Water → Chemical Reactions → PM2.5**
   - ALW formation
   - Deliquescence
   - Aqueous-phase reaction medium

10. **pH → Chemical Reaction Rate → PM2.5**
    - pH effects on aqueous reactions
    - NH3 neutralization

### Allowed Intermediate Nodes:
- `chemical_reaction` (general chemical processes)
- `aqueous_phase_reaction` (reactions in water phase)
- `heterogeneous_reaction` (surface reactions)
- `photochemistry` (photochemical reactions)
- `sia_formation` (secondary inorganic aerosols)
- `soa_formation` (secondary organic aerosols)
- `sulfate_formation` (SO4^2- formation)
- `nitrate_formation` (NO3^- formation)
- `ammonium_nitrate_formation` (NH4NO3 formation)
- `aerosol_liquid_water` (ALW, water coating on particles)
- `o3` (ozone as intermediate)

### Allowed Precursors:
- `so2`, `no2`, `nox`, `nh3`, `vocs`, `hno3`, `h2o2`, `o3`

## OUT-OF-SCOPE (Forbidden - Handoff to Other Prompts)

### Meteorological Processes (→ prompt_01):
- ❌ Temperature → Inversion → PBLH → PM2.5
- ❌ Wind Speed → Dispersion → PM2.5
- ❌ Humidity → Wet Deposition → PM2.5 (precipitation scavenging)
- **Action**: If encountered, note in `handoff_to_other_prompts: ["meteorological_pathways"]`

### Emission Sources (→ prompt_04):
- ❌ Traffic → NOx emissions
- ❌ Industry → SO2 emissions
- ❌ Source apportionment details
- **Action**: If encountered, note in `handoff_to_other_prompts: ["emission_sources"]`

### Transport Mechanisms (→ prompt_03):
- ❌ Wind Direction → Transport of precursors
- ❌ Regional transport of pollutants
- **Note**: Focus on chemical reactions, not transport of precursors

## DISCOVERY PHASE

### Search Strategy

**Primary Search Queries**:
1. "secondary inorganic aerosols SIA PM2.5 Hanoi Vietnam"
2. "aqueous phase reaction SO2 NO2 sulfate nitrate"
3. "ammonium nitrate formation temperature humidity"
4. "secondary organic aerosols SOA VOCs photochemistry"
5. "aerosol liquid water ALW chemical reactions"
6. "photochemical smog O3 formation Southeast Asia"

**Geographic Focus**:
- Primary: Hanoi, Vietnam, Red River Delta
- Secondary: High humidity regions (Southeast Asia, subtropical monsoon)
- Tertiary: Similar mechanisms globally (but note applicability)

**Temporal Focus**:
- Papers from 2015-2024 (preferred)
- Foundational chemistry papers (pre-2015) if still relevant

### Source Requirements

**Minimum Sources**:
- ≥ 6 Tier-1 sources (peer-reviewed papers) OR saturation reached
- Can include Tier-2 sources (official reports) for additional coverage

**Saturation Criteria**:
- Stop when 3 consecutive new sources add NO new mechanisms/relationships
- All major pathways in IN-SCOPE have been covered
- Quality threshold met: At least 6 Tier-1 sources with strong evidence

**Source Quality**:
- Tier-1: Peer-reviewed journals (Atmospheric Chemistry and Physics, Atmospheric Environment, ES&T, JGR, etc.)
- Tier-2: Official reports (Copernicus/CAMS, EPA, WHO)
- Tier-3: Preprints, conference papers (use with caution)

## EXTRACTION PHASE

### Extraction Rules

1. **Only extract relationships in IN-SCOPE**
2. **Each relationship MUST have**:
   - Explicit chemical mechanism (reaction pathway)
   - Source quote supporting the relationship
   - Source metadata (URL, title, authors, year)
   - Conditions (RH thresholds, temperature ranges, pH, presence of catalysts)
   - Confidence assessment based on evidence quality

3. **Chemical Mechanism Requirements**:
   - Must specify reaction type (aqueous-phase, heterogeneous, photochemical)
   - Must identify precursors and products
   - Must explain reaction conditions (RH, T, pH, catalysts)

4. **If relationship is OUT-OF-SCOPE**:
   - Do NOT extract
   - Note in `handoff_to_other_prompts`

5. **If mechanism unclear**:
   - Do NOT invent
   - Note in `missing_info`
   - Set confidence = LOW if weak evidence

### Quality Filters

**Reject if**:
- Only correlation mentioned (no mechanism)
- Chemical pathway unclear
- No source quote available
- Source is Tier-4 (Wikipedia, blogs)

**Accept if**:
- Chemical mechanism explicit and detailed
- Reaction pathway clearly described
- Source quote directly supports relationship
- Source is Tier-1 or Tier-2
- Conditions clearly stated (RH, T, pH, catalysts)

## OUTPUT FORMAT

```json
{
  "category": "chemical_processes",
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
      "id": "chem_001",
      "cause_node": "humidity",
      "effect_node": "sia_formation",
      "relationship_type": "MODERATOR",
      "mechanism": "Độ ẩm cao (>75%) → Hơi nước ngưng tụ trên hạt bụi → Tạo lớp áo nước (ALW) → SO2 và NO2 hòa tan vào ALW → Phản ứng với O3/H2O2 → Hình thành Sulfate và Nitrate",
      "conditions": [
        "RH > 75%",
        "Có SO2 và NO2",
        "pH > 4.5",
        "Có O3 hoặc H2O2",
        "Có kim loại chuyển tiếp (Mn2+, Fe3+) làm xúc tác"
      ],
      "temporal_lag": "4-12h",
      "strength": "STRONG",
      "confidence": "HIGH",
      "source_url": "https://doi.org/...",
      "source_title": "...",
      "source_authors": "...",
      "source_year": "2020",
      "source_quote": "High humidity promotes aqueous-phase reactions...",
      "source_locator": "Page 10, Section 3.2",
      "seasonal_variation": "winter",
      "spatial_scope": "local",
      "notes": "Non-linear relationship: RH > 75% promotes, but RH > 90% with fog may cause measurement artifact"
    }
  ],
  "handoff_to_other_prompts": [
    "meteorological_pathways",
    "emission_sources"
  ],
  "missing_info": "Mechanism for SOA formation from specific VOCs in Hanoi needs more research",
  "contradictions": []
}
```

## VALIDATION CHECKLIST

Before output, verify:
- [ ] All relationships are IN-SCOPE?
- [ ] Each relationship has source_url, source_quote, source_title?
- [ ] Chemical mechanism explains reaction pathway?
- [ ] Conditions include RH, T, pH, catalysts if relevant?
- [ ] Confidence matches evidence quality?
- [ ] Bibliography has ≥6 Tier-1 sources OR saturation reached?
- [ ] OUT-OF-SCOPE relationships noted in handoff?
- [ ] No relationships without evidence?
- [ ] Nodes standardized (snake_case, English)?

## WORKFLOW SUMMARY

1. **Discovery**: Search for papers about chemical processes
2. **Collection**: Build bibliography with Tier classification
3. **Saturation Check**: Continue until ≥6 Tier-1 sources OR saturation
4. **Extraction**: Extract relationships with evidence
5. **Validation**: Check quality and completeness
6. **Output**: Generate JSON with bibliography + relationships

---

**READY TO EXECUTE**: Begin with Discovery Phase - search for papers about chemical processes forming secondary aerosols in Hanoi, Vietnam and high humidity regions.
