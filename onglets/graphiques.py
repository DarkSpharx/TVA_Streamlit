import plotly.express as px
import streamlit as st

def taux_invalides(donnees, colonne):
    """Calcule la part de numéros invalides en % pour chaque valeur de la colonne."""
    return (
        donnees.groupby(colonne)["statut"]
        .apply(lambda statuts: round((statuts == "invalide").mean() * 100, 1))
        .sort_values()
        .reset_index(name="taux d'erreur (%)")
    )

def afficher(selection):
    st.markdown(
    "<h3 style='text-align: center;'>📊 D'où viennent les erreurs ?</h3>",
    unsafe_allow_html=True,
)
    
    # 1. Par canal de saisie
    taux_canal = taux_invalides(selection, "source_saisie")
    fig_canal = px.bar(
        taux_canal,
        x="taux d'erreur (%)",
        y="source_saisie",
        orientation="h",
        text="taux d'erreur (%)",
        title="Part de numéros invalides par canal de saisie",
    )
    st.plotly_chart(fig_canal)
    
    st.markdown(
        "<div style='text-align: center; color: #9ACD32; font-size: 0.8rem; margin-top: 5px;'>"
        "Le canal 'reprise_erp' présente un taux d'invalides nettement supérieur aux autres (~59 % contre ~43 %).<br>"
        "Cela s'explique par le fait qu'il s'agit de clients anciens importés de l'ancien logiciel sans vérification préalable."
        "</div>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
    <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(255, 75, 75, 0.6), transparent); margin: 35px 0;'></div>
    """,
    unsafe_allow_html=True
)
    
    # 2. Par pays déclaré
    taux_pays = taux_invalides(selection, "pays_declare")
    fig_pays = px.bar(
        taux_pays,
        x="taux d'erreur (%)",
        y="pays_declare",
        orientation="h",
        text="taux d'erreur (%)",
        title="Part de numéros invalides par pays déclaré",
    )
    st.plotly_chart(fig_pays)
        
    st.markdown(
        "<div style='text-align: center; color: #9ACD32; font-size: 0.8rem; margin-top: 5px;'>"
        "Hormis les codes hors Union Européenne et les codes erronés, l'analyse par pays montre que le taux d'invalides reste élevé partout, confirmant que le problème de qualité provient des numéros de TVA saisis."
        "</div>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
    <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(255, 75, 75, 0.6), transparent); margin: 35px 0;'></div>
    """,
    unsafe_allow_html=True
)
    
    # 3. Temps de réponse VIES (médiane)
    temps_pays = (
        selection.dropna(subset=["temps_reponse_ms"])
        .groupby("pays_declare")["temps_reponse_ms"]
        .median()
        .round(0)
        .sort_values()
        .reset_index(name="temps_median_ms")
    )
    fig_temps = px.bar(
        temps_pays,
        x="temps_median_ms",
        y="pays_declare",
        orientation="h",
        text="temps_median_ms",
        title="Temps de réponse médian par pays (en millisecondes)",
        labels={"temps_median_ms": "Temps médian (ms)", "pays_declare": "Pays"},
    )
    st.plotly_chart(fig_temps)
    
    st.markdown(
        "<div style='text-align: center; color: #9ACD32; font-size: 0.8rem; margin-top: 5px;'>"
        "Le temps de réponse des numéros de TVA italiens présente une médiane supérieure d'environ 120 ms par rapport aux autres pays."
        "</div>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
    <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(255, 75, 75, 0.6), transparent); margin: 35px 0;'></div>
    """,
    unsafe_allow_html=True
)
    
    # 4. Nombre de non tranchés par pays
    non_tranche_pays = (
        selection[selection["statut"] == "non_tranche"]
        .groupby("pays_declare")
        .size()
        .sort_values()
        .reset_index(name="nb_non_tranches")
    )
    fig_non_tranche = px.bar(
        non_tranche_pays,
        x="nb_non_tranches",
        y="pays_declare",
        orientation="h",
        text="nb_non_tranches",
        title="Nombre de numéros non tranchés par pays",
        labels={"nb_non_tranches": "Nombre de non tranchés", "pays_declare": "Pays"},
    )
    st.plotly_chart(fig_non_tranche)
    
    st.markdown(
        "<div style='text-align: center; color: #9ACD32; font-size: 0.8rem; margin-top: 5px;'>"
        "L'Italie concentre à elle seule plus de la moitié des cas non tranchés (121 cas sur 213), "
        "ce qui est cohérent avec les temps de réponse et timeouts observés sur ce pays."
        "</div>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
    <div style='height: 2px; background: linear-gradient(90deg, transparent, rgba(255, 75, 75, 0.6), transparent); margin: 35px 0;'></div>
    """,
    unsafe_allow_html=True
)