[app]
title = Neon Space
package.name = neonspace
package.domain = com.gamer
source.dir = .
source.include_exts = py,png,jpg,mp3,ogg,wav,json
version = 1.0.0
requirements = python3,pygame_sdl2
orientation = portrait
fullscreen = 1
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.logcat_filters = *:S python:D
android.copy_libs = 1
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
