import streamlit as st

def afficher(selection):
    st.markdown(
        "<h3 style='text-align: center;'>📦 Gestion des fichiers et données</h3>",
        unsafe_allow_html=True,
    )
    
    tab_brut, tab_filtre = st.tabs(["Données brutes", "Données filtrées"])
    
    with tab_brut:
        st.markdown(
            "<p style='color: #9ACD32; font-size: 14px;'>Consultez l'ensemble du référentiel issu de la campagne VIES ou téléchargez le fichier source complet non filtré.</p>",
            unsafe_allow_html=True,
        )
        
        with open("data/resultats_vies.csv", "rb") as f:
            csv_brut = f.read()

        with st.expander(f"Voir toutes les données brutes ({len(selection)})"):
            st.dataframe(selection, hide_index=True)
        
        col_txt1, col_btn1 = st.columns([2, 1])
        with col_txt1:
            st.write(f"**{len(selection)}** numéros de TVA (données brutes).")
        with col_btn1:
            st.download_button(
                label="Télécharger le fichier brut (CSV)",
                data=csv_brut,
                file_name="resultats_vies.csv",
                mime="text/csv",
                icon=":material/download:",
                use_container_width=True,
            )
            
    with tab_filtre:
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
        
        # Tableau caché par défaut dans un expander
        with st.expander(f"Voir les {len(a_traiter)} numéros TVA filtrés"):
            st.dataframe(a_traiter[colonnes], hide_index=True)
            
        # Ligne avec le texte à gauche et le bouton à droite
        col_txt, col_btn2 = st.columns([2, 1])
        with col_txt:
            st.write(f"**{len(a_traiter)}** numéros TVA filtrés.")
        with col_btn2:
            st.download_button(
                label="Télécharger la liste filtrée (CSV)",
                data=a_traiter[colonnes].to_csv(index=False, sep=";").encode("utf-8-sig"),
                file_name="numeros_a_traiter.csv",
                icon=":material/download:",
                use_container_width=True,
        )
