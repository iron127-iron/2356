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

# Python for Android (p4a) branch
p4a.branch = develop

# Android SDK / NDK / API
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.cmd = 33.0.3

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# Architectures
android.archs = arm64-v8a, armeabi-v7a

# App entry point
android.entrypoint = main.py
source.entrypoint = main.py

# Presplash (optional - uncomment if you have images)
# android.presplash_color = #FFFFFF
# android.presplash_image = presplash.png

# App icon (optional)
# android.icon = icon.png

# Debug mode (set to 0 for release build)
android.debug = 1

# Java max heap (increase for large builds)
android.accept_sdk_license = True

# Extra Java dependencies (if needed)
# android.gradle_depends = ...

# Log level
log_level = 2

# Architecture filter
android.arch = arm64-v8a

[buildozer]

# Download locations for SDK/NDK
warn_on_root = 0
