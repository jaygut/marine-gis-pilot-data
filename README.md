# Marine GIS Pilot Data

### Blue Carbon Mangrove Assessment for Colombia

This repository provides **analysis-ready AOI geometries and metadata** for conducting preliminary blue carbon assessments of Colombia's mangrove ecosystems. It is structured for direct handoff to geospatial intelligence engineers at **Earthm.ai**.

**Total mangrove extent analyzed:** ~276,000 hectares across 12 hydrographic zones

---

## Start Here: Recommended First Actions

### For Earthm.ai Engineers

1. **Load the top 3 priority AOIs** for immediate analysis:
   ```
   data/processed/aois/col_patia_mangrove.geojson        (70,961 ha - Pacific flagship)
   data/processed/aois/col_bajo_magdalena_mangrove.geojson (45,839 ha - Caribbean flagship)
   data/processed/aois/col_sinu_mangrove.geojson         (8,748 ha - Cispatá/Vida Manglar)
   ```

2. **Review the metadata contract:**
   ```
   ai_docs/blue_carbon_aoi_metadata.csv
   ```

3. **See the priority ranking visualization:**
   ```
   data/processed/chart_priority_score.png
   data/processed/map_hydrographic_aois.png
   ```

### Why These Three First?

| AOI | Why Prioritize | Validation Value |
|-----|----------------|------------------|
| **Sinú (Cispatá)** | Overlaps existing VCS 2290 Vida Manglar project | Benchmark against known carbon project |
| **Bajo Magdalena** | Ciénaga Grande - INVEMAR's primary research site | Rich existing literature for validation |
| **Patía** | Largest intact Pacific complex (70,961 ha) | High AGB literature base; maximum carbon potential |

---

## Quick Reference: All Deliverables

| Deliverable | Location | What It Contains |
|-------------|----------|------------------|
| **Individual AOI GeoJSONs** | `data/processed/aois/` | 12 ready-to-ingest geometries |
| **AOI Metadata** | `ai_docs/blue_carbon_aoi_metadata.csv` | Provenance, filter logic, strategic notes |
| **Priority Metrics** | `data/processed/blue_carbon_candidates.csv` | Area, fragmentation, scores for all AOIs |
| **National Mangrove Map** | `data/processed/map_national_mangroves.png` | Overview visualization |
| **AOI Zone Map** | `data/processed/map_hydrographic_aois.png` | Colored by flagship status |
| **Area Chart** | `data/processed/chart_area_by_zone.png` | Bar chart by zone |
| **Priority Chart** | `data/processed/chart_priority_score.png` | Scores colored by status |
| **Full Notebook** | `notebooks/01_national_mangrove_backbone.ipynb` | Complete methodology |

---

## AOI File Schema

Each GeoJSON in `data/processed/aois/` contains these fields:

| Field | Type | Description |
|-------|------|-------------|
| `aoi_id` | string | Unique ID (e.g., `COL_SINU_MANGROVE`) |
| `aoi_name` | string | Human-readable name |
| `nom_zh` | string | Original hydrographic zone name |
| `source_layer` | string | Source shapefile reference |
| `area_ha` | float | Area in hectares (EPSG:3116) |
| `flagship_status` | string | `flagship` \| `emerging` \| `exploratory` |
| `priority_score` | float | 0.0–1.0 normalized priority |
| `geometry` | Polygon/MultiPolygon | CRS: EPSG:4686 (MAGNA-SIRGAS) |

### CRS Information

- **Stored CRS**: EPSG:4686 (MAGNA-SIRGAS geographic)
- **Area calculations**: Performed in EPSG:3116 (MAGNA-SIRGAS Colombia Bogota zone, equal-area)

---

## Complete AOI Inventory

### Flagship Sites (4 AOIs - 150,394 ha total)

High-confidence sites with existing literature, carbon projects, or institutional research presence.

