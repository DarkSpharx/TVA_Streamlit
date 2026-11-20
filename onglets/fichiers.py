import streamlit as st

def afficher(selection):
    # Style CSS pour colorer les boutons en bleu Plotly
    st.markdown(
        """
        <style>
        .stDownloadButton button {
            background-color: #636EFA !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        .stDownloadButton button:hover {
            background-color: #4B55E0 !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(99, 110, 250, 0.4) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # 1. DONNÉES BRUTES (En premier)
    # -------------------------------------------------------------------------
    st.markdown(
        "<h3 style='text-align: center;'>📦 Données brutes</h3>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
        "<p style='color: #9ACD32; font-size: 14px;'>Consultez l'ensemble du référentiel issu de la campagne VIES ou téléchargez le fichier source complet non filtré.</p>",
        unsafe_allow_html=True,
    )
    
    with open("data/resultats_vies.csv", "rb") as f:
        csv_brut = f.read()

    col_txt1, col_btn1 = st.columns([2, 1])
    with col_txt1:
        st.write("")  # Espace équilibré
    with col_btn1:
        st.download_button(
            label="Télécharger le fichier brut (CSV)",
            data=csv_brut,
            file_name="resultats_vies.csv",
            mime="text/csv",
            icon=":material/download:",
            use_container_width=True,
        )

    with st.expander("Voir toutes les données brutes"):
        st.dataframe(selection, hide_index=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(154, 205, 50, 0.7), transparent); margin: 35px 0;'></div>
        """,
        unsafe_allow_html=True
    )
    
    # -------------------------------------------------------------------------
    # 2. EXPORT NUMÉROS À TRAITER (En second)
    # -------------------------------------------------------------------------
    st.markdown(
        "<h3 style='text-align: center;'>📥 Export des numéros à traiter (selon vos filtres)</h3>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
        "<p style='color: #9ACD32; font-size: 14px;'>Ce tableau et le fichier à télécharger s'actualisent automatiquement selon les filtres choisis dans la barre latérale.</p>",
        unsafe_allow_html=True,
    )
    
    # Filtrer les numéros qui ne sont pas valides
    a_traiter = selection[selection["statut"] != "valide"].copy()
    
    # Attribuer l'action à mener
    a_traiter["action"] = a_traiter["statut"].map({
        "invalide": "Demander un nouveau numéro au client",
        "non_tranche": "Revérifier sur VIES avant la prochaine facture",
    })
    
    colonnes = ["raison_sociale", "numero_saisi", "pays_declare", "statut", "motif", "action"]
    
    # Ligne avec le texte à gauche et le bouton à droite
    col_txt, col_btn2 = st.columns([2, 1])
    with col_txt:
        st.write(f"**{len(a_traiter)}** numéros demandent une action.")
    with col_btn2:
        st.download_button(
            label="Télécharger la liste filtrée (CSV)",
            data=a_traiter[colonnes].to_csv(index=False, sep=";").encode("utf-8-sig"),
            file_name="numeros_a_traiter.csv",
            icon=":material/download:",
            use_container_width=True,
        )
    
    # Tableau caché par défaut dans un expander
    with st.expander(f"Voir les {len(a_traiter)} numéros à traiter"):
        st.dataframe(a_traiter[colonnes], hide_index=True)
