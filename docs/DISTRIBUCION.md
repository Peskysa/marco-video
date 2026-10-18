# Cinco modalidades y distribución

[Portada](../README.md) · [Instalación](INSTALACION.md) · [Licencia](LICENCIA.md)

Versión **1.1.0**. Los cinco destinos obligatorios de la colección son Linux, Windows, portable, web y Android. Portable es una forma de distribución; se entrega para Windows y Linux.

| Archivo | Modalidad | Requisitos |
| --- | --- | --- |
| `Marco-Video-Windows-Instalador.exe` | Windows | Windows x64; instalación para el usuario actual |
| `Marco-Video-Portable.exe` | Portable Windows | Windows x64; sin instalar |
| `Marco-Video-Web-Portable.exe` | Portable web Windows | Windows x64 y navegador; servidor solo en 127.0.0.1 |
| `Marco-Video-Linux-amd64.deb` | Linux | Ubuntu 22.04 / glibc 2.35 o compatible; bibliotecas indicadas en Instalación |
| `Marco-Video-Linux-Portable.tar.gz` | Portable Linux | Extraer y ejecutar el programa; mismas bibliotecas del sistema que escritorio |
| `Marco-Video-Web.zip` | Web | Navegador moderno; alojamiento HTTP(S) o apertura local donde se documente |
| `Marco-Video-Android.apk` | Android | APK de publicación firmado con clave estable del proyecto; WebView actualizado |
| `Marco-Video-Documentacion.zip` | Documentación | Manuales, capturas y avisos de licencias |
| `Marco-Video-Source.zip` | Código fuente | Código e instrucciones del commit publicado |
| `SHA256SUMS.txt` | Verificación | SHA-256 de cada archivo adjunto |

Las compilaciones y pruebas se ejecutan en Windows y Linux; el APK se compila y verifica su firma. No se afirma una prueba en teléfono físico. En Windows no se incluye firma comercial de ejecutables. La clave Android se guarda en secretos de GitHub y se reutiliza para las siguientes versiones; cambiar desde el antiguo APK debug de ajedrez requiere desinstalarlo una vez.

Antes de publicar se comprueban los nueve paquetes y se calculan sus sumas. No se considera completa una modalidad por existir solamente su carpeta de código. Los enlaces de portada corresponden a esta versión; versiones antiguas pueden tener otros nombres.

Acceso: Repositorio privado; web pública. Web: https://marco-video.peskysa.chatgpt.site.
