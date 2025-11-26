# Prompt for External Agents: Marine GIS Blue-Carbon AOI Preparation

You are an external geospatial / data science team (or AI agent) supporting the **marine-gis-pilot-data** repository. Your primary goal is to implement, refine, and operationalize the strategy described in:

- `ai_docs/blue_carbon_strategy.md`

so that the engineering team at **Earthm.ai** can run a **high-quality first blue-carbon assessment focused on mangrove ecosystems in Colombia**.

Follow the instructions below carefully.

---

## 0. Before Doing Anything: Understand the Codebase and Context

1. **Repository**
   - Git URL (public):
     - `https://github.com/jaygut/marine-gis-pilot-data`

2. **Read these files in full before making changes**
   - `README.md`
     - Overall project context, focus regions, data structure, and current AOI extraction workflow.
   - `ai_docs/blue_carbon_strategy.md`
     - Canonical strategy document. Explains how the national ecosystem map, mangrove extraction, and hydrographic AOIs fit together as a blue-carbon backbone.
   - `scripts/aoi_extractor.py`
     - Script that extracts mangrove polygons based on `u_sintesis` containing "manglar" and produces:
       - National mangrove polygons.
       - National dissolved AOI.
       - Mangrove AOIs grouped by `nom_zh` (hydrographic zones).
   - `requirements.txt`
     - Python GIS/analytics stack (geopandas, shapely, rasterio, etc.).

3. **Understand the current data layout**
   - `data/raw/`
     - Contains large, authoritative input layers (e.g., national ecosystem map at 1:100k for 2024). These are **not meant to be versioned further** or modified.
   - `data/processed/`
     - Contains **derived AOIs and analysis-ready layers**, including:
       - `mangroves_colombia_100k_2024.geojson`
       - `mangroves_colombia_100k_2024_dissolved.geojson`
       - `mangroves_colombia_100k_2024_by_nom_zh.geojson`

4. **Clarify any ambiguities _before_ implementation**
   - If anything in the docs appears inconsistent or underspecified, propose a clarification and explicit assumption before proceeding.

Your work must **respect and extend** this existing structure, not replace or ignore it.

---

## 1. Environment and Tooling

1. **Use the existing Python environment setup**
   - Recommended:
     ```bash
     uv venv .venv
     source .venv/bin/activate
     uv pip install -r requirements.txt
     ```

2. **Do not commit large raw inputs**
   - Respect `.gitignore`:
     - `data/raw/` and other large or sensitive data **must not** be version-controlled.
   - Only commit:
     - Code (scripts, notebooks).
     - Lightweight processed outputs (small GeoJSON/GPKG, CSV).
     - Documentation under `ai_docs/`.

3. **Coding principles**
   - Prefer small, composable functions over monolithic scripts.
   - Keep file paths relative to the repo root.
   - Clearly distinguish **raw inputs** (`data/raw`) from **processed artifacts** (`data/processed`).

---

## 2. Implement the Showcase Notebook (National Mangrove Backbone)

Create a Jupyter notebook (e.g., `notebooks/01_national_mangrove_backbone.ipynb`) that operationalizes the strategy in `ai_docs/blue_carbon_strategy.md`.

### 2.1. Load and Inspect

- Load, using `geopandas`:
  - `data/processed/mangroves_colombia_100k_2024.geojson`
  - `data/processed/mangroves_colombia_100k_2024_dissolved.geojson`
  - `data/processed/mangroves_colombia_100k_2024_by_nom_zh.geojson`

- For each layer, show:
  - CRS and basic metadata.
  - Number of features.
  - Example attribute rows, especially `u_sintesis` and `nom_zh`.

### 2.2. Compute Strategic Metrics per Hydrographic AOI

For each feature in `mangroves_colombia_100k_2024_by_nom_zh.geojson` (one per `nom_zh`):

- **Area metrics (in hectares)**
  - Reproject to a suitable equal-area CRS for Colombia (e.g., `EPSG:3116` or another documented equal-area CRS) for area computation.
  - Compute total mangrove area per `nom_zh`.

- **Optional shape/fragmentation proxies**
  - For each AOI, compute simple metrics such as perimeter, area, and perimeter/area ratio as a crude fragmentation/compactness proxy.

- **Flagship / emerging / exploratory categorization**
  - Add a column, e.g., `flagship_status` with values:
    - `flagship` – e.g., `Sinú` (Cispatá / Vida Manglar region), `Bajo Magdalena` (Ciénaga Grande), selected Pacific basins.
    - `emerging` – large or strategically located mangrove basins with known importance but fewer formal blue carbon projects.
    - `exploratory` – smaller or less-documented units that may yield new opportunities with further analysis.

- **Priority score (first-pass heuristic)**
  - Implement a simple scoring function (describe it clearly in the notebook), for example:
    - Normalize area (0–1).
    - Add bonus for `flagship` status.
    - Optionally adjust for fragmentation proxy.
  - Store this as a numeric `priority_score` field.

