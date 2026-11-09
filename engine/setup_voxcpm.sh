#!/usr/bin/env bash
# Stellt die Sprach-Umgebung für VoxCPM2 wieder her (z. B. nach einem neuen Container).
#   bash engine/setup_voxcpm.sh <zielordner>
# Danach:
#   QA_WHISPER=<ziel>/models/whisper-medium HF_HUB_OFFLINE=1 <ziel>/vx/bin/python engine/build_timeline.py <projekt> <ziel>/models/VoxCPM2
# Benötigt Netzwerkzugriff auf PyPI und Hugging Face (huggingface.co, cas-bridge.xethub.hf.co, us.aws.cdn.hf.co).
set -euo pipefail
Z="${1:?Zielordner angeben}"
mkdir -p "$Z/models"
if [ ! -x "$Z/vx/bin/python" ]; then
  python3 -m venv "$Z/vx"
  "$Z/vx/bin/pip" install -q -U pip setuptools wheel
  "$Z/vx/bin/pip" install -q "voxcpm>=2.0.3" soundfile faster-whisper
fi
for m in openbmb/VoxCPM2 Systran/faster-whisper-small Systran/faster-whisper-medium; do
  name="${m#*/}"; name="${name#faster-}"
  HF_HUB_DISABLE_XET=1 "$Z/vx/bin/python" -c "from huggingface_hub import snapshot_download; snapshot_download('$m', local_dir='$Z/models/$name', max_workers=4)"
done
echo "Fertig: $Z/models/VoxCPM2, $Z/models/whisper-small, $Z/models/whisper-medium"
