#!/bin/bash

# Create archive folder
mkdir -p docs_archive

# Move all OLD documentation files to archive
# Keep only the 6 new consolidated files

KEEP_FILES=(
  "README.md"
  "GETTING_STARTED.md"
  "STRATEGIES.md"
  "TROUBLESHOOTING.md"
  "ARCHITECTURE.md"
  "DEBUG_SUMMARY.md"
  "DOCS_INDEX.md"
  "DOCUMENTATION_STRUCTURE.txt"
)

# Find all .md files in root
for file in *.md *.txt; do
  # Skip if file doesn't exist
  [ -e "$file" ] || continue
  
  # Check if file is in KEEP list
  skip=0
  for keep in "${KEEP_FILES[@]}"; do
    if [ "$file" = "$keep" ]; then
      skip=1
      break
    fi
  done
  
  # Move to archive if not in keep list
  if [ $skip -eq 0 ]; then
    mv "$file" "docs_archive/" 2>/dev/null
    echo "✓ Archived: $file"
  fi
done

echo ""
echo "✅ Cleanup complete!"
echo "📁 Old docs moved to: docs_archive/"
echo ""
echo "📚 Active documentation files:"
ls -1 README.md GETTING_STARTED.md STRATEGIES.md TROUBLESHOOTING.md ARCHITECTURE.md DEBUG_SUMMARY.md 2>/dev/null | sed 's/^/  ✓ /'

