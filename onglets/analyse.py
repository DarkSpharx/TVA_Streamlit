import pandas as pd
import plotly.express as px
import streamlit as st

def afficher(selection, total):
    st.markdown(
    "<h3 style='text-align: center;'>🔍 Combien de numéros ont pu être envoyés à VIES ?</h3>",
    unsafe_allow_html=True,
)
    
    # Phrase d'aide liée aux filtres
    st.markdown(
        "<div style='color: #9ACD32; font-size: 0.8rem; margin-top: -10px; margin-bottom: 15px;'>"
        "Ce graphique en entonnoir s'actualise automatiquement selon les critères choisis dans le panneau latéral (pays, canal, période)."
        "</div>",
        unsafe_allow_html=True,
    )
    
    absents = (selection["etape_rejet"] == "absent").sum()
    doublons = (selection["etape_rejet"] == "doublon").sum()
    structure = (selection["etape_rejet"] == "structure").sum()
    
    entonnoir = pd.DataFrame({
        "étape": ["Référentiel", "Sans les absents", "Sans les doublons", "Envoyés à VIES"],
        "numéros": [
            total,
            total - absents,
            total - absents - doublons,
            total - absents - doublons - structure,
        ],
    })
    
    fig = px.funnel(
        entonnoir,
        x="numéros",
        y="étape",
        title="Du référentiel aux numéros envoyés à VIES",
    )
    st.plotly_chart(fig)