- **Export summary table**
  - Save a CSV file summarizing AOI-level metrics and labels, e.g.:
    - `data/processed/blue_carbon_candidates.csv`

### 2.3. Create Strategic Visuals

In the same notebook, create visuals that are both analytically useful and presentation-ready:

- **National overview map**
  - Plot the dissolved national mangrove AOI on a simple basemap.
  - Use `geopandas` for geometry + `contextily` or similar for tiles (if appropriate).

- **Hydrographic AOI map**
  - Plot the `_by_nom_zh` layer, colored uniquely by `nom_zh`.
  - Label or annotate key basins: `Sinú`, `Bajo Magdalena`, `Patía`, `Mira`, `Caribe - Litoral`, `Islas Caribe`, etc.

- **Priority ranking chart**
  - Bar chart or ordered plot of `area_ha` or `priority_score` per `nom_zh`, colored by `flagship_status`.

Ensure the notebook can be run end-to-end from a clean checkout (after installing dependencies) without manual tweaks.

---

## 3. Prepare AOIs and Metadata for Earthm.ai

Your deliverable must enable the Earthm.ai engineers to ingest AOIs and metadata without guessing. Follow the structure described in `ai_docs/blue_carbon_strategy.md`.

### 3.1. Geometry Exports

For each selected **priority AOI** (both flagship and emerging), export a clean geometry file:

- Format: **GeoJSON** or **GeoPackage**.
- Suggested output folder:
  - `data/processed/aois/`

Each AOI file should contain:

- `aoi_id` – short unique ID (e.g., `COL_SINU_MANGROVE`, `COL_BAJO_MAG_MANGROVE`).
- `aoi_name` – readable name (e.g., `Sinú – Cispatá Mangroves`).
- `nom_zh` – original hydrographic unit name.
- `source_layer` – reference to the original dataset (e.g., `e_eccmc_100K_2024.shp`).
- CRS information (stored with the geometry dataset; note any reprojections used).

### 3.2. Metadata Table

Create a metadata CSV, e.g. `ai_docs/blue_carbon_aoi_metadata.csv`, containing for each AOI:

- `aoi_id`
- `aoi_name`
- `nom_zh`
- `area_ha`
- `flagship_status` (`flagship`, `emerging`, `exploratory`)
- `priority_score`
- `data_source` (1:100k ecosystem map 2024; full path under `data/raw/`)
- `filter_logic` (e.g., `u_sintesis` contains "manglar", case-insensitive)
- `notes` (e.g., overlaps Vida Manglar AOI, proximate to Ciénaga Grande, etc.).

This metadata table is the **contract** between this repo and Earthm.ai-based analytics.

### 3.3. Analytical Expectations (for Earthm.ai)

In `ai_docs/`, add or update documentation clarifying what is expected from the first Earthm.ai runs, for example:

- **Per AOI**:
  - Baseline mangrove extent and time-series change over a clearly specified period (e.g., 2000–2024).
  - Disturbance and degradation hotspots.
  - Zonation within AOIs (e.g., fringe vs interior mangroves, distance to channels, potential salinity gradients if available).

- **Across AOIs**:
  - A ranking or clustering of AOIs by area, change, and opportunity (e.g., conservation vs restoration potential).

You should not implement Earthm.ai internals here; instead, specify **inputs and outputs** clearly for the Earthm.ai team.

---

## 4. Deliverables Checklist

At minimum, your work should produce:

1. **Notebook**
   - `notebooks/01_national_mangrove_backbone.ipynb`
   - Runs end-to-end, generates metrics and visuals, and saves summary artifacts.

2. **Summary table**
   - `data/processed/blue_carbon_candidates.csv` with metrics per `nom_zh`.

3. **AOI geometries**
   - One file per high-priority AOI in `data/processed/aois/` (GeoJSON or GPKG), with core fields as specified above.

4. **AOI metadata**
   - `ai_docs/blue_carbon_aoi_metadata.csv`

5. **Detailed summary report**
   - A written report (Markdown in `ai_docs/`, and optionally rendered to PDF/HTML) that:
     - Summarizes the AOIs, metrics, and visuals you produced.
     - Explains the prioritization logic (how `flagship_status` and `priority_score` were defined and used).
     - Clearly positions the generated AOIs, tables, and notebook as the **baseline starting point** for blue-carbon geospatial analytics to be run on Earthm.ai.

6. **Updated documentation (if needed)**
   - If you adjust or refine the strategy, update `ai_docs/blue_carbon_strategy.md` or add an additional memo in `ai_docs/` describing what changed and why.

---

## 5. Quality and Review

- Ensure all paths are relative to the repo root.
- Ensure your notebook and scripts are reproducible from a clean clone with the documented environment.
- Before handoff, re-run the main notebook from top to bottom and verify:
  - No errors.
  - All expected outputs are created.
  - Maps and charts are legible and clearly labeled.

Your ultimate goal is to hand the Earthm.ai engineering team a **coherent, well-documented set of AOIs, metrics, and visuals** so they can focus on high-value blue-carbon analytics rather than data wrangling.
