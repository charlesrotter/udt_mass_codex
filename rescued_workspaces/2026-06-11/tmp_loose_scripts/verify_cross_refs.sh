#!/bin/bash
file="/home/udt-admin/UDT/docs/udt_active_results.md"

echo "=== Verifying cross-references in AR §1.6.10 ==="
echo ""

refs=(
  "§1.6.7"
  "§1.6.8"
  "§1.6.9"
  "§1.9"
  "§1.4.5"
  "CG §12.15.6b"
  "CG §12.15.6c"
  "CG §15.3"
  "CG §11.7"
  "CG §11.8"
  "CG §11.9"
)

for ref in "${refs[@]}"; do
  if [[ "$ref" == "CG"* ]]; then
    echo "✓ $ref (canonical guide, not in AR)"
  else
    count=$(grep -c "^#### $ref\|^### $ref" "$file")
    if [ "$count" -gt 0 ]; then
      echo "✓ $ref exists"
    else
      echo "✗ $ref NOT FOUND"
    fi
  fi
done
