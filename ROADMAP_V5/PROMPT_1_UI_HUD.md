# PROMPT 1 : HUD Inédit (Three.js / Frontend)

**Contexte :** Tu es un expert Three.js et UI/UX. Tu travailles sur le fichier `VISUAL/index.html` du projet Alpha0az1omega. Le design actuel (fond blanc, visage filaire, panneaux) doit être conservé.

**Tâches :**
1. **Arbre de Merkle 3D :** Connecte les sommets (vertices) du maillage de la tête 3D aux hashs SHA-256 du panneau "Epistemic Integrity". Quand un hash est validé, crée une animation d'onde lumineuse (cyan/or) qui parcourt les arêtes du visage.
2. **Mode Diff & Signature :** Modifie le terminal `α >` pour qu'il affiche les propositions de l'IA sous forme de deux colonnes (Proposition IA vs État Actuel). Ajoute un bouton "SIGN PGP (27D7...)" qui simule la validation.
3. **Oscilloscope d'Entropie :** Ajoute un mini-canvas 2D dans le panneau "System Identity" qui dessine une courbe sinusoïdale temps réel. La fréquence doit augmenter quand l'utilisateur tape vite ou quand l'IA répond.

**Contraintes :** Ne touche pas à la géométrie du visage. Utilise uniquement Three.js et Canvas 2D.
