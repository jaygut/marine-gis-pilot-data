# Strategy for Mapping High-Potential Blue Carbon Mangrove Ecosystems in Colombia

This document outlines how to leverage the current contents of this repo to systematically identify, visualize, and prioritize promising blue carbon mangrove ecosystems in Colombia, and how to prepare inputs for advanced analytics on the Earthm.ai platform.

---

## 1. Strategic Objectives

- **Build a national blue carbon backbone**
  - Use the 1:100k ecosystem map (2024) to define a *consistent, national* mangrove mask.
  - Partition this mask into hydrologically coherent AOIs that are meaningful for carbon and risk assessments.

- **Highlight both flagship and emerging blue carbon sites**
  - Flag **well-established** regions (e.g., Cispatá / Vida Manglar, Pacific complexes around Tumaco/Sanquianga, Ciénaga Grande) as reference AOIs.
  - Surface **promising, under-characterised corridors** where deeper geospatial analysis could reveal new blue carbon opportunities.

- **Create a clear handoff to geospatial intelligence engineers**
  - Provide clean, self-contained AOI geometries and metadata they can ingest into Earthm.ai.
  - Define what success looks like for a “first round” blue carbon assessment.

---

## 2. Data Assets We Have Now

From the 1:100k ecosystem map (2024) and the `aoi_extractor.py` script, we now have:

- **Raw ecosystem map**
  - Path: `data/raw/Mapa_Ecosistemas_Continentales_Costeros_Marinos_100K_2024/SHAPE/e_eccmc_100K_2024.shp`
  - Key attributes (among many):
    - `u_sintesis` – synthesis description of ecosystem units.
    - `nom_zh` – hydrographic unit name.

- **Derived mangrove products (in `data/processed/`)**
  - `mangroves_colombia_100k_2024.geojson`
    - All polygons whose `u_sintesis` contains "manglar" (case-insensitive).
  - `mangroves_colombia_100k_2024_dissolved.geojson`
    - Single, dissolved geometry representing **national mangrove extent** (blue carbon envelope).
  - `mangroves_colombia_100k_2024_by_nom_zh.geojson`
    - One feature per `nom_zh` (e.g., **Patía**, **Mira**, **Sinú**, **Bajo Magdalena**, **Caribe - Litoral**, **Islas Caribe**), each representing a hydrologically coherent mangrove AOI.

These layers are the **starting canvas** for prioritizing where Earthm.ai should focus deeper analysis.

---

## 3. Proposed Showcase Notebook

Create a Jupyter notebook (e.g., `notebooks/01_national_mangrove_backbone.ipynb`) that does three things:

### 3.1. Load & Inspect AOIs

- Load:
  - `mangroves_colombia_100k_2024.geojson`
  - `mangroves_colombia_100k_2024_dissolved.geojson`
  - `mangroves_colombia_100k_2024_by_nom_zh.geojson`
- Print:
  - CRS information.
  - Number of features per dataset.
  - Example rows of `nom_zh`, `u_sintesis`.

**Purpose:** make the structure fully transparent to both you and engineers.

### 3.2. Compute Strategic Summary Metrics

For each `nom_zh` AOI (row in `_by_nom_zh`):

- **Area metrics** (in hectares):
  - Reproject to an equal-area CRS suitable for Colombia (e.g., `EPSG:3116` – MAGNA-SIRGAS / Colombia Bogota zone, or another nationally recommended equal-area system).
  - Compute mangrove area per `nom_zh`.

- **Compactness / shape complexity (optional first proxy)**
  - Simple proxies: perimeter-to-area ratio, number of disjoint parts.
  - Helps distinguish compact, intact blocks from highly fragmented shorelines.

- **Proximity to known blue carbon sites**
  - Tag known flagship regions:
    - `Sinú` → Cispatá / Vida Manglar region.
    - `Bajo Magdalena` → Ciénaga Grande.
    - `Patía`, `Mira`, `Pacífico - Directos`, `San Juán`, `Baudó - Directos Pacífico` → Pacific mangrove complexes.
  - Add a categorical field like `flagship_status` with values such as `"flagship"`, `"emerging"`, `"exploratory"`.

- **Result:** a table like `blue_carbon_candidates.csv` summarizing, per `nom_zh`:
  - `nom_zh`
  - `area_ha`
  - `flagship_status`
  - simple fragmentation metrics (optional)
  - an initial **priority score** (can be simple: e.g., area rank + flagship bonus).

### 3.3. Strategic Visuals

Create visuals that are both **analytically useful** and **story-ready**:

- **National overview map**
  - Plot `mangroves_colombia_100k_2024_dissolved.geojson` on a light basemap.
  - Optionally overlay country boundary and major rivers.
  - Use `geopandas` + `contextily` (or `folium` for interactive web maps).

- **Hydrographic-zone AOI map**
  - Plot `mangroves_colombia_100k_2024_by_nom_zh.geojson` with a categorical colormap by `nom_zh`.
  - Label or annotate key zones: **Sinú**, **Bajo Magdalena**, **Patía**, **Mira**, **Caribe - Litoral**, **Islas Caribe**.
  - Add a legend explaining how colors link to AOI IDs in your analytics tables.

- **Priority ranking visual**
  - Bar chart: `area_ha` per `nom_zh`, colored by `flagship_status` or priority tier.
  - Highlight top 3–5 AOIs you want Earthm.ai to focus on first.

