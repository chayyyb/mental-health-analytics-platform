"""Graphiques Plotly pour la plateforme."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


DEFAULT_SEQUENCE = ["#1769aa", "#00a896", "#f59f00", "#d9480f", "#845ef7", "#495057"]


def heatmap_corr(df: pd.DataFrame) -> go.Figure:
    """Crée une heatmap de corrélation interactive."""

    corr = df.select_dtypes(include="number").corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", aspect="auto")
    fig.update_layout(title="Matrice de corrélation", height=560)
    return fig


def missing_values_chart(df: pd.DataFrame) -> go.Figure:
    """Graphique des valeurs manquantes par colonne."""

    missing = df.isna().sum().reset_index()
    missing.columns = ["colonne", "valeurs_manquantes"]
    missing = missing[missing["valeurs_manquantes"] > 0].sort_values("valeurs_manquantes", ascending=False)
    fig = px.bar(missing, x="colonne", y="valeurs_manquantes", color_discrete_sequence=["#d9480f"])
    fig.update_layout(title="Valeurs manquantes par colonne", xaxis_title="", yaxis_title="Nombre")
    return fig


def distribution_chart(df: pd.DataFrame, column: str, chart_type: str) -> go.Figure:
    """Crée un graphique de distribution pour une colonne."""

    if chart_type == "Histogramme":
        return px.histogram(df, x=column, marginal="box", color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Boxplot":
        return px.box(df, y=column, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Densité":
        return px.histogram(df, x=column, histnorm="probability density", color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Diagramme circulaire":
        counts = df[column].value_counts(dropna=False).reset_index()
        counts.columns = [column, "nombre"]
        return px.pie(counts, names=column, values="nombre", color_discrete_sequence=DEFAULT_SEQUENCE)
    counts = df[column].value_counts(dropna=False).reset_index()
    counts.columns = [column, "nombre"]
    return px.bar(counts, x=column, y="nombre", color_discrete_sequence=DEFAULT_SEQUENCE)


def custom_chart(df: pd.DataFrame, chart_type: str, x: str | None, y: str | None = None, color: str | None = None) -> go.Figure:
    """Construit un graphique choisi par l'utilisateur."""

    color_args = {"color": color} if color else {}
    if chart_type == "Histogramme":
        return px.histogram(df, x=x, **color_args, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Boxplot":
        return px.box(df, x=x, y=y, **color_args, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Scatter plot":
        return px.scatter(df, x=x, y=y, **color_args, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Graphique temporel":
        return px.line(df, x=x, y=y, **color_args, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Graphique comparatif":
        return px.bar(df, x=x, y=y, **color_args, color_discrete_sequence=DEFAULT_SEQUENCE)
    if chart_type == "Heatmap":
        return heatmap_corr(df)
    return px.scatter_matrix(df.select_dtypes(include="number"), color_discrete_sequence=DEFAULT_SEQUENCE)


def mental_health_figures(df: pd.DataFrame, columns: dict[str, str | None]) -> list[tuple[str, go.Figure]]:
    """Génère des analyses spécifiques à la santé mentale selon les colonnes présentes."""

    figures: list[tuple[str, go.Figure]] = []
    for label, concept in [("Répartition du stress", "stress"), ("Répartition de l'anxiété", "anxiety"), ("Répartition de la dépression", "depression")]:
        col = columns.get(concept)
        if col:
            figures.append((label, distribution_chart(df, col, "Histogramme")))

    if columns.get("sleep") and columns.get("stress"):
        figures.append(("Impact du sommeil sur le stress", px.scatter(df, x=columns["sleep"], y=columns["stress"], trendline="ols", color_discrete_sequence=DEFAULT_SEQUENCE)))
    if columns.get("work_hours") and columns.get("stress"):
        figures.append(("Impact des heures de travail sur le stress", px.scatter(df, x=columns["work_hours"], y=columns["stress"], trendline="ols", color_discrete_sequence=DEFAULT_SEQUENCE)))
    if columns.get("gender") and columns.get("stress"):
        figures.append(("Comparaison par genre", px.box(df, x=columns["gender"], y=columns["stress"], color=columns["gender"], color_discrete_sequence=DEFAULT_SEQUENCE)))
    if columns.get("age") and columns.get("stress"):
        temp = df.copy()
        temp["tranche_age"] = pd.cut(temp[columns["age"]], bins=[0, 18, 25, 35, 45, 60, 120], labels=["<18", "18-25", "26-35", "36-45", "46-60", "60+"])
        figures.append(("Analyse par tranche d'âge", px.box(temp, x="tranche_age", y=columns["stress"], color_discrete_sequence=DEFAULT_SEQUENCE)))
    return figures

