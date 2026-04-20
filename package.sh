#!/usr/bin/env bash
# Packages the Helm chart into a .tgz ready for import into PCAI
set -euo pipefail

cd "$(dirname "$0")"
helm package helm/pcai-chat-demo --destination .
echo ""
echo "Upload the generated .tgz to PCAI via:"
echo "  Tools & Frameworks → Import Framework"
