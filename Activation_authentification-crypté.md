# Note d'intention : Système d'authentification sécurisée et cryptage des mots de passe sous Streamlit

## 🎯 Objectif
Mettre en place un accès restreint par identifiant et mot de passe haché afin de protéger les données sensibles et bloquer l'accès aux onglets de l'application Streamlit aux utilisateurs non authentifiés.

---

## 🛠️ Technologies et Librairies recommandées
* **`streamlit-authenticator`** (ou gestion native via `st.session_state` et `bcrypt`) : Pour gérer l'interface de login et la session utilisateur.
* **`bcrypt`** (ou `hashlib` / `argon2`) : Pour le cryptage (hachage et salage) des mots de passe. Les mots de passe ne sont **jamais** stockés en clair.
* **`st.secrets`** : Pour stocker de manière sécurisée les configurations et les hashs des utilisateurs (via le fichier `.streamlit/secrets.toml`).

---

## 📐 Architecture et Fonctionnement

1. **Stockage sécurisé (`secrets.toml`)** :
   Les identifiants et les hashs des mots de passe sont externalisés dans le gestionnaire de secrets de Streamlit :
   ```toml
   [credentials]
   usernames.admin.email = "admin@example.com"
   usernames.admin.name = "Administrateur"
   usernames.admin.password = "$2b$12$..." # Mot de passe haché avec bcrypt
   ```

2. **Garde-fou global dans le script principal (`app.py`)** :
   Vérification de l'état de connexion dès le lancement de l'application pour empêcher le chargement des pages et des données si l'utilisateur n'est pas authentifié :
   ```python
   import streamlit as st

   # Initialisation de l'état de session
   if "authentifie" not in st.session_state:
       st.session_state["authentifie"] = False

   if not st.session_state["authentifie"]:
       # Affichage du formulaire de login et arrêt de l'exécution du reste de l'app
       # ...
       st.stop()

   # Accès autorisé aux onglets et visualisations
   ```

---

## ⚠️ Limites sur le Cloud Public (ex: Streamlit Community Cloud)
* L'application hébergée possède une **URL publique**. Même si le contenu est protégé par un mot de passe, l'URL elle-même est accessible à tous.
* Pour un niveau de sécurité entreprise (SSO, OAuth2, annuaire interne), il est préférable d'héberger l'application en interne (via Docker sur un réseau privé, un VPN, ou une solution cloud d'entreprise).
