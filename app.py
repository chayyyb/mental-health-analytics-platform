"""Point d'entrée de la plateforme Streamlit."""

from __future__ import annotations

import streamlit as st

from utils.helpers import dataset_health_score, init_session, mental_column, render_kpi, require_dataset, setup_page


setup_page("Plateforme d'Analyse des Données de Santé Mentale")
init_session()

st.sidebar.image("assets/logo.svg", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.info("Utilisez les pages du menu pour importer, analyser, nettoyer, visualiser et exporter vos données.")

st.title("Plateforme d'Analyse des Données de Santé Mentale")
st.caption("Analyse exploratoire, prétraitement et visualisation des données psychologiques et comportementales.")

df = require_dataset()
if df is None:
    st.markdown(
        """
        <div class="info-band">
            Commencez par la page <strong>Importation</strong> pour charger un fichier CSV.
            L'application détecte automatiquement les variables de stress, anxiété, dépression,
            sommeil, âge, genre et heures de travail lorsqu'elles existent.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

health = dataset_health_score(df)
age_col = mental_column(df, "age")
stress_col = mental_column(df, "stress")
anxiety_col = mental_column(df, "anxiety")
depression_col = mental_column(df, "depression")

cols = st.columns(4)
with cols[0]:
    render_kpi("Patients", f"{len(df):,}".replace(",", " "))
with cols[1]:
    value = round(df[age_col].mean(), 1) if age_col and df[age_col].dtype.kind in "biufc" else "N/D"
    render_kpi("Âge moyen", value)
with cols[2]:
    value = round(df[stress_col].mean(), 2) if stress_col and df[stress_col].dtype.kind in "biufc" else "N/D"
    render_kpi("Stress moyen", value)
with cols[3]:
    render_kpi("Score qualité", f"{health.score}/100", health.recommendation)

cols = st.columns(4)
with cols[0]:
    render_kpi("Taux anxiété", f"{round(df[anxiety_col].notna().mean() * 100, 1)}%" if anxiety_col else "N/D")
with cols[1]:
    render_kpi("Taux dépression", f"{round(df[depression_col].notna().mean() * 100, 1)}%" if depression_col else "N/D")
with cols[2]:
    render_kpi("Colonnes", df.shape[1])
with cols[3]:
    render_kpi("Lignes", df.shape[0])

st.markdown('<div class="section-title">Aperçu du dataset actif</div>', unsafe_allow_html=True)
st.dataframe(df.head(12), use_container_width=True)

st.markdown('<div class="section-title">Historique des traitements</div>', unsafe_allow_html=True)
history = st.session_state.get("history", [])
if history:
    for item in history[-8:]:
        st.success(item)
else:
    st.info("Aucun traitement appliqué pour le moment.")
