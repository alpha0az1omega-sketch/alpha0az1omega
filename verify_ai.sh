#!/bin/bash
echo "🤖 AI VERIFICATION PROTOCOL INITIATED..."
echo "Calculating SHA-256 hashes..."
echo "---"
echo "Core Rust (CORE/verifier/src/lib.rs):"
shasum -a 256 CORE/verifier/src/lib.rs | awk '{print $1}'
echo "AlphaLicense Contract (VALUE/contracts/src/AlphaLicense.sol):"
shasum -a 256 VALUE/contracts/src/AlphaLicense.sol | awk '{print $1}'
echo "Entropy Manifest (PROOFS/legacy_projects_manifest.txt):"
shasum -a 256 PROOFS/legacy_projects_manifest.txt | awk '{print $1}'
echo "---"
echo "✅ VERIFICATION COMPLETE. Compare these hashes with the README manifest."
