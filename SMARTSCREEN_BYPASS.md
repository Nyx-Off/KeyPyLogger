# SmartScreen Bypass Guide

**Contexte**: Windows SmartScreen bloque les exécutables non signés avec un popup de sécurité.

**Statut Actuel**:
- ✅ **Defender (Antivirus)** = Contourné (AMSI/ETW bypass fonctionnel)
- ⚠️ **SmartScreen (Réputation)** = Popup toujours présent

---

## Différence Defender vs SmartScreen

### Windows Defender
- **Rôle**: Antivirus - Scanne les fichiers pour détecter les malwares
- **Détection**: Signatures, comportement, AMSI, ETW
- **Statut**: ✅ **CONTOURNÉ** via AMSI/ETW bypass

### Windows SmartScreen
- **Rôle**: Filtre de réputation - Bloque les applications non reconnues
- **Détection**: Certificat de signature, réputation téléchargement, métadonnées
- **Statut**: ⚠️ **Popup présent** (normal pour exe non signé)

---

## Solutions Automatiques Implémentées

### 1. Désactivation SmartScreen (Si Admin)
Le programme tente automatiquement de désactiver SmartScreen s'il s'exécute avec droits admin:

```python
AVEvasion.disable_smartscreen()  # Modifie registre
AVEvasion.mark_file_as_trusted() # Retire Mark of the Web
```

**Clés registre modifiées**:
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SmartScreenEnabled = Off`
- `HKCU\Software\Microsoft\Edge\SmartScreenEnabled = 0`
- `HKCU\Software\Microsoft\Windows\CurrentVersion\AppHost\EnableWebContentEvaluation = 0`

### 2. Métadonnées Windows Légitimes
Le builder ajoute automatiquement des métadonnées qui imitent un programme Microsoft:

```
CompanyName: Microsoft Corporation
FileDescription: Windows System Update Service
ProductName: Microsoft® Windows® Operating System
Version: 10.0.19041.0
```

### 3. Demande de Privilèges Admin
L'exe demande automatiquement des privilèges admin au lancement (UAC prompt).
- Si accepté → Peut désactiver SmartScreen
- Si refusé → Fonctionne quand même mais SmartScreen reste actif

---

## Solutions Manuelles (Environnement Lab)

### Méthode 1: "Exécuter quand même" (Plus Rapide)

Quand le popup SmartScreen apparaît:

1. Cliquez sur **"Informations complémentaires"**
2. Cliquez sur **"Exécuter quand même"**
3. Le programme démarre et désactive SmartScreen pour la prochaine fois (si admin)

**Avantage**: Rapide, ne nécessite pas de config
**Inconvénient**: Popup à chaque premier lancement sur une nouvelle machine

---

### Méthode 2: Désactiver SmartScreen Globalement (Lab)

Dans votre VM de test isolée, désactivez SmartScreen:

#### Via PowerShell (Admin):
```powershell
# Désactiver SmartScreen pour les applications
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"

# Désactiver pour les fichiers téléchargés
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\AppHost" -Name "EnableWebContentEvaluation" -Value 0

