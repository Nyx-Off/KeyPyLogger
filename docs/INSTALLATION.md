# 📦 Guide d'Installation - KeyPyLogger

## Prérequis Système

### Windows
- Windows 7 ou supérieur
- Python 3.7+ installé
- Connexion Internet

### Linux
- Distribution récente (Ubuntu 20.04+, Debian 11+, etc.)
- Python 3.7+ installé
- Environnement graphique (X11 ou Wayland)
- Connexion Internet

---

## Installation Python

### Windows

**Vérifier si Python est installé** :
```powershell
python --version
```

**Si Python n'est pas installé** :
1. Télécharger depuis [python.org](https://www.python.org/downloads/)
2. Installer (cocher "Add Python to PATH")
3. Redémarrer le terminal

### Linux

**Ubuntu/Debian** :
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Fedora** :
```bash
sudo dnf install python3 python3-pip
```

**Arch** :
```bash
sudo pacman -S python python-pip
```

---

## Installation de KeyPyLogger

### Méthode 1 : Git Clone (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/Nyx-Off/KeyPyLogger.git
cd KeyPyLogger

# Installer les dépendances
pip install -r requirements.txt
```

### Méthode 2 : Téléchargement ZIP

1. Télécharger le ZIP depuis GitHub
2. Extraire l'archive
3. Ouvrir un terminal dans le dossier
4. `pip install -r requirements.txt`

---

## Installation des Dépendances

### Installation Basique

```bash
pip install -r requirements.txt
```

### Installation Manuelle

```bash
pip install pynput>=1.7.6
pip install requests>=2.31.0
pip install pyinstaller>=6.0.0  # Optionnel
```

### Vérifier l'Installation

```bash
python -c "import pynput, requests; print('OK')"
```

Si vous voyez "OK", l'installation est réussie.

---

## Configuration des Permissions (Linux)

### Méthode 1 : Groupe input (Recommandée)

```bash
# Ajouter l'utilisateur au groupe input
sudo usermod -a -G input $USER

# Vérifier
groups

# Déconnexion/reconnexion pour appliquer
```

### Méthode 2 : Exécuter avec sudo

```bash
sudo python3 src/linux/keylogger_linux.py
```

---

## Installation dans un Environnement Virtuel (Recommandé)

### Windows

```powershell
# Créer l'environnement
python -m venv venv

# Activer
venv\Scripts\activate

# Installer
pip install -r requirements.txt
```

### Linux

```bash
# Créer l'environnement
python3 -m venv venv

# Activer
source venv/bin/activate

# Installer
pip install -r requirements.txt
```

---

## Vérification de l'Installation

### Test Complet

```bash
python tools/test_webhook.py
```

Ce script vérifie :
- ✅ Importation de pynput
- ✅ Importation de requests
- ✅ Connexion webhook Discord
- ✅ Listener clavier

---

## Problèmes Courants

### "pip: command not found"

**Windows** :
```powershell
python -m pip install -r requirements.txt
```

**Linux** :
```bash
sudo apt install python3-pip
```

### "Permission denied" lors de l'installation

```bash
pip install --user -r requirements.txt
```

### Erreur avec pyinstaller sur Python 3.14

```bash
pip install --upgrade pyinstaller
```

---

## Installation Complète - Étape par Étape

### Windows

```powershell
# 1. Installer Python depuis python.org
# 2. Ouvrir PowerShell
cd C:\Users\VotreNom\Documents

# 3. Cloner
git clone https://github.com/Nyx-Off/KeyPyLogger.git
cd KeyPyLogger

# 4. Installer
pip install -r requirements.txt

# 5. Vérifier
python tools/test_webhook.py
```

### Linux (Ubuntu/Debian)

```bash
# 1. Installer Python et Git
sudo apt update
sudo apt install python3 python3-pip git

# 2. Cloner
cd ~
git clone https://github.com/Nyx-Off/KeyPyLogger.git
cd KeyPyLogger

# 3. Installer
pip3 install -r requirements.txt

# 4. Configurer permissions
sudo usermod -a -G input $USER

# 5. Déconnexion/reconnexion puis vérifier
python3 tools/test_webhook.py
```

---

## Installation pour Développement

### Avec environnement virtuel

```bash
# Cloner
git clone https://github.com/Nyx-Off/KeyPyLogger.git
cd KeyPyLogger

# Créer venv
python3 -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

# Installer en mode éditable
pip install -e .
pip install -r requirements.txt

# Installer outils de développement
pip install pytest black flake8
```

---

## Désinstallation

### Supprimer le projet

```bash
cd ..
rm -rf KeyPyLogger  # Linux
rmdir /s KeyPyLogger  # Windows
```

### Désinstaller les dépendances

```bash
pip uninstall pynput requests pyinstaller
```

---

## Mise à Jour

```bash
cd KeyPyLogger
git pull origin main
pip install --upgrade -r requirements.txt
```

---

## Installation Hors Ligne

Si vous n'avez pas Internet sur la machine cible :

```bash
# Sur machine avec Internet :
pip download -r requirements.txt -d packages/

# Copier le dossier packages/ vers la machine cible

# Sur machine cible :
pip install --no-index --find-links=packages/ -r requirements.txt
```

---

**Installation terminée ! → Voir [QUICK_START.md](../QUICK_START.md) pour l'utilisation**
