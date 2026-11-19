# Brief — Un tableau de bord TVA avec Streamlit

# Fiche du brief

| Durée | 1 jour et demi : le jour 1 entier et le matin du jour 2 (environ 8 h 30 de travail, plus la démonstration) |
| :---- | :---- |
| Niveau | Débutant. Aucune connaissance de Streamlit n'est nécessaire |
| Modalité | Individuel |
| Technologies | Python 3.11 à 3.14, pandas, Streamlit, Plotly, Git/GitHub |
| Données | data/resultats\_vies.csv, fourni dans le starter kit |

# Compétences visées

Référentiel RNCP 38616, option Data Analyse. Niveau 1 (imiter) : le code de départ et les exemples sont fournis.

* **C16 — Indicateurs clés.** Vous calculez les chiffres qui disent où en est le référentiel.  
* **C17 — Visualisations accessibles.** Vos graphiques se lisent sans avoir besoin des couleurs.  
* **C18 — Tableau de bord.** Vous construisez une application web filtrable.  
* **C15 — Présentation.** Vous montrez votre application comme devant la directrice financière.

# Contexte

La directrice financière de Meridian Distribution a lu votre note sur les numéros de TVA. Elle veut maintenant suivre le référentiel elle-même, dans son navigateur, sans attendre un nouveau rapport.

Vous allez lui construire une page web avec **Streamlit**, une bibliothèque Python qui transforme un script en application web, sans HTML ni JavaScript.

Les résultats de la campagne VIES vous sont fournis, déjà propres, dans *`data/resultats_vies.csv`*. Un fichier `app.py` est déjà commencé : vous le complétez étape par étape, en suivant les `TODO`.

# Avant de commencer

Le starter kit contient :

* `app.py` : l'application déjà commencée, à compléter en suivant les `TODO` ;  
* `data/resultats_vies.csv` : les données ;  
* `data/LISEZMOI.md` : le sens de chaque colonne et les chiffres à retrouver ;  
* `requirements.txt`, `.gitignore` et `.streamlit/config.toml` : déjà prêts, n'y touchez pas.

Lisez `data/LISEZMOI.md`. Il explique chaque colonne et donne **les chiffres que votre application doit retrouver**. Vous vous en servirez à chaque étape pour vérifier votre travail.

Deux choses à savoir sur `app.py` avant de commencer :

* **Les `TODO` portent chacun un nom et ne sont pas dans l'ordre du fichier.** Les filtres (étape 3\) et le texte d'en-tête (étape 6\) sont en haut, parce qu'ils doivent passer avant le reste. Chaque étape du brief donne le nom de son TODO : cherchez-le avec Ctrl+F (Cmd+F sur Mac), par exemple TODO CHIFFRES.  
* **`selection`, ce sont les données filtrées.** Tant que vous n'avez pas fait l'étape 3, `selection` contient toutes les lignes, exactement comme `df`. Utilisez toujours `selection` dans vos calculs, jamais `df` : c'est ce qui fera réagir la page aux filtres plus tard.

# Déroulé

## Jour 1, matin

### Étape 0 — Installer, lancer et relier à GitHub

1. Créez un dossier `dashboard-tva` et copiez-y tout le contenu du starter kit, y compris le dossier caché `.streamlit`. Pour voir les fichiers cachés : sur Mac, appuyez sur Cmd+Maj+. dans le Finder ; sous Windows, dans l'Explorateur, menu Affichage \> Afficher \> Éléments masqués.  
2. Ouvrez un terminal dans ce dossier.  
3. Créez l'environnement virtuel et installez les bibliothèques :  
   `python3 -m venv .venv`  
   `source .venv/bin/activate`  
   `pip install -r requirements.txt`  
   Sous Windows, la deuxième ligne devient `.venv\Scripts\activate`.   
   L'environnement virtuel est une installation de Python propre à ce projet. Vous savez qu'il est activé quand `(.venv)` apparaît au début de la ligne du terminal. Le jour 2, il n'y a rien à réinstaller : ouvrez un terminal dans le dossier et retapez seulement la ligne `source .venv/bin/activate`.  
