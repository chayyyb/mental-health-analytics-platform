"""Page de prétraitement des données."""

from __future__ import annotations

import streamlit as st

from utils.helpers import add_history, categorical_columns, get_active_df, init_session, numeric_columns, require_dataset, save_dataset, setup_page
from utils.preprocessing_utils import (
    detect_outliers_iqr,
    filter_dataframe,
    handle_missing_values,
    normalize_minmax,
    one_hot_encode,
    remove_duplicates,
    remove_outliers_iqr,
    standardize_zscore,
)


setup_page("Prétraitement")
init_session()

st.title("Prétraitement des données")
df = require_dataset()
if df is None:
    st.stop()

original = get_active_df(clean=False)

tab_missing, tab_duplicates, tab_outliers, tab_transform, tab_select, tab_filter, tab_compare = st.tabs(
    ["Valeurs manquantes", "Doublons", "Valeurs aberrantes", "Transformations", "Variables", "Filtrage", "Avant / Après"]
)

with tab_missing:
    st.subheader("Gestion des valeurs manquantes")
    strategy = st.selectbox("Stratégie", ["Supprimer les lignes", "Supprimer les colonnes", "Moyenne", "Médiane", "Mode", "Valeur personnalisée"])
    cols = st.multiselect("Colonnes", df.columns.tolist(), default=df.columns[df.isna().any()].tolist())
    custom = st.text_input("Valeur personnalisée", "") if strategy == "Valeur personnalisée" else None
    if st.button("Appliquer la stratégie", type="primary"):
        try:
            cleaned = handle_missing_values(df, strategy, cols, custom)
            save_dataset(cleaned)
            add_history(f"Valeurs manquantes traitées avec la stratégie : {strategy}")
            st.success("Traitement appliqué.")
            st.rerun()
        except Exception as exc:
            st.error(f"Impossible d'appliquer le traitement : {exc}")

with tab_duplicates:
    st.subheader("Gestion des doublons")
    st.metric("Doublons détectés", int(df.duplicated().sum()))
    if st.button("Supprimer les doublons", type="primary"):
        cleaned = remove_duplicates(df)
        save_dataset(cleaned)
        add_history("Suppression des doublons")
        st.success("Doublons supprimés.")
        st.rerun()

with tab_outliers:
    st.subheader("Gestion des valeurs aberrantes")
    num_cols = numeric_columns(df)
    selected = st.multiselect("Colonnes numériques", num_cols, default=num_cols[:3])
    if selected:
        st.dataframe(detect_outliers_iqr(df, selected), use_container_width=True)
        col = st.selectbox("Visualisation", selected)
        st.box_chart(df[col])
    if st.button("Supprimer les valeurs aberrantes IQR", type="primary"):
        cleaned = remove_outliers_iqr(df, selected)
        save_dataset(cleaned)
        add_history("Suppression des valeurs aberrantes par IQR")
        st.success("Valeurs aberrantes supprimées.")
        st.rerun()

with tab_transform:
    st.subheader("Transformation des données")
    num_cols = numeric_columns(df)
    cat_cols = categorical_columns(df)
    action = st.selectbox("Transformation", ["Normalisation Min-Max", "Standardisation Z-Score", "Encodage One-Hot", "Renommage d'une colonne", "Changement de type"])

    if action in ["Normalisation Min-Max", "Standardisation Z-Score"]:
        cols = st.multiselect("Colonnes numériques", num_cols)
    elif action == "Encodage One-Hot":
        cols = st.multiselect("Colonnes catégorielles", cat_cols)
    else:
        cols = []

    if action == "Renommage d'une colonne":
        old = st.selectbox("Colonne actuelle", df.columns)
        new = st.text_input("Nouveau nom")
    elif action == "Changement de type":
        old = st.selectbox("Colonne", df.columns)
        new_type = st.selectbox("Nouveau type", ["str", "int", "float", "category"])

    if st.button("Appliquer la transformation", type="primary"):
        try:
            cleaned = df.copy()
            if action == "Normalisation Min-Max":
                cleaned = normalize_minmax(cleaned, cols)
            elif action == "Standardisation Z-Score":
                cleaned = standardize_zscore(cleaned, cols)
            elif action == "Encodage One-Hot":
                cleaned = one_hot_encode(cleaned, cols)
            elif action == "Renommage d'une colonne" and new:
                cleaned = cleaned.rename(columns={old: new})
            elif action == "Changement de type":
                cleaned[old] = cleaned[old].astype(new_type)
            save_dataset(cleaned)
            add_history(f"Transformation appliquée : {action}")
            st.success("Transformation appliquée.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erreur de transformation : {exc}")

with tab_select:
    st.subheader("Sélection des variables")
    keep_cols = st.multiselect("Colonnes à conserver", df.columns.tolist(), default=df.columns.tolist())
    if st.button("Conserver uniquement ces colonnes", type="primary"):
        save_dataset(df[keep_cols].copy())
        add_history("Sélection des variables utiles")
        st.success("Sélection appliquée.")
        st.rerun()

with tab_filter:
    st.subheader("Filtrage et tri")
    query = st.text_input("Recherche globale")
    sort_col = st.selectbox("Trier par", [""] + df.columns.tolist())
    ascending = st.radio("Ordre", ["Ascendant", "Descendant"], horizontal=True) == "Ascendant"
    filtered = filter_dataframe(df, query, sort_col or None, ascending)
    st.dataframe(filtered, use_container_width=True)
    if st.button("Utiliser ce résultat comme dataset nettoyé"):
        save_dataset(filtered)
        add_history("Filtrage dynamique appliqué")
        st.success("Dataset mis à jour.")
        st.rerun()

with tab_compare:
    st.subheader("Comparaison original / nettoyé")
    if original is None:
        st.info("Aucun dataset original disponible.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Original**")
            st.write(original.shape)
            st.dataframe(original.head(8), use_container_width=True)
        with c2:
            st.markdown("**Nettoyé**")
            st.write(df.shape)
            st.dataframe(df.head(8), use_container_width=True)

