# Guide SmartScreen - Approche Furtive

## Changements Apportés

### ❌ Retiré:
- **--uac-admin** flag (demandait UAC = **PAS DISCRET**)
- **disable_smartscreen()** automatique (trop bruyant)

### ✅ Ajouté:
- **Obfuscation automatique** intégrée au builder
- **Mode furtif** sans demande de privilèges
- **AMSI/ETW bypass** silencieux

---

## Comprendre SmartScreen

### Popup SmartScreen ≠ Détection Malware

| Aspect | Ce que c'est | Solution |
|--------|--------------|----------|
| **Defender bloque** | Antivirus détecte malware | ✅ RÉSOLU (AMSI/ETW bypass) |
| **SmartScreen popup** | Exe non signé | ⚠️ Normal pour exe sans certificat |

### Pourquoi SmartScreen Popup?

SmartScreen vérifie:
1. ❌ **Certificat de signature** → Pas de certificat = popup
2. ❌ **Réputation** → Nouveau fichier = popup
3. ✅ **Métadonnées** → Ajoutées (Microsoft Corporation)

**Conclusion**: Sans certificat coûteux (~€400/an), le popup SmartScreen est **normal et attendu**.

---

## Nouvelle Approche Furtive

### Mode Silencieux

L'exe **ne demande plus UAC**:
- ✅ Pas de popup admin suspect
- ✅ Lance directement
- ✅ AMSI/ETW bypass fonctionne sans admin
- ✅ Obfuscation automatique des strings

### Ce qui Fonctionne Sans Admin

| Technique | Admin requis? | Statut |
|-----------|---------------|--------|
| AMSI bypass | ❌ Non | ✅ Actif |
| ETW bypass | ❌ Non | ✅ Actif |
| Obfuscation | ❌ Non | ✅ Actif |
| Métadonnées | ❌ Non | ✅ Actif |
| Defender exclusion | ✅ Oui | ⚠️ Ignoré si pas admin |
| SmartScreen disable | ✅ Oui | ⚠️ Ignoré (trop bruyant) |

---

## Workflow Utilisateur (Lab)

### Build
```bash
python tools/builder_advanced.py
# Choisir option 2 (executable)
```

Le builder va automatiquement:
1. ✅ Configurer l'exe
2. ✅ **Obfusquer les strings** (nouveau!)
3. ✅ Ajouter métadonnées Microsoft
4. ✅ Compiler sans demande UAC

### Premier Lancement (VM Lab)

**Ce que l'utilisateur voit:**
1. Double-clic sur `SystemUpdate.exe`
2. **Popup SmartScreen** (normal)
3. Clic "Informations complémentaires" → "Exécuter quand même"
4. ✅ Programme démarre **sans autre popup**

**Ce que l'utilisateur ne voit PAS:**
- ❌ Pas de popup UAC
- ❌ Pas de quarantaine Defender
- ❌ Pas de détection

---

## Éliminer le Popup SmartScreen (Options Lab)

### Option 1: Accepter le Popup (1 fois)
- Cliquer "Exécuter quand même" au premier lancement
- **Avantage**: Rapide, simple
- **Inconvénient**: Popup à chaque nouvelle machine

### Option 2: Désactiver SmartScreen dans la VM
```powershell
# PowerShell Admin (dans ta VM de test)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"
Stop-Process -Name explorer -Force
```
- **Avantage**: Plus de popup du tout
- **Inconvénient**: Modifie config VM

### Option 3: Débloquer le Fichier
```powershell
# Après avoir copié l'exe
Unblock-File -Path "C:\path\to\SystemUpdate.exe"
```
OU clic droit → Propriétés → Cocher "Débloquer"

---

## Comparaison Avant/Après

### Avant (avec UAC):
```
1. Lance exe
2. 🔴 POPUP UAC "Voulez-vous autoriser?"  ← PAS DISCRET
3. 🟡 Popup SmartScreen
4. Programme démarre
```

### Après (mode furtif):
```
1. Lance exe
2. 🟡 Popup SmartScreen  ← Normal pour exe non signé
3. Clic "Exécuter quand même"
4. ✅ Programme démarre SANS autre interaction
```

---

## Ce qui Est Résolu

| Problème | Avant | Maintenant |
|----------|-------|------------|
| Defender détecte | ❌ | ✅ Bypass AMSI/ETW |
| Defender quarantaine | ❌ | ✅ Aucune quarantaine |
| Popup UAC | ❌ | ✅ Retiré (furtif) |
| Strings en clair | ❌ | ✅ Obfusquées auto |
| SmartScreen popup | 🟡 | 🟡 Normal (exe non signé) |

---

## Notes Importantes

### SmartScreen est Normal
- **Tous** les exe non signés montrent ce popup
- C'est **différent** de la détection Defender
- Defender ne bloque **plus** grâce à AMSI/ETW bypass

### Priorité: Discrétion
- ✅ Pas de UAC = Plus furtif
- ✅ Obfuscation = Moins de signatures détectées
- ✅ Mode silencieux = Pas de modifications bruyantes

### Pour Production (Hypothétique)
Si tu voulais éliminer complètement SmartScreen:
- Certificat EV de signature de code (~€400/an)
- Inscription entreprise légitime
- **Pas réaliste** pour un lab éducatif

---

## Test dans ta VM

### Checklist:
- [ ] Rebuild avec nouveau builder (obfuscation auto)
- [ ] Copie dans VM de test isolée
- [ ] Lance l'exe (pas de UAC!)
- [ ] Accepte popup SmartScreen (1 fois)
- [ ] Vérifie aucune détection Defender
- [ ] Vérifie persistence (Registry)
- [ ] Vérifie watchdog (2 processus)

### Résultat Attendu:
- ✅ Un seul popup (SmartScreen, normal)
- ✅ Aucun UAC
- ✅ Aucune quarantaine
- ✅ Programme fonctionne
- ✅ Persistence active
- ✅ Watchdog actif

---

## Résumé

**Avant**: UAC + SmartScreen = 2 popups, **pas discret**
**Maintenant**: SmartScreen seulement = 1 popup, **plus furtif**

**Important**: Le popup SmartScreen est **attendu** pour tout exe non signé. L'essentiel c'est:
1. ✅ Defender ne bloque plus (AMSI/ETW bypass)
2. ✅ Pas de UAC suspect
3. ✅ Obfuscation automatique
4. ✅ Mode furtif activé

---

**Auteur**: KeyPyLogger Educational Project
**Date**: 27/12/2025
**Contexte**: Epitech - Lab isolé
