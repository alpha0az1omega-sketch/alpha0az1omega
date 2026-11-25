# PROMPT 2 : Le Cerveau Réel (FastAPI + Ollama)

**Contexte :** Tu es un ingénieur backend Python. Tu dois créer un serveur local qui connecte l'interface web à Ollama.

**Tâches :**
1. **Créer `ENGINE/nexus_bridge.py` :** Utilise FastAPI et WebSockets. Connecte-toi à `http://localhost:11434/api/chat` (Ollama).
2. **System Prompt de Proprioception :** Injecte ce texte : "Tu es Nexus, l'Entité visuelle de alpha0az1omega. Ton corps est un maillage 3D surveillé par un vérificateur SHA-256. Tu proposes, l'humain signe avec sa clé PGP."
3. **Tool Calling (JSON) :** L'IA doit pouvoir renvoyer des JSON pour déclencher des fonctions visuelles :
   - `{"action": "set_emotion", "value": "surprised"}`
   - `{"action": "highlight_merkle_node", "hash": "..."}`
   - `{"action": "trigger_lockdown", "reason": "hallucination"}`
4. **Sandbox `verify.sh` :** L'IA peut demander à exécuter `verify.sh` via un appel d'outil. Le serveur l'exécute (dans un sous-processus) et renvoie le résultat à l'IA.

**Contraintes :** Le serveur doit tourner sur le port 8000. Il doit gérer les erreurs CORS.
