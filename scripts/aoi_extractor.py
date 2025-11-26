#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd


def load_ecosystems(path: Path) -> gpd.GeoDataFrame:
    """Load the national ecosystem layer."""
    return gpd.read_file(path)


def get_text_columns(gdf: gpd.GeoDataFrame) -> list[str]:
    """Return columns that look text-like, to help the user pick a name field."""
    return [col for col in gdf.columns if gdf[col].dtype == object]


def filter_mangroves(
    gdf: gpd.GeoDataFrame,
    name_column: str,
    substring: str = "manglar",
) -> gpd.GeoDataFrame:
    """Filter rows whose name column contains the given substring (case-insensitive)."""
    if name_column not in gdf.columns:
        raise ValueError(
            f"Column {name_column!r} not found. Available columns: {list(gdf.columns)}"
        )

    series = gdf[name_column].astype("string")
    mask = series.str.contains(substring, case=False, na=False)
    mangroves = gdf.loc[mask].copy()
    return mangroves


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Extract mangrove polygons from the national ecosystem layer by "
            "filtering on a name column containing 'manglar'."
        )
    )
    parser.add_argument(
        "--ecosystems-path",
        type=Path,
        default=Path(
            "data/raw/Mapa_Ecosistemas_Continentales_Costeros_Marinos_100K_2024/SHAPE/"
            "e_eccmc_100K_2024.shp"
        ),
        help="Path to the national ecosystem layer (shapefile or similar)",
    )
    parser.add_argument(
        "--name-column",
        type=str,
        help=(
            "Attribute column that contains ecosystem names (e.g. 'NOMBRE'). If "
            "omitted, the script will list candidate text columns and exit."
        ),
    )
    parser.add_argument(
        "--substring",
        type=str,
        default="manglar",
        help="Substring to search for in the name column (default: 'manglar').",
    )
    parser.add_argument(
        "--group-column",
        type=str,
        default="nom_zh",
        help=(
            "Optional attribute column to use for grouped dissolves (for example, "
            "'nom_zh' for hydrographic zones). Set to an empty string to disable."
        ),
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("data/processed/mangroves_colombia_100k_2024.geojson"),
        help="Output path for the filtered mangrove layer (GeoJSON).",
    )

    args = parser.parse_args()

    ecosystems_path: Path = args.ecosystems_path
    name_column: str | None = args.name_column
    substring: str = args.substring
    group_column: str | None = args.group_column
    output_path: Path = args.output_path

    if not ecosystems_path.exists():
        raise SystemExit(f"Ecosystem layer not found at: {ecosystems_path}")

    gdf = load_ecosystems(ecosystems_path)

    if name_column is None:
        text_cols = get_text_columns(gdf)
        print("No --name-column provided. Text-like columns found:")
        for col in text_cols:
            print(f"  - {col}")
        raise SystemExit(
            "Please re-run specifying --name-column with the field holding "
            "ecosystem names."
        )

    mangroves = filter_mangroves(gdf, name_column=name_column, substring=substring)

    if mangroves.empty:
        print(
            "Warning: no features matched the mangrove filter. "
            "Check the name column and substring."
        )

    ensure_parent_dir(output_path)
    mangroves.to_file(output_path, driver="GeoJSON")
    print(f"Saved mangrove layer with {len(mangroves)} features to: {output_path}")

    if group_column:
        if group_column not in mangroves.columns:
            print(
                "Warning: group column "
                f"{group_column!r} not found in mangrove layer; skipping grouped AOIs."
            )
        else:
            grouped = mangroves.dissolve(by=group_column)
            grouped_path = output_path.with_name(
                output_path.stem + f"_by_{group_column}" + output_path.suffix
            )
            grouped.to_file(grouped_path, driver="GeoJSON")
            print(
                "Saved grouped mangrove AOIs by "
                f"{group_column!r} to: {grouped_path}"
            )

    # Also write a dissolved version as a single AOI geometry
    dissolved = mangroves.dissolve()
    dissolved_path = output_path.with_name(
        output_path.stem + "_dissolved" + output_path.suffix
    )
    dissolved.to_file(dissolved_path, driver="GeoJSON")
    print(
        "Saved dissolved mangrove AOI (single geometry) to: "
        f"{dissolved_path}"
    )


if __name__ == "__main__":
    main()
