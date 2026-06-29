#!/bin/bash
# Build MHDDoS APK using Docker + Buildozer
# Run this on Linux or WSL2 (Windows)

set -e

IMAGE="kivy/buildozer:latest"

echo "[*] Pulling Buildozer Docker image..."
docker pull $IMAGE

echo "[*] Building APK (this may take 30+ minutes first time)..."
docker run --rm -it \
    -v "$(pwd):/home/user/work" \
    -w /home/user/work \
    $IMAGE \
    bash -c "pip install --user --upgrade buildozer cython && buildozer android debug"

echo ""
echo "[+] Done! APK should be in: bin/"
echo "    Look for: bin/mhddos-*-debug.apk"
