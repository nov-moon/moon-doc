#!/bin/bash
gitbook build
rsync -auvztopgP --delete ./_book/ root@192.168.49.104:/opt/soft/tengine/html/mljr/moon-android

open http://192.168.49.104/moon-android/