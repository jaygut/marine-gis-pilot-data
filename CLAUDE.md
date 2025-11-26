# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blue carbon mangrove assessment for Colombia. This repository provides analysis-ready AOI geometries and metadata for Earthm.ai engineers to conduct preliminary blue carbon assessments. Focus areas: Cispatá Bay (Caribbean) and Pacific Coast mangrove complexes.

## Key Commands

### Environment Setup
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### AOI Extraction (from raw ecosystem map)
```bash
python scripts/aoi_extractor.py --name-column u_sintesis
```

### Run Analysis Notebook
```bash
jupyter notebook notebooks/01_national_mangrove_backbone.ipynb
```

## Architecture

### Data Flow
```
Raw Ecosystem Map (1:100k 2024)
    ↓ filter: u_sintesis contains "manglar"
National Mangrove Polygons
    ↓ dissolve by nom_zh (hydrographic zone)
Hydrographic AOIs (12 zones)
    ↓ compute metrics + assign priority
Individual AOI GeoJSONs + Metadata CSVs
```

### Key Outputs

| File | Purpose |
|------|---------|
| `data/processed/aois/*.geojson` | Individual AOI geometries for Earthm.ai ingestion |
| `ai_docs/blue_carbon_aoi_metadata.csv` | Full provenance and context per AOI |
| `data/processed/blue_carbon_candidates.csv` | Priority metrics table |
| `notebooks/01_national_mangrove_backbone.ipynb` | Full methodology with visualizations |

### AOI GeoJSON Schema
```
aoi_id          → COL_SINU_MANGROVE, COL_PATIA_MANGROVE, etc.
aoi_name        → Human-readable name
nom_zh          → Hydrographic zone from source data
source_layer    → e_eccmc_100K_2024.shp
area_ha         → Area in hectares (computed in EPSG:3116)
flagship_status → flagship | emerging | exploratory
priority_score  → 0.0–1.0
geometry        → CRS EPSG:4686 (MAGNA-SIRGAS)
```

### Priority Classification

**Flagship** (validated blue carbon sites):
- `Sinú` → Cispatá / Vida Manglar VCS 2290
- `Bajo Magdalena` → Ciénaga Grande de Santa Marta
- `Patía`, `Mira` → Pacific complexes with AGB literature

**Emerging** (high potential, fewer projects):
- `Tapaje-Dagua-Directos`, `Pacífico-Directos`, `San Juán`, `Atrato-Darién`

**Exploratory** (discovery candidates):
- `Baudó`, `Caribe-Litoral`, `Caribe-Guajira`, `Islas Caribe`

## GIS Conventions

- **Storage CRS**: EPSG:4686 (MAGNA-SIRGAS geographic)
- **Area calculations**: EPSG:3116 (MAGNA-SIRGAS Colombia Bogota zone, equal-area)
- **Output format**: GeoJSON for portability
- **Filter logic**: `u_sintesis` contains "manglar" (case-insensitive)
- **Grouping**: `nom_zh` attribute (hydrographic zones)

## Key Attributes in Source Data

| Attribute | Description | Usage |
|-----------|-------------|-------|
| `u_sintesis` | Ecosystem synthesis description | Mangrove filtering |
| `nom_zh` | Hydrographic zone name | AOI partitioning |

## Documentation

- `ai_docs/blue_carbon_strategy.md` → Strategic workflow for AOI identification
- `ai_docs/external_agents_prompt.md` → Instructions for implementing the workflow
- `ai_docs/blue_carbon_aoi_metadata.csv` → AOI provenance and handoff metadata

## Earthm.ai Integration

The `data/processed/aois/` directory contains 12 GeoJSON files ready for ingestion. Each file is self-contained with all metadata embedded. The `ai_docs/blue_carbon_aoi_metadata.csv` provides the contract for understanding filter logic, data sources, and analytical context.

Expected Earthm.ai outputs per AOI:
1. Baseline extent and change (2000–2024)
2. Disturbance/degradation hotspots
3. Zonation (fringe vs interior)
4. Priority sub-polygons for field work