4. Lancez l'application :  
   `streamlit run app.py`  
   Votre navigateur s'ouvre sur une page « Qualité du référentiel TVA ». Laissez ce terminal ouvert : à chaque enregistrement de `app.py`, la page se met à jour toute seule.  
5. Créez le dépôt Git et faites un premier commit. Ouvrez un **second** terminal dans le dossier (le premier fait tourner l'application), puis :  
   `git init`  
   `git add .`  
   `git commit -m "Starter kit"`  
6. Reliez ce dépôt à GitHub. Sur github.com, créez un nouveau dépôt public nommé `dashboard-tva`, **sans** cocher « Add a README » (le dépôt doit être vide). Puis, dans le terminal, en remplaçant `VOTRE-PSEUDO` par votre nom d'utilisateur GitHub :  
   `git branch -M main`  
   `git remote add origin https://github.com/VOTRE-PSEUDO/dashboard-tva.git`  
   `git push -u origin main`  
   1. `git branch -M main` nomme la branche principale `main` ;  
   2. `git remote add origin …` indique à Git l'adresse de votre dépôt GitHub, sous le nom `origin` ;  
   3. `git push -u origin main` envoie vos commits sur GitHub. Le `-u` retient la destination : les fois suivantes, `git push` suffit.

   Si Git répond `remote origin already exists`, l'adresse est déjà enregistrée : corrigez-la avec `git remote set-url origin https://github.com/VOTRE-PSEUDO/dashboard-tva.git`.

7. Dans la suite du brief, chaque « Faites un commit » veut dire :  
   `git add .`  
   `git commit -m "Étape 1 : chiffres clés"`  
   `git push`  
   en adaptant le message à l'étape.

**Vérification** : la page affiche « Numéros : 10000 », et votre dépôt GitHub montre vos fichiers.

### Étape 1 — Les quatre chiffres clés (1 h 30\)

Le premier chiffre, le nombre total de numéros, est déjà affiché. Dans `app.py`, au `TODO CHIFFRES`, ajoutez les trois autres : le nombre de **valides**, d'**invalides** et de **non tranchés**, chacun avec son pourcentage.

Aide :

`valides = (selection["statut"] == "valide").sum()`  
`col2.metric("Valides", valides, f"{valides / total:.1%} du total", delta_color="off")`

* La première ligne compte les lignes dont le statut vaut `"valide"`.  
* `:.1%` écrit un nombre en pourcentage avec un chiffre après la virgule (0,515 devient 51.5%).  
* `delta_color="off"` affiche le pourcentage en gris. Sans lui, Streamlit l'affiche en vert avec une flèche, comme une hausse.

Faites de même pour `invalide` dans `col3` et `non_tranche` dans `col4`.

**Vérification** : 5 149 valides (51,5 %), 4 638 invalides (46,4 %), 213 non tranchés (2,1 %).

Faites un commit.

### Étape 2 — L'entonnoir (1 h)

L'entonnoir montre combien de numéros restent à chaque étape avant l'envoi à VIES.

Au `TODO ENTONNOIR` :

1. comptez les lignes dont `etape_rejet` vaut `"absent"`, puis `"doublon"`, puis `"structure"` (trois nombres) ;  
2. soustrayez-les de `total` un par un, pour obtenir le nombre de numéros qui restent après chaque étape. Il n'y a pas de tableau à filtrer, seulement des soustractions ;  
3. mettez ces quatre nombres dans un petit tableau pandas et affichez-le avec `px.funnel`.

Aide (complétez les deux lignes qui contiennent `???`) :

`absents = (selection["etape_rejet"] == "absent").sum()`  
`doublons = ???      # même chose avec "doublon"`  
`structure = ???     # même chose avec "structure"`  
`entonnoir = pd.DataFrame({`  
    `"étape": ["Référentiel", "Sans les absents", "Sans les doublons", "Envoyés à VIES"],`  
    `"numéros": [total,`  
                `total - absents,`  
                `total - absents - doublons,`  
                `total - absents - doublons - structure],`  
`})`  
`fig = px.funnel(entonnoir, x="numéros", y="étape",`  
                `title="Du référentiel aux numéros envoyés à VIES")`  
`st.plotly_chart(fig)`

**Vérification** : 10 000 → 9 778 → 9 302 → 5 802\.

Faites un commit.

## Jour 1, après-midi

### Étape 3 — Les filtres (1 h 30\)

Le filtre « Pays déclaré » est déjà écrit en haut de `app.py`. Lisez-le, puis :

* **TODO FILTRE\_CANAL** : sur le même modèle, ajoutez un filtre « Canal de saisie » sur la colonne `source_saisie` ;  
* **TODO FILTRE\_PERIODE** : ajoutez un filtre « Période de saisie ». Aide :  
  `debut, fin = st.sidebar.slider(`  
      `"Période de saisie",`  
      `min_value=df["date_saisie"].min().date(),`  
      `max_value=df["date_saisie"].max().date(),`  
      `value=(df["date_saisie"].min().date(), df["date_saisie"].max().date()),`  
      `format="DD/MM/YYYY",`  
  `)`  
* **TODO APPLIQUER\_FILTRES** : appliquez ces deux filtres à `selection`, sur le modèle du filtre pays. Pour la période :  
  `selection = selection[selection["date_saisie"].dt.date.between(debut, fin)]`

Les chiffres clés et l'entonnoir utilisent déjà `selection` : ils réagissent tout seuls.

**Vérification** (remettez les autres filtres à zéro entre deux essais) :

* avec le seul pays `FR` : 974 numéros, dont 555 valides ;  
* avec le seul canal `reprise_erp` : 2 071 numéros, dont 1 219 invalides ;  
* avec le pays `FR` **et** le canal `reprise_erp` en même temps : 197 numéros, dont 93 valides. Si vous trouvez 2 071, vos filtres ne se cumulent pas : relisez la règle ci-dessus.

Faites un commit.

### Étape 4 — D'où viennent les erreurs ? (1 h)

Au `TODO GRAPHIQUES`, faites deux graphiques en barres horizontales : la **part de numéros invalides** par canal de saisie, puis par pays déclaré.

Le calcul est déjà écrit pour vous : c'est la fonction `taux_invalides`, en haut de `app.py`. Lisez son commentaire, puis affichez son résultat avec `st.dataframe(taux_invalides(selection, "source_saisie"))` pour voir ce qu'elle renvoie.

Aide pour le premier graphique :

`taux = taux_invalides(selection, "source_saisie")`  
`fig = px.bar(taux, x="taux d'erreur (%)", y="source_saisie", orientation="h",`  
             `text="taux d'erreur (%)", title="Part de numéros invalides par canal de saisie")`  
`st.plotly_chart(fig)`

Faites le second en remplaçant `source_saisie` par `pays_declare` (et non `pays`). Une fois que vous avez compris ce que renvoie `taux_invalides`, supprimez le `st.dataframe` de test.

Ensuite, **regardez vos graphiques**. Un canal sort nettement du lot : lequel ? Écrivez sous les graphiques, avec `st.caption`, une phrase qui le dit et propose une explication. Le `LISEZMOI.md` vous dit ce que recouvre chaque canal.

**Vérification** : le canal `reprise_erp` est autour de 59 %, les autres autour de 43 %.

Faites un commit.

## Jour 2, matin

### Étape 5 — Les numéros à traiter (1 h)

Au `TODO A_TRAITER`, recopiez et complétez : 

`# 1. Garder les lignes dont le statut n'est pas "valide" (!= veut dire « différent de »)`  
`a_traiter = selection[selection["statut"] != "valide"].copy()`

`# 2. Ajouter une colonne "action" : .map remplace chaque statut par le texte associé`  
`a_traiter["action"] = a_traiter["statut"].map({`  
    `"invalide": "Demander un nouveau numéro au client",`  
    `"non_tranche": "Revérifier sur VIES avant la prochaine facture",`  
`})`

`# 3. Afficher le nombre et le tableau, avec les colonnes utiles pour la comptabilité`  
`colonnes = ["raison_sociale", "numero_saisi", "pays_declare", "statut", "motif", "action"]`  
`st.write(f"{len(a_traiter)} numéros demandent une action.")`  
`st.dataframe(a_traiter[colonnes], hide_index=True)`

`# 4. Le bouton de téléchargement`  
`st.download_button(`  
    `"Télécharger la liste",`  
    `a_traiter[colonnes].to_csv(index=False, sep=";").encode("utf-8-sig"),`  
    `file_name="numeros_a_traiter.csv",`  
`)`

Le `.copy()` de la première ligne évite un avertissement orange de pandas dans le terminal. Le séparateur `;` et l'encodage `utf-8-sig` permettent d'ouvrir le fichier proprement dans Excel, accents compris.

**Vérification** : sans filtre, 4 851 numéros sont à traiter. Le fichier téléchargé s'ouvre dans Excel avec les accents.

Faites un commit.

### Étape 6 — Rendre la page lisible par tous (1 h)

1. **TODO AIDE** : en haut de la page, écrivez une ou deux phrases qui expliquent à la directrice financière ce qu'elle regarde et comment utiliser les filtres.  
2. **TODO DATE\_REGLE** : avec `st.info`, affichez la date de la dernière vérification VIES et rappelez la règle : un numéro non tranché ne doit pas être facturé hors taxe tant qu'il n'a pas été revérifié. Aide :  
   `derniere = df["date_verification"].max()`  
   `st.info(f"Dernière vérification VIES : {derniere:%d/%m/%Y à %H:%M}. Règle : ...")`  
   Ici, on utilise bien `df` et non `selection` : la date de la campagne ne dépend pas des filtres.  
3. Vérifiez vos graphiques :  
   1. chaque barre affiche sa valeur (`text=`), donc on peut les lire sans les couleurs ;  
   2. chaque graphique a un titre qui dit ce qu'il montre ;  
   3. zoomez à 200 % dans le navigateur (Ctrl et \+ ou Cmd et \+) : tout doit rester lisible.

Faites un commit.

### Étape 7 — Capture d'écran (15 min)

1. Sans filtre actif, faites une capture d'écran de votre application (Mac : Cmd+Maj+4 ; Windows : touche Windows+Maj+S).  
2. Enregistrez-la dans le dossier `dashboard-tva` sous le nom `capture.png`.  
3. Faites un dernier commit, avec son `git push`.

**Vérification** : sur la page GitHub du dépôt, le fichier `capture.png` apparaît et s'ouvre.

### Démonstration (fin de matinée)

5 minutes par personne. Vous présentez l'application comme devant la directrice financière, en trois temps :

1. les chiffres clés ;  
2. un filtre qui montre d'où viennent les erreurs ;  
3. la liste des numéros à traiter.

Un filtre est ensuite choisi au hasard pour vérifier vos chiffres.

# Pour aller plus loin (si vous avez fini)

* Un graphique des temps de réponse VIES (`temps_reponse_ms`) avec la médiane.  
* Un graphique du nombre de non tranchés par pays : un pays ressort-il ?  
* Ranger la page en onglets avec `st.tabs`.  
* Déployer l'application sur Streamlit Community Cloud.

# Livrables

Le lien de votre dépôt GitHub, posté sur la plateforme. Il doit contenir :

* `app.py` complété ;  
* `requirements.txt` et `data/` ;  
* `capture.png`, une capture d'écran de l'application ;  
* au moins un commit par étape.

# Ressources

* Les bases de Streamlit : [https\://docs.streamlit.io/get-started/fundamentals/main-concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts)  
* `st.metric` : [https\://docs.streamlit.io/develop/api-reference/data/st.metric](https://docs.streamlit.io/develop/api-reference/data/st.metric)  
* `st.multiselect` : [https\://docs.streamlit.io/develop/api-reference/widgets/st.multiselect](https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect)  
* `st.download_button` : [https\://docs.streamlit.io/develop/api-reference/widgets/st.download\_button](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button)  
* Plotly Express, barres : [https\://plotly.com/python/bar-charts/](https://plotly.com/python/bar-charts/)