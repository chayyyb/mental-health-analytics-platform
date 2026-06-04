"""Export CSV, Excel, statistiques, rapports et graphiques."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import plotly.graph_objects as go


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convertit un DataFrame en CSV encodé UTF-8."""

    return df.to_csv(index=False).encode("utf-8-sig")


def dataframe_to_excel_bytes(df: pd.DataFrame, stats: pd.DataFrame | None = None) -> bytes:
    """Convertit un DataFrame en classeur Excel."""

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="dataset")
        if stats is not None and not stats.empty:
            stats.to_excel(writer, sheet_name="statistiques")
    return output.getvalue()


def report_to_markdown(df: pd.DataFrame, summary: str, stats: pd.DataFrame) -> str:
    """Crée un rapport d'analyse synthétique en Markdown."""

    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    return f"""# Rapport d'analyse des données de santé mentale

## Résumé automatique
{summary}

## Dimensions
- Lignes : {df.shape[0]}
- Colonnes : {df.shape[1]}
- Valeurs manquantes : {missing}
- Doublons : {duplicates}

## Statistiques descriptives

{stats.to_markdown() if not stats.empty else "Aucune colonne numérique disponible."}

## Recommandations
- Traiter les valeurs manquantes avant les visualisations finales.
- Vérifier les doublons pour éviter les biais.
- Contrôler les valeurs aberrantes des scores psychologiques.
- Documenter chaque transformation appliquée au dataset.
"""


def figure_to_png_bytes(fig: go.Figure) -> bytes | None:
    """Exporte une figure en PNG si Kaleido est disponible."""

    try:
        return fig.to_image(format="png", scale=2)
    except Exception:
        return None

