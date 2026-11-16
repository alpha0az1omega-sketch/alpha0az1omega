#!/bin/bash

# ==========================================
# ALPHA0AZ1OMEGA MASTER VERIFIER (v0.1)
# This script is the deterministic judge.
# It verifies the entire organism in one command.
# ==========================================

echo "🔍 Starting Organism Verification..."
echo "-----------------------------------"

# 1. Verify Cryptographic Identity (PGP Signature of the last commit)
echo "Step 1: Checking Cryptographic Identity (PGP Signature)..."
if git log --show-signature -1 | grep -q "Bonne signature"; then
    echo "✅ PGP Signature is valid."
else
    echo "❌ ERROR: PGP Signature is invalid or missing."
    exit 1
fi

# 2. Verify The Wheel (CORE - Rust Tests)
echo "Step 2: Verifying The Wheel (CORE Rust Tests)..."
cd CORE/verifier
if cargo test --quiet; then
    echo "✅ CORE mathematical logic is valid."
else
    echo "❌ ERROR: CORE tests failed."
    exit 1
fi
cd ../..

# 3. Verify The Economics (VALUE - Solidity Tests)
echo "Step 3: Verifying The Economics (VALUE Solidity Tests)..."
cd VALUE/contracts
if forge test --quiet; then
    echo "✅ VALUE economic logic is valid."
else
    echo "❌ ERROR: VALUE tests failed."
    exit 1
fi
cd ../..

echo "-----------------------------------"
echo "🏆 SUCCESS: The alpha0az1omega organism is fully verified and intact."