- **Outputs to save from the notebook**
  - `data/processed/blue_carbon_candidates.csv`
  - Selected AOI subsets for top candidates, e.g.:
    - `data/processed/aoi_sinu_cispata.geojson`
    - `data/processed/aoi_bajo_magdalena_cienaga_grande.geojson`
    - `data/processed/aoi_patia_pacific_complex.geojson`

These outputs become your **handoff artifacts** for Earthm.ai.

---

## 4. Information to Share with Geospatial Intelligence Engineers

To enable advanced analytics on Earthm.ai (or similar platforms), prepare and share:

### 4.1. Geometry Files

For each priority AOI (e.g. `Sinú / Cispatá`, `Bajo Magdalena / Ciénaga Grande`, a combined `Patía + Mira` Pacific AOI):

- **GeoJSON or GeoPackage** with:
  - Field `aoi_id` (unique short ID, e.g., `COL_SINU_MANGROVE`).
  - Field `aoi_name` (human-readable, e.g., `Sinú – Cispatá Mangroves`).
  - Field `nom_zh` (original hydrographic unit name).
  - Field `source_layer` (e.g., `e_eccmc_100K_2024.shp` / 1:100k 2024 ecosystem map).

- **CRS information**
  - Explicitly state original CRS from the shapefile (from `.prj`) and any reprojection used for area calculations.

### 4.2. Tabular Metadata & Context

Provide a concise table (e.g. `ai_docs/blue_carbon_aoi_metadata.csv`) containing, for each selected AOI:

- `aoi_id`
- `aoi_name`
- `nom_zh`
- `area_ha` (in an equal-area CRS)
- `flagship_status` (`flagship`, `emerging`, `exploratory`)
- `data_source` (1:100k ecosystem map 2024 + path)
- `filter_logic` (e.g., `u_sintesis` contains "manglar")
- `notes` (e.g., "Overlaps Vida Manglar VCS 2290 AOI" or "Pacific complex with strong AGB literature base").

This allows engineers to:

- Validate that they’re loading the **correct geometries**.
- Understand **why** each AOI is strategically important.
- Track provenance and assumptions in any downstream modeling.

### 4.3. Analytical Expectations for Earthm.ai

Clearly state what you want from the first analytics pass, for example:

- **For each AOI**:
  - Baseline mangrove extent and change over the last N years (e.g., 2000–2024).
  - Disturbance / degradation hotspots (e.g., canopy loss near edges, conversion to aquaculture/agriculture).
  - Zonation: potential differentiation between fringe vs. interior mangroves, distance to channels, salinity proxies where available.
  - Priority sub-polygons for further field investigation or project design.

- **Cross-AOI comparison**:
  - Ranking of AOIs by:
    - Total mangrove area.
    - Recent loss rate.
    - Potential for additional conservation/restoration (e.g., high remaining area + moderate pressure).

Documenting these expectations helps your engineers configure Earthm.ai pipelines (e.g., dataset choices, temporal ranges, model types) without guesswork.

---

## 5. Selecting the Most Promising Blue Carbon AOIs (First Round)

Using the notebook outputs and AOI metadata, you can define a **first cohort** of sites for deep analysis:

1. **Flagship validation AOIs**
   - `Sinú` (Cispatá / Vida Manglar region).
   - `Bajo Magdalena` (Ciénaga Grande).
   - One or two Pacific basins (e.g., `Patía`, `Mira` or `Pacífico - Directos`).

   *Goal:* Demonstrate that your pipeline reproduces and extends what is already known in the literature and project community.

2. **Emerging opportunity AOIs**
   - Smaller or less-studied `nom_zh` units with substantial mangrove area but fewer published blue carbon projects.

   *Goal:* Use Earthm.ai to uncover **new high-potential blue carbon opportunities** (e.g., stable but under-protected mangrove blocks, regions with recent degradation but high restoration potential).

3. **Iterate with experts**
   - Review first-round analytics results with senior mangrove and carbon experts.
   - Refine AOI definitions and add/remove candidates for the next iteration.

---

## 6. How to Proceed Next

1. **Create the showcase notebook** (as described in Section 3) using the existing processed layers.
2. **Export AOI geometries and metadata** (Section 4) into a clearly named folder structure, for example:
   - `data/processed/aois/` – AOI GeoJSON/GeoPackage files.
   - `ai_docs/blue_carbon_aoi_metadata.csv` – tabular description.
3. **Share with geospatial engineers**:
   - Provide:
     - The AOI files.
     - The metadata CSV.
     - The rendered notebook (HTML or PDF) so they can see maps and priority rationale.
4. **Coordinate Earthm.ai runs**:
   - Agree with engineers on:
     - Temporal window (e.g., 2000–2024).
     - Core indicators to compute.
     - Delivery format for outputs (rasters, vector summaries, dashboards).
5. **Feed results back into this repo**:
   - Store summary outputs under `data/processed/` (e.g., `data/processed/earthm/` subfolder).
   - Extend this `ai_docs` folder with short memos interpreting each new round of analytics.

Following this guideline, you can move from a national ecosystem map to a **sharply defined, analytics-ready portfolio of blue carbon mangrove AOIs**, and give your geospatial intelligence engineers everything they need to deliver a compelling first assessment using Earthm.ai.
