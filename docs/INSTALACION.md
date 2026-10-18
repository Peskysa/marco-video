# Instalación y requisitos

[Portada](../README.md) · [Distribución y nombres de archivo](DISTRIBUCION.md)

Descarga los paquetes de la versión **1.1.0** en [Releases](https://github.com/Peskysa/marco-video/releases/latest). No se necesita Python, Node.js ni herramientas de desarrollo para utilizarlos. Comprueba el archivo con `Get-FileHash archivo -Algorithm SHA256` en Windows o `sha256sum archivo` en Linux, comparándolo con `SHA256SUMS.txt`.

## Windows

Windows x64. Ejecuta `Marco-Video-Windows-Instalador.exe` para instalar para tu usuario, o `Marco-Video-Portable.exe` para abrir sin instalación. `Marco-Video-Web-Portable.exe` abre la web incluida en tu navegador mediante un servidor solo local en 127.0.0.1; mantén su ventana abierta y ciérrala al terminar. Los EXE no tienen firma comercial. Los portables extraen componentes temporales y siguen sujetos a las políticas del equipo.

## Linux

Ubuntu 22.04 o distribución compatible, amd64 y entorno gráfico. Instala `Marco-Video-Linux-amd64.deb` con el gestor de paquetes para resolver dependencias. Para usar sin instalar, extrae `Marco-Video-Linux-Portable.tar.gz` y ejecuta el programa de su carpeta; las bibliotecas del sistema siguen siendo necesarias.

## Web

Abre [la aplicación alojada](https://marco-video.peskysa.chatgpt.site) o sirve `Marco-Video-Web.zip` desde HTTP(S). Usa un navegador moderno. Los recursos se incluyen en el ZIP; no se necesita instalar herramientas de desarrollo. El acceso al sitio alojado es independiente de la visibilidad del repositorio.

## Android

Instala `Marco-Video-Android.apk` tras autorizar esa fuente en Android. Usa una clave de publicación propia y estable del proyecto. No se publica en Google Play y no se ha probado en teléfono físico. Si usabas el antiguo APK debug de ajedrez, desinstálalo una vez antes de instalar el nuevo; las siguientes actualizaciones conservarán la clave de publicación.

## Requisitos concretos de este programa

Android 7 o posterior (API 24), WebView actualizado. Linux requiere glibc 2.35, OpenGL/EGL, X11/XCB, xkbcommon, PulseAudio/ALSA y NSS, según el DEB. Extrae el TAR.GZ y ejecuta `./Marco\ Video`. El ZIP web admite abrir index.html directamente; los formatos dependen del navegador.

Consulta [Manual](MANUAL.md) para las diferencias funcionales y [Privacidad](PRIVACIDAD.md) para los archivos locales y conexiones.
