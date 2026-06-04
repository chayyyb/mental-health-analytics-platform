"""Page d'analyse exploratoire."""

from __future__ import annotations

import streamlit as st

from utils.helpers import MENTAL_HEALTH_ALIASES, init_session, mental_column, require_dataset, setup_page
from utils.statistiques import correlation_matrix, descriptive_statistics, missing_values_table
from utils.visualisation_utils import distribution_chart, heatmap_corr, mental_health_figures, missing_values_chart


setup_page("Analyse exploratoire")
init_session()

st.title("Analyse exploratoire")
df = require_dataset()
if df is None:
    st.stop()

tab_stats, tab_missing, tab_duplicates, tab_corr, tab_dist, tab_mental = st.tabs(
    ["Statistiques", "Valeurs manquantes", "Doublons", "Corrélations", "Distributions", "Santé mentale"]
)

with tab_stats:
    st.subheader("Analyse statistique")
    stats = descriptive_statistics(df)
    if stats.empty:
        st.info("Aucune colonne numérique disponible.")
    else:
        st.dataframe(stats, use_container_width=True)

with tab_missing:
    st.subheader("Analyse des valeurs manquantes")
    missing = missing_values_table(df)
    if missing.empty:
        st.success("Aucune valeur manquante détectée.")
    else:
        st.dataframe(missing, use_container_width=True)
        st.plotly_chart(missing_values_chart(df), use_container_width=True)

with tab_duplicates:
    st.subheader("Analyse des doublons")
    duplicate_count = int(df.duplicated().sum())
    st.metric("Nombre de doublons", duplicate_count)
    if duplicate_count:
        st.dataframe(df[df.duplicated(keep=False)], use_container_width=True)
    else:
        st.success("Aucune ligne dupliquée détectée.")

with tab_corr:
    st.subheader("Analyse des corrélations")
    corr = correlation_matrix(df)
    if corr.empty:
        st.info("Il faut au moins deux colonnes numériques.")
    else:
        st.dataframe(corr, use_container_width=True)
        st.plotly_chart(heatmap_corr(df), use_container_width=True)

with tab_dist:
    st.subheader("Analyse des distributions")
    column = st.selectbox("Colonne", df.columns)
    chart_type = st.selectbox("Type de graphique", ["Histogramme", "Boxplot", "Densité", "Diagramme circulaire", "Barres"])
    st.plotly_chart(distribution_chart(df, column, chart_type), use_container_width=True)

with tab_mental:
    st.subheader("Analyse spécifique santé mentale")
    detected = {concept: mental_column(df, concept) for concept in MENTAL_HEALTH_ALIASES}
    st.dataframe(
        [{"concept": concept, "colonne détectée": column or "Non trouvée"} for concept, column in detected.items()],
        use_container_width=True,
    )
    figures = mental_health_figures(df, detected)
    if not figures:
        st.warning("Aucune analyse spécifique possible avec les noms de colonnes actuels.")
    for title, fig in figures:
        st.markdown(f"### {title}")
        st.plotly_chart(fig, use_container_width=True)

