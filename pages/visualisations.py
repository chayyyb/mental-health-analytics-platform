"""Page de visualisations interactives."""

from __future__ import annotations

import streamlit as st

from utils.export_utils import figure_to_png_bytes
from utils.helpers import init_session, require_dataset, setup_page
from utils.visualisation_utils import custom_chart


setup_page("Visualisations")
init_session()

st.title("Visualisations interactives")
df = require_dataset()
if df is None:
    st.stop()

chart_type = st.selectbox(
    "Type de graphique",
    ["Histogramme", "Boxplot", "Heatmap", "Scatter plot", "Graphique temporel", "Graphique comparatif", "Graphique de corrélation"],
)

cols = df.columns.tolist()
x = st.selectbox("Colonne X", cols)
y = None
if chart_type not in ["Histogramme", "Heatmap", "Graphique de corrélation"]:
    y = st.selectbox("Colonne Y", cols)
color = st.selectbox("Couleur / groupe", ["Aucune"] + cols)

fig = custom_chart(df, chart_type, x, y, None if color == "Aucune" else color)
fig.update_layout(height=620, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

html = fig.to_html(include_plotlyjs="cdn").encode("utf-8")
st.download_button("Exporter le graphique en HTML", html, "graphique_sante_mentale.html", "text/html")

png = figure_to_png_bytes(fig)
if png:
    st.download_button("Exporter le graphique en PNG", png, "graphique_sante_mentale.png", "image/png")
else:
    st.info("Export PNG indisponible si Kaleido n'est pas installé. L'export HTML reste disponible.")

