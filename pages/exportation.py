"""Page d'exportation des résultats."""

from __future__ import annotations

import streamlit as st

from utils.data_loader import summarize_dataset
from utils.export_utils import dataframe_to_csv_bytes, dataframe_to_excel_bytes, report_to_markdown
from utils.helpers import init_session, require_dataset, setup_page
from utils.statistiques import descriptive_statistics


setup_page("Exportation")
init_session()

st.title("Exportation")
df = require_dataset()
if df is None:
    st.stop()

stats = descriptive_statistics(df)
summary = summarize_dataset(df)
report = report_to_markdown(df, summary, stats)

st.download_button("Exporter le dataset nettoyé en CSV", dataframe_to_csv_bytes(df), "dataset_sante_mentale_nettoye.csv", "text/csv")
st.download_button(
    "Exporter le dataset nettoyé en Excel",
    dataframe_to_excel_bytes(df, stats),
    "dataset_sante_mentale_nettoye.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
st.download_button("Exporter les statistiques en CSV", dataframe_to_csv_bytes(stats.reset_index()), "statistiques_sante_mentale.csv", "text/csv")
st.download_button("Exporter le rapport d'analyse", report.encode("utf-8"), "rapport_analyse_sante_mentale.md", "text/markdown")

st.markdown("### Aperçu du rapport")
st.markdown(report)

