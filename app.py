"""
Tableau de bord TVA — Meridian Distribution.

Lancement : streamlit run app.py
"""

import pandas as pd
import streamlit as st

# Import des onglets
from onglets import accueil, analyse, graphiques, fichiers

st.set_page_config(page_title="Référentiel TVA", layout="wide")


@st.cache_data
def charger_donnees():
    df = pd.read_csv(
        "data/resultats_vies.csv",
        parse_dates=["date_saisie", "date_verification"],
        encoding="utf-8",
    )
    df["etape_rejet"] = df["etape_rejet"].fillna("envoyé à VIES")
    return df


df = charger_donnees()

# =============================================================================
# BARRE LATÉRALE
# =============================================================================
# 1. CSS bouton Dashboard
st.sidebar.markdown(
    """
    <style>
    .btn-cloud {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background: linear-gradient(135deg, #9ACD32 0%, #7AA822 100%);
        color: #1a1a1a !important;
        padding: 12px 18px;
        border-radius: 12px;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.3px;
        box-shadow: none !important;
        transition: all 0.2s ease;
        margin-bottom: 12px;
    }
    .btn-cloud:hover {
        transform: translateY(-2px);
        box-shadow: none !important;
        color: #000000 !important;
    }
    </style>
    <a class="btn-cloud" href="https://tva-meridian-darkspharx.streamlit.app/" target="_self">
        📊 Dashboard
    </a>
    """,
    unsafe_allow_html=True,
)

# 2. Le liseré
st.sidebar.markdown(
    """
    <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(154, 205, 50, 0.7), transparent); margin: 20px 0;'></div>
    """,
    unsafe_allow_html=True,
)

# 3. Les filtres
st.sidebar.header("Filtres")

pays = st.sidebar.multiselect("Pays déclaré", sorted(df["pays_declare"].unique()))
sources_saisie = st.sidebar.multiselect("Canal de saisie", sorted(df["source_saisie"].unique()))

debut, fin = st.sidebar.slider(
    "Période de saisie",
    min_value=df["date_saisie"].min().date(),
    max_value=df["date_saisie"].max().date(),
    value=(df["date_saisie"].min().date(), df["date_saisie"].max().date()),
    format="DD/MM/YYYY",
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 4. Info VIES 
derniere = df["date_verification"].max()
st.sidebar.info(
    f"Dernière vérification VIES : {derniere:%d/%m/%Y à %H:%M}.\n\n"
    "Règle : un numéro non tranché ne doit pas être facturé hors taxe tant qu'il n'a pas été revérifié."
)

# =============================================================================
# APPLICATION DES FILTRES
# =============================================================================
selection = df
if pays:
    selection = selection[selection["pays_declare"].isin(pays)]

if sources_saisie:
    selection = selection[selection["source_saisie"].isin(sources_saisie)]

selection = selection[selection["date_saisie"].dt.date.between(debut, fin)]

# =============================================================================
# EN-TÊTE
# =============================================================================
st.markdown(
    """
    <style>
    /* Alignement vertical au pixel près du bouton et du titre */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    [data-testid="stSidebarHeader"] {
        display: none;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 3.8rem !important;
    }

    /* Couleur du titre principal et calage haut */
    h1 {
        color: #9ACD32 !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Qualité du référentiel TVA")

# Calcul des métriques
total = len(selection)
valides = (selection["statut"] == "valide").sum()
invalides = (selection["statut"] == "invalide").sum()
non_tranches = (selection["statut"] == "non_tranche").sum()

# =============================================================================
# LES ONGLETS
# =============================================================================
onglet1, onglet2, onglet3, onglet4 = st.tabs(["Accueil", "Analyse", "Graphiques", "Fichiers"])

with onglet1:
    # 1. Le texte de bienvenue et explications
    accueil.afficher(df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Les 4 chiffres clés
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Numéros", total)
    col2.metric("Valides", valides, f"{valides / total:.1%} du total" if total else "0%", delta_color="off")
    col3.metric("Invalides", invalides, f"{invalides / total:.1%} du total" if total else "0%", delta_color="off")
    col4.metric("Non tranchés", non_tranches, f"{non_tranches / total:.1%} du total" if total else "0%", delta_color="off")

with onglet2:
    analyse.afficher(selection, total)

with onglet3:
    graphiques.afficher(selection)

with onglet4:
    fichiers.afficher(selection)