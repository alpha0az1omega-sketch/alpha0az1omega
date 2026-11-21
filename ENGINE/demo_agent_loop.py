import os
import json
import subprocess
import hashlib
from datetime import datetime

# 1. L'IA PROPOSE (Simulation)
print("🤖 [ENGINE]: L'IA propose une modification (ajout d'une fonction)...")
proposed_code = "def add(a, b):\n    return a + b\n"
with open("ENGINE/proposed_function.py", "w") as f:
    f.write(proposed_code)

# Génération du Manifeste de Critique de l'IA
manifest = {
    "version": "0.1.0",
    "ai_agent": {
        "model_name": "Demo-Agent-v1",
        "prompt_hash": hashlib.sha256(b"Add two numbers").hexdigest()
    },
    "proposed_changes": {
        "target_file": "ENGINE/proposed_function.py",
        "rationale": "Added a basic addition function."
    },
    "self_critique": {
        "potential_risks": "None detected.",
        "deterministic_tests_passed": False
    },
    "human_approval": {
        "status": "PENDING",
        "pgp_signature": None
    }
}

with open("ENGINE/demo_critique_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# 2. LE JUGE DÉTERMINISTE (Le CORE vérifie)
print("\n⚙️ [CORE]: Exécution des tests déterministes...")
# On simule un test qui passe (dans la réalité, on lancerait 'cargo test' ou 'forge test')
test_passed = True 

if test_passed:
    print("✅ [CORE]: Tests RÉUSSIS. L'IA met à jour son manifeste.")
    manifest["self_critique"]["deterministic_tests_passed"] = True
    with open("ENGINE/demo_critique_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
else:
    print("❌ [CORE]: Tests ÉCHOUÉS. La proposition est rejetée automatiquement.")
    exit(1)

# 3. L'HUMAIN SIGNE (L'Asymétrie Stricte)
print("\n🛡️ [HUMAN]: L'IA ne peut pas signer ceci. C'est à vous de valider avec votre clé PGP.")
print("Le terminal va vous demander votre phrase de passe...")

# Appel de GPG pour signer le manifeste
result = subprocess.run(
    ["gpg", "-u", "EEC3D5AE9D2E2290", "--clearsign", "ENGINE/demo_critique_manifest.json"],
    capture_output=True, text=True
)

if result.returncode == 0:
    with open("ENGINE/demo_critique_manifest.json.asc", "w") as f:
        f.write(result.stdout)
    print("\n🏆 [SUCCESS]: Signature Humaine appliquée. La boucle est bouclée.")
    print("Vous pouvez vérifier la preuve avec : gpg --verify ENGINE/demo_critique_manifest.json.asc")
else:
    print("\n❌ Échec de la signature. Avez-vous entré la bonne phrase de passe ?")
