# 🤖 Guide de Démarrage - Bot Discord (Préfixe : `+`)

Ce projet contient un bot Discord de modération et d'utilité codé en Python.

---

## 📋 Prérequis

Pour lancer ce bot, vous devez installer **Python** (version 3.8 ou supérieure conseillée) sur votre ordinateur.

---

## 🛠️ Étape 1 : Créer le Bot sur Discord (Developer Portal)

Pour faire fonctionner le bot, vous devez récupérer son **Token d'authentification** :

1. Rendez-vous sur le [Discord Developer Portal](https://discord.com/developers/applications).
2. Cliquez sur **New Application** (Nouvelle Application) en haut à droite. Donnez un nom à votre application et validez.
3. Dans le menu de gauche, allez sur l'onglet **Bot** et cliquez sur **Add Bot** (Ajouter un Bot).
4. **Très Important (Intents) :**
   - Faites défiler la page vers le bas jusqu'à la section **Privileged Gateway Intents**.
   - Activez les options suivantes (cochez les cases) :
     - **Presence Intent**
     - **Server Members Intent** (Nécessaire pour kick/ban)
     - **Message Content Intent** (Nécessaire pour lire le préfixe `+`)
   - Cliquez sur **Save Changes** (Sauvegarder les modifications) en bas.
5. Remontez un peu sur la page du bot et cliquez sur **Reset Token** pour obtenir votre jeton secret. Copiez-le et gardez-le en sécurité !

---

## 🔗 Étape 2 : Inviter le Bot sur votre Serveur

1. Toujours sur le Developer Portal, allez dans l'onglet **OAuth2** puis **URL Generator**.
2. Dans la section **Scopes**, cochez la case **bot**.
3. Dans la section **Bot Permissions** qui apparaît en dessous, cochez :
   - **Administrator** (ou manuellement : *Manage Messages*, *Kick Members*, *Ban Members*, *Send Messages*, *Embed Links*, etc.).
4. Copiez le lien généré tout en bas de la page et collez-le dans votre navigateur pour inviter le bot sur votre serveur.

---

## ⚙️ Étape 3 : Configuration locale

1. Ouvrez le fichier [.env](file:///C:/Users/Nzomd/.gemini/antigravity/scratch/discord-bot/.env) présent dans ce dossier.
2. Remplacez `VOTRE_TOKEN_ICI` par le Token que vous avez copié à l'Étape 1.
3. Enregistrez le fichier.

---

## 🚀 Étape 4 : Installation et Lancement

1. Ouvrez votre terminal (PowerShell ou Invite de commandes) dans le dossier du bot.
2. Installez les packages nécessaires avec la commande :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez le bot avec la commande :
   ```bash
   python bot.py
   ```

---

## 🎮 Commandes du Bot

Une fois connecté, le bot répond aux commandes suivantes :

*   `+help` : Affiche l'aide et les commandes.
*   `+embed Titre | Description | #CouleurHex | URL_Image` : Envoie un message sous forme d'embed personnalisé.
    *   *Exemple :* `+embed Annonce | Rendez-vous ce soir à 20h pour l'événement ! | #ff0000`
*   `+clear <nombre>` : Supprime `<nombre>` de messages dans le salon actuel (ex: `+clear 20`).
*   `+kick <@membre> [raison]` : Expulse un membre du serveur.
*   `+ban <@membre> [raison]` : Bannit définitivement un membre.
*   `+tempban <@membre> <durée> [raison]` : Bannit temporairement un membre.
    *   *Exemples de durée :* `30s` (30 secondes), `15m` (15 minutes), `2h` (2 heures), `1d` (1 jour).
    *   *Exemple :* `+tempban @Utilisateur 2h Spam de messages`
