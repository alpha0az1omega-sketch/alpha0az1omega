#!/bin/bash
echo "🤖 AI VERIFICATION PROTOCOL"
echo "---"
CORE_HASH=$(shasum -a 256 CORE/verifier/src/lib.rs | awk '{print $1}')
VALUE_HASH=$(shasum -a 256 VALUE/contracts/src/AlphaLicense.sol | awk '{print $1}')
PROOFS_HASH=$(shasum -a 256 PROOFS/legacy_projects_manifest.txt | awk '{print $1}')

# Remplacer par les hashes attendus (ceux du README)
EXPECTED_CORE="c9dc3980dfc9a7c0e79c057be35ae6fea3e8fb9a7b55555f3199931893afe9de"
EXPECTED_VALUE="d912974c4f4766a0a5f1fdcb7da453bd6474548907b36b37bc98d8367d5f82eb"
EXPECTED_PROOFS="42f98fce38d71778ccca150983ed25d703d89992c74103d47ed214bfbb7c09d2"

FAIL=0
if [ "$CORE_HASH" != "$EXPECTED_CORE" ]; then echo "❌ CORE hash mismatch"; FAIL=1; fi
if [ "$VALUE_HASH" != "$EXPECTED_VALUE" ]; then echo "❌ VALUE hash mismatch"; FAIL=1; fi
if [ "$PROOFS_HASH" != "$EXPECTED_PROOFS" ]; then echo "❌ PROOFS hash mismatch"; FAIL=1; fi

if [ $FAIL -eq 0 ]; then
    echo "✅ ALL HASHES MATCH. The organism is intact."
    exit 0
else
    echo "⚠️ VERIFICATION FAILED. Files have been modified."
    exit 1
fi
