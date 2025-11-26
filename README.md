# Marine GIS Pilot Data

### Blue Carbon Mangrove Assessment for Colombia

This repository provides **analysis-ready AOI geometries and metadata** for conducting preliminary blue carbon assessments of Colombia's mangrove ecosystems. It is structured for direct handoff to geospatial intelligence engineers at **Earthm.ai**.

---

## Quick Start for Earthm.ai Engineers

### What You Need

| Deliverable | Location | Description |
|-------------|----------|-------------|
| **Individual AOI GeoJSONs** | `data/processed/aois/` | 12 priority AOIs with standardized schema |
| **AOI Metadata** | `ai_docs/blue_carbon_aoi_metadata.csv` | Full provenance, filter logic, and context |
| **Priority Rankings** | `data/processed/blue_carbon_candidates.csv` | Metrics and scores for all AOIs |
| **Analysis Notebook** | `notebooks/01_national_mangrove_backbone.ipynb` | Full methodology and visualizations |

### AOI File Schema

Each GeoJSON in `data/processed/aois/` contains:

```
aoi_id          → Unique identifier (e.g., COL_SINU_MANGROVE)
aoi_name        → Human-readable name
nom_zh          → Original hydrographic zone name
source_layer    → Source shapefile reference
area_ha         → Area in hectares (EPSG:3116)
flagship_status → flagship | emerging | exploratory
priority_score  → 0.0–1.0 normalized priority
geometry        → Polygon/MultiPolygon (EPSG:4686)
```

### CRS Information

- **Stored CRS**: EPSG:4686 (MAGNA-SIRGAS geographic)
- **Area calculations**: Performed in EPSG:3116 (MAGNA-SIRGAS Colombia Bogota zone, equal-area)

---

## Priority AOIs for First Assessment

### Flagship Sites (Recommended First Round)

| AOI ID | Zone | Area (ha) | Priority | Notes |
|--------|------|-----------|----------|-------|
| `COL_SINU_MANGROVE` | Sinú | 8,748 | 0.422 | Overlaps Vida Manglar VCS 2290; Cispatá Bay |
| `COL_BAJO_MAGDALENA_MANGROVE` | Bajo Magdalena | 45,839 | 0.945 | Ciénaga Grande de Santa Marta; INVEMAR research area |
| `COL_PATIA_MANGROVE` | Patía | 70,961 | 1.000 | Pacific coast complex; high AGB literature base |
| `COL_MIRA_MANGROVE` | Mira | 24,846 | 0.649 | Southern Pacific; near Ecuador border |

### Emerging Sites (High Potential)

| AOI ID | Zone | Area (ha) | Priority | Notes |
|--------|------|-----------|----------|-------|
| `COL_TAPAJE_DAGUA_DIRECTOS_MANGROVE` | Tapaje-Dagua | 67,902 | 1.000 | Large extent; fewer formal carbon projects |
| `COL_PACIFICO_DIRECTOS_MANGROVE` | Pacífico-Directos | 17,285 | 0.392 | Strategic Pacific corridor |
| `COL_SAN_JUAN_MANGROVE` | San Juán | 13,102 | 0.333 | Pacific basin with restoration potential |
| `COL_ATRATO_DARIEN_MANGROVE` | Atrato-Darién | 5,896 | 0.231 | Darien Gap region |

### Exploratory Sites

| AOI ID | Zone | Area (ha) | Priority |
|--------|------|-----------|----------|
| `COL_BAUDO_DIRECTOS_PACIFICO_MANGROVE` | Baudó | 11,719 | 0.164 |
| `COL_CARIBE_LITORAL_MANGROVE` | Caribe-Litoral | 7,992 | 0.111 |
| `COL_CARIBE_GUAJIRA_MANGROVE` | Caribe-Guajira | 2,004 | 0.026 |
| `COL_ISLAS_CARIBE_MANGROVE` | Islas Caribe | 137 | 0.000 |

---

## Analytical Expectations

### Per-AOI Analysis

For each AOI, we expect Earthm.ai to compute:

1. **Baseline mangrove extent** and time-series change (2000–2024)
2. **Disturbance/degradation hotspots** (canopy loss, conversion to aquaculture/agriculture)
3. **Zonation** (fringe vs interior mangroves, distance to channels)
4. **Priority sub-polygons** for field investigation or project design

### Cross-AOI Comparison

- Ranking by total area, recent loss rate, and conservation/restoration potential
- Identification of high-integrity blocks vs degraded areas suitable for restoration

---

## Data Provenance

### Source Data

- **National Ecosystem Map (1:100k, 2024)**
  - Location: `data/raw/Mapa_Ecosistemas_Continentales_Costeros_Marinos_100K_2024/`
  - Shapefile: `SHAPE/e_eccmc_100K_2024.shp`

### Filter Logic

All mangrove polygons extracted where:
```
u_sintesis CONTAINS 'manglar' (case-insensitive)
```

### Grouping

AOIs partitioned by hydrographic zone using the `nom_zh` attribute, providing hydrologically coherent units aligned with watershed boundaries.

---

## Repository Structure

```
marine-gis-pilot-data/
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant guidance
├── requirements.txt             # Python dependencies
│
├── data/
│   ├── raw/                     # Original source data (not version-controlled)
│   │   └── Mapa_Ecosistemas_.../
│   │
│   └── processed/               # Analysis-ready outputs
│       ├── aois/                         # Individual AOI GeoJSONs (12 files)
│       ├── blue_carbon_candidates.csv    # Priority metrics table
│       ├── mangroves_colombia_100k_2024.geojson
│       ├── mangroves_colombia_100k_2024_dissolved.geojson
│       ├── mangroves_colombia_100k_2024_by_nom_zh.geojson
│       ├── map_national_mangroves.png
│       ├── map_hydrographic_aois.png
│       ├── chart_area_by_zone.png
│       └── chart_priority_score.png
│
├── notebooks/
│   └── 01_national_mangrove_backbone.ipynb  # Full analysis notebook
│
├── scripts/
│   └── aoi_extractor.py         # AOI extraction script
│
└── ai_docs/
    ├── blue_carbon_strategy.md          # Strategic workflow
    ├── external_agents_prompt.md        # Agent instructions
    └── blue_carbon_aoi_metadata.csv     # Full AOI metadata
```

---

## Getting Started (Development)

### Clone and Setup

```bash
git clone https://github.com/jaygut/marine-gis-pilot-data
cd marine-gis-pilot-data
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Re-run AOI Extraction

```bash
python scripts/aoi_extractor.py --name-column u_sintesis
```

### Run Analysis Notebook

```bash
jupyter notebook notebooks/01_national_mangrove_backbone.ipynb
```

---

## Key Focus Areas

### Cispatá Bay (Caribbean Coast)
- **Goal**: Validate AOI against Vida Manglar carbon project (VCS ID 2290)
- **Status**: `COL_SINU_MANGROVE` provides the hydrographic zone boundary; authoritative project AOI from INVEMAR pending

### Pacific Coast Mangroves
- **Goal**: Prioritize high-integrity sites for new blue carbon projects
- **Status**: Patía, Mira, Tapaje-Dagua complexes identified as top priorities

---

## Contact

For questions about this repository or the blue carbon assessment workflow, contact the project maintainers.
