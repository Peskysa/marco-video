#!/bin/sh
set -eu
root="$(pwd)/build/deb"
mkdir -p "$root/DEBIAN" "$root/opt/marco-video" "$root/usr/bin" "$root/usr/share/applications" "$root/usr/share/icons/hicolor/scalable/apps"
cp -a 'dist/Marco Video/.' "$root/opt/marco-video/"
cp web/icon.svg "$root/usr/share/icons/hicolor/scalable/apps/marco-video.svg"
cat > "$root/DEBIAN/control" <<'EOF'
Package: marco-video
Version: 1.0.0
Section: video
Priority: optional
Architecture: amd64
Maintainer: Marco Pescador
Depends: libc6 (>= 2.35), libgl1, libegl1, libxkbcommon0, libxkbcommon-x11-0, libxcb-shape0, libxcb-cursor0, libxcb-icccm4, libxcb-image0, libxcb-keysyms1, libxcb-render-util0, libxcb-xinerama0, libxcb-xkb1, libpulse0, libnss3, libasound2
Description: Reproductor de video local con listas y subtitulos, ES EN FR.
EOF
cat > "$root/usr/bin/marco-video" <<'EOF'
#!/bin/sh
exec '/opt/marco-video/Marco Video' "$@"
EOF
chmod 755 "$root/usr/bin/marco-video"
cat > "$root/usr/share/applications/marco-video.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Marco Vídeo
Exec=marco-video %F
Icon=marco-video
Terminal=false
Categories=AudioVideo;Player;Video;
MimeType=video/mp4;video/webm;video/x-matroska;video/quicktime;audio/mpeg;
EOF
dpkg-deb --root-owner-group --build "$root" dist/Marco-Video-Linux-amd64.deb
tar -czf dist/Marco-Video-Linux-Portable.tar.gz -C dist 'Marco Video'
