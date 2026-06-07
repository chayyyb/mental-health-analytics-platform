"""Helpers UI, session et détection de colonnes."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st


PRIMARY_COLOR = "#1769aa"
ACCENT_COLOR = "#00a896"
WARNING_COLOR = "#f59f00"
DANGER_COLOR = "#d9480f"


MENTAL_HEALTH_ALIASES: dict[str, tuple[str, ...]] = {
    "age": ("age", "âge"),
    "gender": ("gender", "genre", "sexe", "sex"),
    "stress": ("stress", "stress_level", "niveau_stress", "niveau de stress"),
    "anxiety": ("anxiety", "anxiété", "anxiety_level", "niveau_anxiete"),
    "depression": ("depression", "dépression", "depression_level", "niveau_depression"),
    "sleep": ("sleep", "sommeil", "sleep_hours", "heures_sommeil", "sleep duration"),
    "work_hours": ("work_hours", "heures_travail", "working_hours", "work hours"),
    "treatment": ("treatment", "traitement", "mental_health_treatment"),
}


@dataclass(frozen=True)
class DatasetHealth:
    """Résumé de qualité globale du dataset."""

    score: float
    missing_rate: float
    duplicate_rate: float
    numeric_rate: float
    recommendation: str


def setup_page(title: str) -> None:
    """Configure une page Streamlit avec styles communs."""

    st.set_page_config(page_title=title, page_icon="🧠", layout="wide")
    dark = st.session_state.get("dark_mode", False)
    background = "#0f172a" if dark else "#ffffff"
    panel = "#111827" if dark else "#ffffff"
    text = "#e5e7eb" if dark else "#1f2937"
    soft = "#1f2937" if dark else "#f5f9fc"
    border = "#334155" if dark else "#d9e8f5"
    st.markdown(
        f"""
        <style>
        :root {{
            --primary: #1769aa;
            --accent: #00a896;
            --soft: {soft};
            --text: {text};
        }}
        .stApp {{background: {background}; color: {text};}}
        header {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        [data-testid="stStatusWidget"] {{display: none;}}
        .main .block-container {{padding-top: 1.6rem; padding-bottom: 2rem;}}
        [data-testid="stSidebar"] {{background: linear-gradient(180deg, #0f4c81 0%, #1769aa 100%);}}
        [data-testid="stSidebar"] * {{color: white;}}
        .kpi-card {{
            background: {panel};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 1rem;
            min-height: 112px;
            box-shadow: 0 8px 24px rgba(15, 76, 129, .08);
        }}
        .kpi-label {{color: #7ba7c7; font-size: .82rem; font-weight: 700; text-transform: uppercase;}}
        .kpi-value {{color: #37b6ff; font-size: 1.75rem; font-weight: 800; margin-top: .35rem;}}
        .info-band {{
            background: {soft};
            border-left: 4px solid #1769aa;
            border-radius: 8px;
            padding: 1rem;
            color: {text};
        }}
        .section-title {{font-size: 1.25rem; font-weight: 800; color: #37b6ff; margin-top: 1rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.toggle("Mode sombre", key="dark_mode")


def init_session() -> None:
    """Initialise les objets persistants de l'application."""

    defaults = {
        "df_original": None,
        "df_clean": None,
        "file_name": None,
        "history": [],
        "dark_mode": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    if os.environ.get("MENTAL_HEALTH_DEMO") == "1" and st.session_state.df_original is None:
        demo_path = Path(__file__).resolve().parents[1] / "data" / "exemple_sante_mentale.csv"
        if demo_path.exists():
            demo_df = pd.read_csv(demo_path)
            st.session_state.df_original = demo_df.copy()
            st.session_state.df_clean = demo_df.copy()
            st.session_state.file_name = demo_path.name
            st.session_state.history = ["Chargement automatique du dataset d'exemple pour la démonstration"]


def get_active_df(clean: bool = True) -> pd.DataFrame | None:
    """Retourne le dataset actif."""

    key = "df_clean" if clean else "df_original"
    df = st.session_state.get(key)
    return df.copy() if isinstance(df, pd.DataFrame) else None


def save_dataset(df: pd.DataFrame, cleaned: bool = True) -> None:
    """Sauvegarde un dataset en session."""

    if cleaned:
        st.session_state.df_clean = df.copy()
    else:
        st.session_state.df_original = df.copy()


def add_history(action: str) -> None:
    """Ajoute une action dans l'historique utilisateur."""

    st.session_state.setdefault("history", [])
    st.session_state.history.append(action)


def render_kpi(label: str, value: object, help_text: str | None = None) -> None:
    """Affiche une carte KPI."""

    help_html = f"<div style='color:#6b7280;font-size:.78rem;margin-top:.35rem'>{help_text}</div>" if help_text else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {help_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """Liste les colonnes numériques."""

    return df.select_dtypes(include="number").columns.tolist()


def categorical_columns(df: pd.DataFrame) -> list[str]:
    """Liste les colonnes catégorielles."""

    return df.select_dtypes(exclude="number").columns.tolist()


def find_column(df: pd.DataFrame, aliases: Iterable[str]) -> str | None:
    """Trouve une colonne même si son nom varie selon le dataset."""

    normalized = {col.lower().strip().replace("-", "_"): col for col in df.columns}
    for alias in aliases:
        key = alias.lower().strip().replace("-", "_")
        if key in normalized:
            return normalized[key]
    for col in df.columns:
        low = col.lower()
        if any(alias.lower() in low for alias in aliases):
            return col
    return None


def mental_column(df: pd.DataFrame, concept: str) -> str | None:
    """Retourne la colonne associée à un concept de santé mentale."""

    return find_column(df, MENTAL_HEALTH_ALIASES.get(concept, (concept,)))


def dataset_health_score(df: pd.DataFrame) -> DatasetHealth:
    """Calcule un score simple de santé du dataset sur 100."""

    total_cells = max(df.shape[0] * df.shape[1], 1)
    missing_rate = float(df.isna().sum().sum() / total_cells)
    duplicate_rate = float(df.duplicated().mean()) if len(df) else 0.0
    numeric_rate = float(len(numeric_columns(df)) / max(len(df.columns), 1))
    score = 100 - (missing_rate * 55) - (duplicate_rate * 35)
    score = max(0.0, min(100.0, score))

    if score >= 85:
        rec = "Dataset de bonne qualité. L'analyse peut commencer après une vérification rapide."
    elif score >= 65:
        rec = "Qualité correcte. Traiter les valeurs manquantes et doublons avant l'analyse finale."
    else:
        rec = "Qualité fragile. Nettoyage prioritaire recommandé avant toute interprétation."

    return DatasetHealth(
        score=round(score, 1),
        missing_rate=round(missing_rate * 100, 2),
        duplicate_rate=round(duplicate_rate * 100, 2),
        numeric_rate=round(numeric_rate * 100, 2),
        recommendation=rec,
    )


def require_dataset() -> pd.DataFrame | None:
    """Affiche un message clair si aucun dataset n'est chargé."""

    df = get_active_df()
    if df is None:
        st.warning("Importez d'abord un fichier CSV depuis la page Importation.")
        return None
    return df