| File | Zone | Area (ha) | Fragments | Priority | Strategic Context |
|------|------|-----------|-----------|----------|-------------------|
| `col_patia_mangrove.geojson` | Patía | 70,961 | 147 | 1.000 | Largest Pacific complex; extensive AGB studies; near Tumaco |
| `col_bajo_magdalena_mangrove.geojson` | Bajo Magdalena | 45,839 | 65 | 0.945 | Ciénaga Grande de Santa Marta; INVEMAR HQ; strong baseline data |
| `col_mira_mangrove.geojson` | Mira | 24,846 | 87 | 0.649 | Southern Pacific; transboundary with Ecuador; intact corridors |
| `col_sinu_mangrove.geojson` | Sinú | 8,748 | 10 | 0.422 | **Cispatá Bay / Vida Manglar VCS 2290**; most compact AOI |

### Emerging Sites (4 AOIs - 104,183 ha total)

Large extent with strategic importance but fewer formal blue carbon projects. High discovery potential.

| File | Zone | Area (ha) | Fragments | Priority | Strategic Context |
|------|------|-----------|-----------|----------|-------------------|
| `col_tapaje_dagua_directos_mangrove.geojson` | Tapaje-Dagua | 67,902 | 137 | 1.000 | Second-largest; underexplored; adjacent to Patía |
| `col_pacifico_directos_mangrove.geojson` | Pacífico-Directos | 17,285 | 52 | 0.392 | Central Pacific corridor; connects major basins |
| `col_san_juan_mangrove.geojson` | San Juán | 13,102 | 54 | 0.333 | Chocó bioregion; high biodiversity value |
| `col_atrato_darien_mangrove.geojson` | Atrato-Darién | 5,896 | 12 | 0.231 | Darién Gap; remote but potentially pristine |

### Exploratory Sites (4 AOIs - 21,852 ha total)

Smaller or less-documented zones for future discovery and expansion.

| File | Zone | Area (ha) | Fragments | Priority |
|------|------|-----------|-----------|----------|
| `col_baudo_directos_pacifico_mangrove.geojson` | Baudó | 11,719 | 34 | 0.164 |
| `col_caribe_litoral_mangrove.geojson` | Caribe-Litoral | 7,992 | 31 | 0.111 |
| `col_caribe_guajira_mangrove.geojson` | Caribe-Guajira | 2,004 | 20 | 0.026 |
| `col_islas_caribe_mangrove.geojson` | Islas Caribe | 137 | 1 | 0.000 |

---

## Analytical Expectations for Earthm.ai

### Per-AOI Deliverables (Priority Order)

1. **Baseline mangrove extent** (2000, 2010, 2020, 2024)
2. **Change detection** - net loss/gain and annual rates
3. **Disturbance hotspots** - canopy loss, conversion to aquaculture/agriculture
4. **Zonation mapping** - fringe vs basin vs riverine mangroves
5. **Priority sub-polygons** - areas for field investigation or project design

### Cross-AOI Comparison

- Rank all 12 AOIs by: total area, recent loss rate, restoration potential
- Identify: high-integrity blocks vs degraded areas suitable for restoration
- Flag: AOIs with anomalous change patterns warranting deeper investigation

### Suggested Temporal Windows

| Analysis | Period | Rationale |
|----------|--------|-----------|
| Long-term baseline | 2000–2024 | Full Landsat archive; captures major policy changes |
| Recent change | 2015–2024 | Post-Paris Agreement; recent conservation efforts |
| Validation period | 2010–2020 | Overlap with Vida Manglar project timeline |

---

## Data Provenance

### Source Data

- **National Ecosystem Map (1:100k, 2024)**
  - Publisher: IDEAM / SINCHI / IAvH / INVEMAR
  - Location: `data/raw/Mapa_Ecosistemas_Continentales_Costeros_Marinos_100K_2024/`
  - Shapefile: `SHAPE/e_eccmc_100K_2024.shp`

### Filter Logic

```
WHERE u_sintesis ILIKE '%manglar%'
```

