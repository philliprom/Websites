#!/usr/bin/env bash
# Richtet alles für das Format „Unbekannte Nummer“ in einem frischen Container ein.
#   bash setup.sh <zielordner>          (z. B. das Scratchpad; braucht ca. 16 GB Platz)
# Danach gibt es: <ziel>/bl (Blender-Python), <ziel>/vx (Ton + Whisper), <ziel>/qw (Qwen3-TTS) und <ziel>/models/…
# Netz: PyPI, Hugging Face (ohne Xet), Ubuntu-Paketquellen.
set -euo pipefail
Z="${1:?Zielordner angeben}"
mkdir -p "$Z/models"
# 1) Mesa/EGL, damit Blender Workbench ohne Grafikkarte rendert (EGL_PLATFORM=surfaceless)
if [ ! -e /usr/lib/x86_64-linux-gnu/libEGL.so.1 ]; then
  apt-get update -q && apt-get install -y -q --no-install-recommends libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1
fi
command -v ffmpeg >/dev/null || apt-get install -y -q --no-install-recommends ffmpeg
# 2) Blender als Python-Modul
if [ ! -x "$Z/bl/bin/python" ]; then
  python3 -m venv "$Z/bl" && "$Z/bl/bin/pip" install -q "bpy==5.3.0" numpy soundfile
fi
# 3) Ton, Whisper, Praat (vx) – Qwen-Umgebung (qw) nutzt torch aus vx mit
if [ ! -x "$Z/vx/bin/python" ]; then
  python3 -m venv "$Z/vx" && "$Z/vx/bin/pip" install -q -U pip && \
  "$Z/vx/bin/pip" install -q torch faster-whisper soundfile scipy praat-parselmouth pillow
fi
if [ ! -x "$Z/qw/bin/python" ]; then
  python3 -m venv "$Z/qw"
  "$Z/vx/bin/python" -c 'import site;print(site.getsitepackages()[0])' > \
    "$("$Z/qw/bin/python" -c 'import site;print(site.getsitepackages()[0])')/zz_vx_torch.pth"
  "$Z/qw/bin/pip" install -q qwen-tts
fi
# 4) Modelle
for spec in "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign:Qwen3-TTS-VoiceDesign" "Qwen/Qwen3-TTS-12Hz-1.7B-Base:Qwen3-TTS-Base" \
            "Systran/faster-whisper-medium:whisper-medium"; do
  repo="${spec%%:*}"; dir="${spec##*:}"
  [ -d "$Z/models/$dir" ] || HF_HUB_DISABLE_XET=1 "$Z/vx/bin/python" -c \
    "from huggingface_hub import snapshot_download as d; d('$repo', local_dir='$Z/models/$dir', max_workers=4)"
done
echo "Fertig. Test: EGL_PLATFORM=surfaceless $Z/bl/bin/python -c 'import bpy; print(bpy.app.version_string)'"
