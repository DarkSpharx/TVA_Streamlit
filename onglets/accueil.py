import streamlit as st

def afficher(df):
    st.markdown(
    "<h3 style='text-align: center;'>👋 Bienvenue sur le tableau de bord TVA</h3>",
    unsafe_allow_html=True,
)
    
    # 1. Texte d'information
    st.write(
        "Ce tableau de bord permet de suivre la conformité des numéros de TVA intracommunautaires de nos clients suite à la campagne de vérification VIES. Utilisez les filtres dans le volet de gauche pour affiner l'analyse."
    )
    
   
