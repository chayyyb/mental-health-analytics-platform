"""Page de présentation du projet."""

from __future__ import annotations

import streamlit as st

from utils.helpers import init_session, setup_page


setup_page("À propos")
init_session()

st.title("À propos")
st.markdown(
    """
    Cette plateforme universitaire permet d'analyser des données de santé mentale
    à partir d'un fichier CSV. Elle couvre l'importation, l'analyse exploratoire,
    le nettoyage, le prétraitement, les visualisations interactives et l'exportation.

    **Technologies utilisées :** Python 3.12, Streamlit, Pandas, NumPy, Plotly,
    Matplotlib et OpenPyXL.

    **Objectif pédagogique :** fournir une application claire, moderne et réutilisable
    pour comprendre les relations entre variables psychologiques, comportementales
    et sociodémographiques.
    """
)

st.markdown("### Historique de traitement")
history = st.session_state.get("history", [])
if history:
    for item in history:
        st.write(f"- {item}")
else:
    st.info("Aucun traitement enregistré.")