All polygons whose ecosystem synthesis description (`u_sintesis`) contains the substring "manglar" (case-insensitive) are classified as mangrove-dominated ecosystems.

### Grouping Logic

AOIs partitioned by the `nom_zh` attribute (hydrographic zone name), providing **hydrologically coherent units** aligned with watershed boundaries. This enables:
- Consistent upstream/downstream analysis
- Alignment with Colombian water management units
- Meaningful aggregation for national reporting

---

## Repository Structure

```
marine-gis-pilot-data/
├── README.md                              # This file
├── CLAUDE.md                              # AI assistant guidance
├── requirements.txt                       # Python dependencies
│
├── data/
│   ├── raw/                               # Source data (not in repo)
│   │
│   └── processed/
│       ├── aois/                          # ← START HERE: 12 AOI GeoJSONs
│       │   ├── col_patia_mangrove.geojson
│       │   ├── col_bajo_magdalena_mangrove.geojson
│       │   ├── col_sinu_mangrove.geojson
│       │   └── ... (9 more)
│       │
│       ├── blue_carbon_candidates.csv     # Priority metrics table
│       ├── mangroves_colombia_100k_2024.geojson
│       ├── mangroves_colombia_100k_2024_dissolved.geojson
│       ├── mangroves_colombia_100k_2024_by_nom_zh.geojson
│       │
│       └── [visualizations]
│           ├── map_national_mangroves.png
│           ├── map_hydrographic_aois.png
│           ├── chart_area_by_zone.png
│           └── chart_priority_score.png
│
├── notebooks/
│   └── 01_national_mangrove_backbone.ipynb  # Full analysis methodology
│
├── scripts/
│   └── aoi_extractor.py                   # AOI extraction script
│
└── ai_docs/
    ├── blue_carbon_aoi_metadata.csv       # ← METADATA CONTRACT
    ├── blue_carbon_strategy.md            # Strategic workflow
    └── external_agents_prompt.md          # Agent instructions
```

---

## Key Metrics Summary

| Metric | Value |
|--------|-------|
| Total AOIs | 12 |
| Total mangrove area | 276,429 ha |
| Flagship AOIs | 4 (150,394 ha) |
| Emerging AOIs | 4 (104,183 ha) |
| Exploratory AOIs | 4 (21,852 ha) |
| Largest AOI | Patía (70,961 ha) |
| Most compact AOI | Sinú (10 fragments) |
| Most fragmented AOI | Patía (147 fragments) |

---

## Development Setup

### Clone and Install

```bash
git clone https://github.com/jaygut/marine-gis-pilot-data
cd marine-gis-pilot-data
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Re-run Analysis

```bash
# Extract AOIs from raw ecosystem map
python scripts/aoi_extractor.py --name-column u_sintesis

# Run full analysis notebook
jupyter notebook notebooks/01_national_mangrove_backbone.ipynb
```

---

## Key Focus Areas

### Cispatá Bay (Caribbean Coast)
- **AOI**: `col_sinu_mangrove.geojson`
- **Goal**: Validate against Vida Manglar carbon project (VCS ID 2290)
- **Status**: Hydrographic zone boundary provided; authoritative project AOI from INVEMAR pending
- **Centroid**: 9.39°N, 75.87°W

### Pacific Coast Mangroves
- **AOIs**: Patía, Mira, Tapaje-Dagua, San Juán, Baudó
- **Goal**: Prioritize high-integrity sites for new blue carbon projects
- **Status**: Patía and Tapaje-Dagua identified as top priorities by area and potential

### Ciénaga Grande (Caribbean Coast)
- **AOI**: `col_bajo_magdalena_mangrove.geojson`
- **Goal**: Leverage INVEMAR's extensive research baseline
- **Status**: Second-largest AOI; strong existing data for validation
- **Centroid**: 10.66°N, 74.79°W

---

## Contact

For questions about this repository or the blue carbon assessment workflow, contact the project maintainers.
