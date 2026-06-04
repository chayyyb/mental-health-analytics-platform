"""Page d'accueil analytique."""

from __future__ import annotations

import streamlit as st

from utils.helpers import dataset_health_score, init_session, mental_column, render_kpi, require_dataset, setup_page


setup_page("Accueil")
init_session()

st.title("Accueil")
st.caption("Vue d'ensemble professionnelle du dataset de santé mentale.")

df = require_dataset()
if df is None:
    st.stop()

health = dataset_health_score(df)
age_col = mental_column(df, "age")
stress_col = mental_column(df, "stress")
anxiety_col = mental_column(df, "anxiety")
depression_col = mental_column(df, "depression")

cols = st.columns(4)
with cols[0]:
    render_kpi("Patients", df.shape[0])
with cols[1]:
    render_kpi("Âge moyen", round(df[age_col].mean(), 1) if age_col and df[age_col].dtype.kind in "biufc" else "N/D")
with cols[2]:
    render_kpi("Stress moyen", round(df[stress_col].mean(), 2) if stress_col and df[stress_col].dtype.kind in "biufc" else "N/D")
with cols[3]:
    render_kpi("Qualité dataset", f"{health.score}/100")

cols = st.columns(4)
with cols[0]:
    render_kpi("Anxiété détectée", "Oui" if anxiety_col else "Non")
with cols[1]:
    render_kpi("Dépression détectée", "Oui" if depression_col else "Non")
with cols[2]:
    render_kpi("Colonnes", df.shape[1])
with cols[3]:
    render_kpi("Lignes", df.shape[0])

st.info(health.recommendation)
st.dataframe(df.head(10), use_container_width=True)

