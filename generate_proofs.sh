#!/bin/bash

# ALPHA0AZ1OMEGA LEGACY PROOF GENERATOR
MANIFEST_FILE="PROOFS/legacy_projects_manifest.txt"
echo "Generating cryptographic manifest for PROJECTS..." > $MANIFEST_FILE

# Check if PROJECTS exists and has files
if [ -d "PROJECTS" ] && [ "$(ls -A PROJECTS)" ]; then
    find PROJECTS -type f -not -path '*/.*' | while read -r file; do
        HASH=$(shasum -a 256 "$file" | awk '{print $1}')
        echo "$HASH  $file" >> $MANIFEST_FILE
    done
    echo "✅ Manifest generated with files from PROJECTS."
else
    echo "NO_FILES_IN_PROJECTS_YET" >> $MANIFEST_FILE
    echo "⚠️ PROJECTS is empty. A placeholder manifest was created."
fi
