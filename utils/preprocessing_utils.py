"""Prétraitement, nettoyage et transformation des données."""

from __future__ import annotations

import numpy as np
import pandas as pd


def handle_missing_values(df: pd.DataFrame, strategy: str, columns: list[str], custom_value: str | float | None = None) -> pd.DataFrame:
    """Applique une stratégie de gestion des valeurs manquantes."""

    result = df.copy()
    if strategy == "Supprimer les lignes":
        return result.dropna(subset=columns or None)
    if strategy == "Supprimer les colonnes":
        return result.drop(columns=columns, errors="ignore")

    for col in columns:
        if col not in result.columns:
            continue
        if strategy == "Moyenne" and pd.api.types.is_numeric_dtype(result[col]):
            result[col] = result[col].fillna(result[col].mean())
        elif strategy == "Médiane" and pd.api.types.is_numeric_dtype(result[col]):
            result[col] = result[col].fillna(result[col].median())
        elif strategy == "Mode":
            mode = result[col].mode(dropna=True)
            if not mode.empty:
                result[col] = result[col].fillna(mode.iloc[0])
        elif strategy == "Valeur personnalisée":
            result[col] = result[col].fillna(custom_value)
    return result


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les lignes dupliquées."""

    return df.drop_duplicates().reset_index(drop=True)


def detect_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Détecte les valeurs aberrantes avec la méthode IQR."""

    records: list[dict[str, object]] = []
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        records.append(
            {
                "colonne": col,
                "borne_inférieure": round(lower, 3),
                "borne_supérieure": round(upper, 3),
                "valeurs_aberrantes": int(mask.sum()),
            }
        )
    return pd.DataFrame(records)


def remove_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Supprime les lignes contenant des valeurs aberrantes IQR."""

    result = df.copy()
    for col in columns:
        if col not in result.columns or not pd.api.types.is_numeric_dtype(result[col]):
            continue
        q1 = result[col].quantile(0.25)
        q3 = result[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        result = result[(result[col] >= lower) & (result[col] <= upper)]
    return result.reset_index(drop=True)


def normalize_minmax(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Normalise les colonnes sélectionnées entre 0 et 1."""

    result = df.copy()
    for col in columns:
        min_value = result[col].min()
        max_value = result[col].max()
        if max_value != min_value:
            result[col] = (result[col] - min_value) / (max_value - min_value)
    return result


def standardize_zscore(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Standardise les colonnes sélectionnées par Z-score."""

    result = df.copy()
    for col in columns:
        std = result[col].std()
        if std and not np.isnan(std):
            result[col] = (result[col] - result[col].mean()) / std
    return result


def one_hot_encode(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Encode les variables catégorielles en one-hot."""

    return pd.get_dummies(df, columns=columns, drop_first=False)


def filter_dataframe(df: pd.DataFrame, query_text: str = "", sort_column: str | None = None, ascending: bool = True) -> pd.DataFrame:
    """Filtre globalement un dataset et applique un tri optionnel."""

    result = df.copy()
    if query_text:
        mask = result.astype(str).apply(lambda col: col.str.contains(query_text, case=False, na=False)).any(axis=1)
        result = result[mask]
    if sort_column and sort_column in result.columns:
        result = result.sort_values(sort_column, ascending=ascending)
    return result

