# Prompt 19: Proxy Validation and Research

**Task ID:** 19  
**Category:** Validation & Research  
**Priority:** High  
**Status:** Pending  
**Assigned To:** Manus  
**Deadline:** 2025-01-28  

---

## 1. Research Objectives

Validate and enhance the scientific foundation of proxy strategies used in the Hanoi Air Quality Knowledge Graph. For each proxy, we need:

1. **Literature Review**: Find peer-reviewed papers that either:
   - Propose similar proxy methods
   - Validate the scientific basis of our approach
   - Suggest alternative/better methods

2. **Validation Data**: Where possible, identify datasets that could be used to validate the proxy against direct measurements.

3. **Confidence Assessment**: Based on literature, assess if our current approach has high/medium/low confidence.

---

## 2. Proxies to Research

### 2.1. PBLH (Planetary Boundary Layer Height) Proxy

**Current Approach:**
```
PBLH = base_height × wind_factor × cloud_factor × time_factor × temp_factor
Where:
- base_height = 150 m
- wind_factor = 1 + (wind_speed / 4.0)
- cloud_factor = max(0.4, 1 - (cloud_cover / 150))
- time_factor = diurnal variation (0.4-1.5)
- temp_factor = 1 + 0.02 × (temperature - 20)
```

**Research Questions:**
1. Are there published formulas for estimating PBLH from surface variables that we should be using instead?
2. What are typical coefficient values used in the literature for similar empirical formulas?
3. Are there studies validating similar approaches for Southeast Asian megacities?

**References to Check:**
- Su et al. (2018) - Already referenced, but look for more recent work
- Search for: "empirical PBLH estimation urban areas"
- Focus on studies in tropical/subtropical climates

### 2.2. Atmospheric Stability Proxy

**Current Approach:**
Simplified Pasquill-Gifford stability classes based on:
- Wind speed
- Cloud cover
- Time of day (day/night)

**Research Questions:**
1. What are standard methods for estimating atmospheric stability when vertical profiles are not available?
2. Are there validated simplified stability classification schemes for urban areas?
3. How does the diurnal cycle of stability vary in tropical megacities like Hanoi?

**Note:** We found that Open-Meteo does NOT provide direct stability indices (no CAPE, lifted_index), so we need surface-based approaches.

### 2.3. Aerosol Liquid Water (ALW) Proxy

**Current Approach:**
```
If RH < 70%: ALW ≈ 0
Elif RH < 80%: ALW ≈ 0.1 * (RH - 70) / 10
Elif RH < 90%: ALW ≈ 0.1 + 0.3 * (RH - 80) / 10
Else: ALW ≈ 0.4 + 0.6 * (RH - 90) / 10
```

**Research Questions:**
1. What are the established relationships between RH and ALW in the literature?
2. Are there parameterizations that include temperature or aerosol composition?
3. How does ALW vary between clean and polluted conditions?

### 2.4. Cold Surge Detection

**Current Approach:**
```
If pressure > 1020 hPa AND wind_direction in [0-90] AND temperature < 15°C:
    cold_surge_phase = "onset" or "persistence"
```

**Research Questions:**
1. What are the standard meteorological criteria for cold surges in Southeast Asia?
2. How do these criteria vary between different regions (e.g., Northern Vietnam vs. Southern China)?
3. Are there studies on the impact of cold surges on air quality in Hanoi?

### 2.5. Upwind Emission Exposure

**Current Approach:**
```
exposure = 2 * industrial_zones + 1 * road_density + 1.5 * traffic_factor
```

**Research Questions:**
1. How is upwind source exposure typically quantified in air quality studies?
2. What weightings are used for different source types in literature?
3. Are there studies that validate these approaches with measurements?

---

## 3. Expected Deliverables

For each proxy, please provide:

1. **Literature Review Summary**
   - Key papers (with citations)
   - Main findings relevant to our approach
   - Confidence assessment (High/Medium/Low)

2. **Recommendations**
   - Keep current approach (with justification)
   - Modify approach (specific changes suggested)
   - Alternative approach (with references)

3. **Validation Strategy**
   - How could we validate this proxy with available data?
   - What additional data would be helpful?

---

## 4. Format

Please structure your response as a Markdown document with the following sections for EACH proxy:

```markdown
## [Proxy Name]

### Literature Review
[Summary of findings from papers]

### Assessment of Current Approach
[Strengths/weaknesses based on literature]

### Recommendations
1. [Specific recommendation]
2. [Alternative approaches if applicable]
3. [Validation suggestions]

### Key References
- [Full citation with DOI/link]
```

---

## 5. Timeline

- **Start**: [Date]
- **First draft due**: [Date + 3 days]
- **Final delivery**: [Date + 5 days]

---

## 6. Additional Notes

- Focus on papers from the last 10 years where possible
- Prioritize studies in tropical/subtropical regions
- Include both observational and modeling studies
- Note any datasets used for validation in the papers

Let me know if you need any clarification or have questions about specific proxies!