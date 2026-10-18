<p align="center"><img src="assets/banner.svg" alt="Marco Vídeo · Colección Marco Pescador" width="100%"></p>

<p align="center"><a href="LICENSE"><img alt="AGPL-3.0-only" src="https://img.shields.io/badge/licencia-AGPL--3.0-173e40?style=flat-square"></a> <a href="https://github.com/Peskysa/marco-video/actions/workflows/release.yml"><img alt="Compilación y pruebas" src="https://github.com/Peskysa/marco-video/actions/workflows/release.yml/badge.svg"></a> <a href="https://github.com/Peskysa/marco-video/releases/latest"><img alt="Última versión" src="https://img.shields.io/github/v/release/Peskysa/marco-video?style=flat-square"></a></p>

<p align="center"><strong>Reproduce vídeos y audios propios, organiza listas y controla subtítulos, imagen y sonido.</strong><br>Linux · Windows · Portable · Web · Android</p>

<p align="center"><a href="https://marco-video.peskysa.chatgpt.site"><strong>Abrir aplicación web</strong></a> · <a href="https://github.com/Peskysa/marco-video/releases/latest">Descargas</a> · <a href="docs/README.md">Documentación</a> · <a href="https://github.com/Peskysa/marco-video/issues">Ayuda</a></p>

## La aplicación

Reproduce vídeos y audios propios, organiza listas y controla subtítulos, imagen y sonido. Creada por **Marco Pescador**. Listas, subtítulos SRT/WebVTT, velocidad, marcadores, reanudación, capturas y controles de reproducción. Interfaz en español, inglés y francés.

![Aplicación real en escritorio](docs/images/escritorio.png)

## Cinco modalidades

| Modalidad | Descarga | Uso |
| --- | --- | --- |
| **Linux** | [Marco-Video-Linux-amd64.deb](https://github.com/Peskysa/marco-video/releases/download/v1.1.0/Marco-Video-Linux-amd64.deb) | Instalador DEB para amd64; también portable TAR.GZ. |
| **Windows** | [Marco-Video-Windows-Instalador.exe](https://github.com/Peskysa/marco-video/releases/download/v1.1.0/Marco-Video-Windows-Instalador.exe) | Instalador para el usuario actual, x64. |
| **Portable** | [Marco-Video-Portable.exe](https://github.com/Peskysa/marco-video/releases/download/v1.1.0/Marco-Video-Portable.exe) | Un EXE Windows sin instalar; también web portable y Linux portable. |
| **Web** | [Marco-Video-Web.zip](https://github.com/Peskysa/marco-video/releases/download/v1.1.0/Marco-Video-Web.zip) | ZIP autónomo para navegador o alojamiento HTTPS. |
| **Android** | [Marco-Video-Android.apk](https://github.com/Peskysa/marco-video/releases/download/v1.1.0/Marco-Video-Android.apk) | APK de publicación firmado con clave propia del proyecto. |

Todas las variantes incluyen la aplicación y sus recursos. No necesitas instalar Python ni Node.js para utilizar los paquetes compilados. Los portables no requieren instalación, pero siguen sujetos a los permisos de ejecución del equipo. Los ejecutables Windows no tienen firma comercial. El APK se instala directamente, fuera de Google Play; su compilación no equivale a una prueba en teléfono físico.

Acceso: **Repositorio y web públicos**. La visibilidad del repositorio y la del alojamiento web son ajustes independientes. La publicación concreta y sus archivos se comprueban en [Releases](https://github.com/Peskysa/marco-video/releases/latest).

Además: `Marco-Video-Web-Portable.exe`, `Marco-Video-Linux-Portable.tar.gz`, documentación, código fuente y `SHA256SUMS.txt`. [Formatos, requisitos y verificación](docs/DISTRIBUCION.md).

## Funciones

Listas, subtítulos SRT/WebVTT, velocidad, marcadores, reanudación, capturas y controles de reproducción. Interfaz en español, inglés y francés. [Manual completo](docs/MANUAL.md).

![Función principal real](docs/images/funcion.png)

## Capturas

<p align="center"><img src="docs/images/movil.png" alt="Vista móvil real en navegador con pantalla simulada" width="320"></p>

Capturas auténticas de la aplicación con ejemplos propios. La vista móvil usa una pantalla simulada del navegador; no representa una prueba en Android físico. [Galería y reproducción](docs/CAPTURAS.md).

## Instalación y uso

Descarga el formato de tu sistema en [Releases](https://github.com/Peskysa/marco-video/releases/latest), comprueba su suma SHA-256 y sigue [Instalación](docs/INSTALACION.md). En la web, abre el enlace de la portada. Los archivos se procesan en el dispositivo; consulta [Privacidad](docs/PRIVACIDAD.md) para las conexiones y datos locales concretos.

## Documentación

- [Instalación](docs/INSTALACION.md) y [manual](docs/MANUAL.md).
- [Distribución](docs/DISTRIBUCION.md), [capturas](docs/CAPTURAS.md) y [desarrollo](docs/DESARROLLO.md).
- [Privacidad](docs/PRIVACIDAD.md), [licencia](docs/LICENCIA.md) y [terceros](THIRD_PARTY.md).
- [Historial](CHANGELOG.md), [contribuir](CONTRIBUTING.md) y [seguridad](SECURITY.md).

## Desarrollo y comprobaciones

Consulta [Desarrollo](docs/DESARROLLO.md) para las herramientas y pruebas funcionales. El contrato común se comprueba con `python scripts/distribution.py check`. Las publicaciones automáticas generan los nueve paquetes comunes y sus sumas; la publicación falla si falta alguno.

## Alcance y límites

Los formatos reproducibles dependen de los códecs de cada plataforma. Web y Android tienen menos formatos que escritorio. Sin DRM, conversión ni descarga de plataformas. Las distintas tecnologías mantienen sus diferencias documentadas; compartir formatos de distribución no garantiza idénticos códecs o prestaciones del sistema.

## Licencia y autoría

Copyright © 2026 **Marco Pescador**. Código e identidad visual originales bajo [GNU AGPL versión 3 exclusivamente](LICENSE), `AGPL-3.0-only`, sin garantía. Los componentes de terceros conservan sus licencias. Las ediciones anteriores conservan las condiciones con que se publicaron. [Detalles y código fuente](docs/LICENCIA.md).
