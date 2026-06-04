"""Page d'importation CSV."""

from __future__ import annotations

import streamlit as st

from utils.data_loader import dataset_overview, load_csv, summarize_dataset
from utils.helpers import add_history, dataset_health_score, init_session, render_kpi, save_dataset, setup_page


setup_page("Importation")
init_session()

st.title("Importation des données")
st.caption("Chargez un fichier CSV de santé mentale pour démarrer l'analyse.")

with st.sidebar:
    st.subheader("Paramètres CSV")
    sep = st.selectbox("Séparateur", [",", ";", "\t"], index=0)
    encoding = st.selectbox("Encodage", ["utf-8", "latin-1"], index=0)

uploaded_file = st.file_uploader("Importer un fichier CSV", type=["csv"])

if uploaded_file:
    try:
        with st.spinner("Chargement du dataset..."):
            df = load_csv(uploaded_file, sep=sep, encoding=encoding)
            save_dataset(df, cleaned=False)
            save_dataset(df, cleaned=True)
            st.session_state.file_name = uploaded_file.name
            add_history(f"Importation du fichier {uploaded_file.name}")
        st.success("Fichier importé avec succès.")
    except Exception as exc:
        st.error(f"Erreur d'importation : {exc}")

df = st.session_state.get("df_original")
if df is not None:
    overview = dataset_overview(df)
    health = dataset_health_score(df)

    cols = st.columns(4)
    with cols[0]:
        render_kpi("Lignes", overview["lignes"])
    with cols[1]:
        render_kpi("Colonnes", overview["colonnes"])
    with cols[2]:
        render_kpi("Doublons", overview["doublons"])
    with cols[3]:
        render_kpi("Mémoire", f"{overview['memoire_mo']} Mo")

    cols = st.columns(3)
    with cols[0]:
        render_kpi("Colonnes numériques", len(overview["colonnes_numeriques"]))
    with cols[1]:
        render_kpi("Colonnes catégorielles", len(overview["colonnes_categorielles"]))
    with cols[2]:
        render_kpi("Score qualité", f"{health.score}/100")

    st.markdown('<div class="section-title">Résumé automatique</div>', unsafe_allow_html=True)
    st.write(summarize_dataset(df))
    st.info(health.recommendation)

    st.markdown('<div class="section-title">Aperçu du dataset</div>', unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown('<div class="section-title">Types des colonnes</div>', unsafe_allow_html=True)
    st.dataframe(df.dtypes.astype(str).rename("type").reset_index().rename(columns={"index": "colonne"}), use_container_width=True)

    st.markdown('<div class="section-title">Statistiques descriptives</div>', unsafe_allow_html=True)
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

