#!/bin/bash
# Convert .pptx → .key + .pdf via Keynote AppleScript
# Usage: ./convert_to_keynote_pdf.sh /absolute/path/to/devotional.pptx
set -e
PPTX="$1"
[ -z "$PPTX" ] && { echo "Usage: $0 /path/to/file.pptx"; exit 1; }
[ ! -f "$PPTX" ] && { echo "Not found: $PPTX"; exit 1; }
KEY="${PPTX%.pptx}.key"
PDF="${PPTX%.pptx}.pdf"

osascript <<EOF
tell application "Keynote"
  activate
  delay 1
  set theFile to POSIX file "$PPTX"
  set theDoc to open theFile
  delay 3
  save theDoc in POSIX file "$KEY"
  delay 2
  set pdfDest to POSIX file "$PDF"
  export theDoc to pdfDest as PDF
  delay 2
  close theDoc saving no
end tell
EOF

ls -la "$KEY" "$PDF" 2>&1 | tail -3
