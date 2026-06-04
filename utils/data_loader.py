"""Chargement et résumé des datasets CSV."""

from __future__ import annotations

from io import BytesIO

import pandas as pd


def load_csv(uploaded_file: BytesIO, sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    """Charge un fichier CSV avec validation minimale."""

    if uploaded_file is None:
        raise ValueError("Aucun fichier fourni.")
    if not getattr(uploaded_file, "name", "").lower().endswith(".csv"):
        raise ValueError("Le fichier doit être au format CSV.")

    try:
        df = pd.read_csv(uploaded_file, sep=sep, encoding=encoding)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=sep, encoding="latin-1")

    if df.empty:
        raise ValueError("Le fichier CSV est vide.")
    return df


def dataset_overview(df: pd.DataFrame) -> dict[str, object]:
    """Retourne les informations principales du dataset."""

    return {
        "lignes": df.shape[0],
        "colonnes": df.shape[1],
        "doublons": int(df.duplicated().sum()),
        "memoire_mo": round(df.memory_usage(deep=True).sum() / 1024**2, 3),
        "colonnes_numeriques": df.select_dtypes(include="number").columns.tolist(),
        "colonnes_categorielles": df.select_dtypes(exclude="number").columns.tolist(),
    }


def summarize_dataset(df: pd.DataFrame) -> str:
    """Génère un résumé automatique du dataset."""

    numeric = len(df.select_dtypes(include="number").columns)
    categorical = len(df.select_dtypes(exclude="number").columns)
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    return (
        f"Le dataset contient {df.shape[0]} lignes et {df.shape[1]} colonnes. "
        f"Il comprend {numeric} variables numériques et {categorical} variables catégorielles. "
        f"On observe {missing} valeurs manquantes et {duplicates} lignes dupliquées."
    )

