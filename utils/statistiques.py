"""Fonctions statistiques pour l'analyse exploratoire."""

from __future__ import annotations

import pandas as pd


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule moyenne, médiane, mode, variance, écart-type et quartiles."""

    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()

    mode = numeric_df.mode(numeric_only=True).iloc[0] if not numeric_df.mode().empty else pd.Series()
    stats = pd.DataFrame(
        {
            "moyenne": numeric_df.mean(),
            "médiane": numeric_df.median(),
            "mode": mode,
            "variance": numeric_df.var(),
            "écart-type": numeric_df.std(),
            "minimum": numeric_df.min(),
            "q1": numeric_df.quantile(0.25),
            "q2": numeric_df.quantile(0.50),
            "q3": numeric_df.quantile(0.75),
            "maximum": numeric_df.max(),
        }
    )
    return stats.round(3)


def missing_values_table(df: pd.DataFrame) -> pd.DataFrame:
    """Construit le tableau des valeurs manquantes."""

    missing = df.isna().sum()
    percent = (missing / max(len(df), 1) * 100).round(2)
    return (
        pd.DataFrame({"valeurs_manquantes": missing, "pourcentage": percent})
        .query("valeurs_manquantes > 0")
        .sort_values("pourcentage", ascending=False)
    )


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne la matrice de corrélation numérique."""

    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr(numeric_only=True).round(3)

