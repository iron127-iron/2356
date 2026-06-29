[app]

# App basic info
title = MHDDoS
package.name = mhddos
package.domain = org.mhddos

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json,mmdb
source.include_patterns = libs/PyRoxy/**, files/**, config.json, help.txt

# Version
version = 2.4.4
version.regex = __version__\s*=\s*['"](.*)['"]
version.filename = start.py

# Requirements (pip packages)
requirements = python3,kivy,impacket,dnspython,requests,cloudscraper,certifi,psutil,icmplib,pyasn1,yarl,pysocks,maxminddb,six

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Android SDK / NDK / API
android.api = 34
android.minapi = 21
android.ndk = 27c
android.sdk = 34
android.cmd = 34.0.0

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# Architectures (remove armeabi-v7a for faster build, add back if needed)
android.archs = arm64-v8a

# App entry point
android.entrypoint = main.py
source.entrypoint = main.py

# Debug mode
android.debug = 1

# Accept SDK license automatically
android.accept_sdk_license = True

# Log level
log_level = 2

[buildozer]

# Download locations for SDK/NDK
warn_on_root = 0