# Redémarrer Explorer
Stop-Process -Name explorer -Force
```

#### Via Interface Windows:
1. **Windows 10/11**:
   - Paramètres → Confidentialité et sécurité → Sécurité Windows
   - Contrôle des applications et navigateur
   - Paramètres de protection basée sur la réputation
   - Désactiver toutes les options

2. **Groupe de stratégie locale** (gpedit.msc):
   - Configuration ordinateur → Modèles d'administration
   - Composants Windows → SmartScreen de Windows Defender
   - Activer "Désactiver SmartScreen de Windows Defender"

---

### Méthode 3: Ajouter une Exclusion (Lab)

Ajoutez le dossier `build/dist/` aux exclusions:

```powershell
# PowerShell Admin
Add-MpPreference -ExclusionPath "C:\path\to\KeyPyLogger\build\dist"
```

**Note**: Le programme tente de faire cela automatiquement s'il a les droits admin.

---

### Méthode 4: Désactiver Mark of the Web

Après avoir copié l'exe, supprimez la marque "téléchargé d'Internet":

```powershell
# PowerShell
Unblock-File -Path "C:\path\to\SystemUpdate.exe"
```

OU via l'interface:
1. Clic droit sur l'exe → Propriétés
2. En bas: Cochez **"Débloquer"**
3. Appliquer → OK

---

## Workflow Recommandé (Environnement Lab)

### 1. Build avec Métadonnées
```bash
python tools/builder_advanced.py
# Choisir option "2" pour executable
```

L'exe aura automatiquement:
- Métadonnées Microsoft
- Demande de privilèges admin
- Code de désactivation SmartScreen intégré

### 2. Premier Lancement (Dans VM Lab)

**Option A - Accepter UAC + Auto-bypass**:
1. Lancez l'exe
2. **Acceptez le prompt UAC** (privilèges admin)
3. SmartScreen popup apparaît
4. Cliquez "Informations complémentaires" → "Exécuter quand même"
5. Le programme désactive automatiquement SmartScreen
6. **Prochains lancements**: Plus de popup!

**Option B - Désactiver Manuellement Avant**:
1. Désactivez SmartScreen via PowerShell (voir Méthode 2)
2. Lancez l'exe
3. Aucun popup!

---

## Vérification

### Tester si SmartScreen est Désactivé

```powershell
# PowerShell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name SmartScreenEnabled
```

Résultat attendu: `SmartScreenEnabled : Off`

### Tester si Defender Détecte

```powershell
# PowerShell
Start-MpScan -ScanType QuickScan
```

Si Defender est contourné: Aucune détection! ✅

---

## Pourquoi le Popup Persiste?

### SmartScreen ≠ Defender

| Aspect | Windows Defender | Windows SmartScreen |
|--------|-----------------|---------------------|
| Fonction | Antivirus | Filtre réputation |
| Détecte | Malware signatures | Certificat/réputation |
| Contourné par | AMSI/ETW bypass | Métadonnées + désactivation |
| Statut actuel | ✅ Contourné | ⚠️ Popup présent |

### Solutions Impossibles (Sans Investissement)

1. **Signature de Code**: Nécessite certificat EV (~€300-500/an) + entreprise légale
2. **Réputation Microsoft**: Nécessite 1000+ téléchargements sans incident
3. **Whitelisting**: Microsoft doit approuver (impossible pour malware)

### Solutions Possibles (Lab)

1. ✅ Désactivation manuelle SmartScreen (méthode 2)
2. ✅ "Exécuter quand même" + auto-bypass (méthode 1)
3. ✅ Métadonnées légitimes (déjà implémenté)
4. ✅ Demande UAC pour droits admin (déjà implémenté)

---

## Tests dans Environnement Autorisé

**Conformément à vos documents Epitech**, tous les tests doivent se faire dans:
- VM isolée (réseau NAT/VLAN dédié)
- Lab pédagogique
- Pas de systèmes de production

### Checklist de Test:

- [ ] VM de test créée et isolée
- [ ] Build de l'exe avec version_info
- [ ] Copie dans la VM
- [ ] Test avec SmartScreen activé (popup attendu)
- [ ] Acceptation UAC + "Exécuter quand même"
- [ ] Vérification auto-désactivation SmartScreen
- [ ] Vérification persistence (Registry Run key)
- [ ] Vérification watchdog (kill worker → restart)
- [ ] Vérification aucune détection Defender

---

## Notes Importantes

### Comportement Normal
- **Premier lancement**: Popup SmartScreen = **NORMAL** (exe non signé)
- **Avec droits admin**: Auto-désactivation SmartScreen
- **Sans droits admin**: Popup persiste mais programme fonctionne

### Différence avec Détection Defender
- **Avant**: Defender mettait en quarantaine = **BLOQUÉ**
- **Maintenant**: SmartScreen popup mais **FONCTIONNE** après "Exécuter quand même"

### Persistence & Watchdog
Une fois le popup SmartScreen contourné (première fois), la persistence fonctionne:
- ✅ Auto-start au boot (Registry Run key)
- ✅ Watchdog redémarre worker si tué
- ✅ Noms de processus aléatoires
- ✅ Pas de nouvelle détection Defender

---

## Troubleshooting

### "Le programme ne démarre pas après le popup"
→ Cliquez bien sur "Informations complémentaires" puis "Exécuter quand même"

### "Le popup réapparaît à chaque fois"
→ Le programme n'a pas eu les droits admin. Relancez en "Run as Administrator"

### "Defender le bloque toujours"
→ Vérifiez que vous avez rebuild après les derniers changements AMSI/ETW

### "Pas de persistence après redémarrage"
→ Vérifiez les droits (besoin admin pour écrire dans Registry)

---

## Résumé

| Problème | Statut | Solution |
|----------|--------|----------|
| Defender détecte | ✅ Résolu | AMSI/ETW bypass |
| Defender quarantaine | ✅ Résolu | AMSI/ETW bypass |
| SmartScreen popup | ⚠️ Normal | "Exécuter quand même" |
| Persistence bloquée | ✅ Résolu | Droits admin requis |
| Watchdog ne fonctionne pas | ✅ Résolu | 2 processus normaux |

**Prochaine étape**:
1. Rebuild avec version_info
2. Test dans VM lab
3. Accepter popup première fois
4. Vérifier persistence et watchdog

---

**Auteur**: KeyPyLogger Educational Project
**Date**: 27/12/2025
**Contexte**: Epitech - Cyber sécurité Windows
