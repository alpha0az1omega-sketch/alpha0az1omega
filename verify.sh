#!/bin/bash
echo "🔍 Verifying Organism V2..."
echo "-----------------------------------"

# 1. PGP Check
if git verify-commit HEAD > /dev/null 2>&1; then
    echo "✅ PGP Signature is valid."
else
    echo "❌ ERROR: PGP Signature is invalid or missing."
    exit 1
fi

# 2. Hash Check
if ./verify_ai.sh; then
    echo "✅ Cryptographic integrity verified."
else
    echo "❌ ERROR: Hash mismatch."
    exit 1
fi

# 3. Ledger Check
if python3 ENGINE/ledger.py | grep -q "LEDGER VALID"; then
    echo "✅ Cryptographic Ledger is intact."
else
    echo "❌ ERROR: Ledger is corrupted."
    exit 1
fi

# 4. Solidity Tests
cd VALUE/contracts
if forge test > /dev/null 2>&1; then
    echo "✅ Solidity Smart Contract tests passed (Royalties & Anti-Reentrancy)."
else
    echo "❌ ERROR: Solidity tests failed."
    exit 1
fi
cd ../..

echo "-----------------------------------"
echo "🏆 SUCCESS: The Organism is fully verified, secured, and ready."
