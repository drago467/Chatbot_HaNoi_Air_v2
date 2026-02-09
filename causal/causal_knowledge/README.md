# Causal Knowledge Graph - Extracted Relationships

## Tổng quan

Thư mục này chứa Causal Knowledge Graph (CKG) hoàn chỉnh về PM2.5 tại Hà Nội, được xây dựng từ 18 prompts chuyên biệt và trích xuất từ hơn 90 bài báo khoa học.

**Phiên bản hiện tại**: v2.1 (2026-01-24)

## 📊 Thống kê CKG

| Metric | Giá trị | Mô tả |
|--------|---------|-------|
| **Relationships** | 205 | Số mối quan hệ nhân quả |
| **Nodes** | 116 | Số yếu tố/biến |
| **Edges** | 143 | Số cạnh đồ thị |
| **PM2.5 In-Degree** | 63 | Số yếu tố ảnh hưởng trực tiếp đến PM2.5 |
| **Sources** | 90+ | Số bài báo khoa học (>90% Tier 1) |
| **Quality Score** | 96.5% | Điểm chất lượng tổng hợp |

## Cấu trúc Thư mục

```
causal_knowledge/
├── extracted_relationships/     # JSON kết quả từ Manus (18 files)
│   ├── Core prompts (01-07):
│   │   ├── meteorological_pathways.json
│   │   ├── chemical_processes.json
│   │   ├── transport_mechanisms.json
│   │   ├── emission_sources.json
│   │   ├── static_factors.json
│   │   ├── seasonal_patterns.json
│   │   └── edge_cases.json
│   ├── Gap-focused prompts (08-15):
│   │   ├── winter_chemistry_sia.json
│   │   ├── precipitation_wet_scavenging.json
│   │   ├── synoptic_cold_surge_transport.json
│   │   ├── wind_direction_upwind_exposure.json
│   │   ├── static_moderators.json
│   │   ├── fog_visibility_artifacts.json
│   │   ├── cold_surge_chain.json
│   │   └── meteorological_core_variables.json
│   └── Advanced prompts (16-18):
│       ├── precipitation_paradox.json      # Light rain paradox, ALW, fog effects
│       ├── aerosol_chemistry_advanced.json # pH, partitioning, catalysis
│       └── photochemistry_complete.json    # SOA, cloud-photolysis, radical chemistry
├── extraction_artifacts/       # Artifacts từ quá trình Manus extract
│   └── (18 folders corresponding to prompts)

```

## Cấu trúc Files

### 1. meteorological_pathways.json
- **Category**: Meteorological pathways
- **Focus**: Temperature → Inversion → PBLH → PM2.5, Wind → Dispersion, etc.
- **Format**: Standard V2.0 (có bibliography + relationships)

### 2. chemical_processes.json
- **Category**: Chemical processes
- **Focus**: SO2/NO2 → SIA Formation, VOCs → SOA Formation, etc.
- **Format**: Standard V2.0

### 3. transport_mechanisms.json
- **Category**: Transport mechanisms
- **Focus**: Wind Direction → Transport, Back-trajectory, etc.
- **Format**: Có metadata, sources, relationships

### 4. emission_sources.json
- **Category**: Emission sources
- **Focus**: Traffic → NOx, Industry → SO2, Biomass Burning → PM2.5
- **Format**: Standard V2.0

### 5. static_factors.json
- **Category**: Static factors
- **Focus**: Population Density, LULC, Topography → PM2.5
- **Format**: Array format (cần normalize)

### 6. seasonal_patterns.json
- **Category**: Seasonal patterns
- **Focus**: Season → Weather Pattern, Diurnal Cycle → PBLH, etc.
- **Format**: Có prompt_id, causal_relationships

### 7. edge_cases.json
- **Category**: Edge cases and exceptions
- **Focus**: Non-linear relationships, Measurement artifacts, Exceptions
- **Format**: Standard V2.0

### 8. winter_chemistry_sia.json
- **Category**: Chemical processes (gap-focused)
- **Focus**: Winter SIA formation, NH4NO3 thermodynamics, SOA winter chemistry
- **Format**: Standard V2.0

### 9. precipitation_wet_scavenging.json
- **Category**: Meteorological pathways (gap-focused)
- **Focus**: Wet scavenging mechanisms, precipitation intensity effects, washout efficiency
- **Format**: Standard V2.0

### 10. synoptic_cold_surge_transport.json
- **Category**: Transport mechanisms (gap-focused)
- **Focus**: Cold surge patterns, synoptic-scale transport, regional pollution advection
- **Format**: Standard V2.0

### 11. wind_direction_upwind_exposure.json
- **Category**: Transport mechanisms (gap-focused)
- **Focus**: Wind sector analysis, upwind source exposure, directional transport patterns
- **Format**: Standard V2.0

### 12. static_moderators.json
- **Category**: Static factors (gap-focused)
- **Focus**: Static factors as moderators (LULC, topography, population density moderating effects)
- **Format**: Array format (cần normalize)

### 13. fog_visibility_artifacts.json
- **Category**: Edge cases (gap-focused)
- **Focus**: Fog/visibility measurement artifacts, hygroscopic growth effects
- **Format**: Standard V2.0

