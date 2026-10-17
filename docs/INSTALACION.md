# Instalar o usar sin instalar

[Portada](../README.md) · [Manual](MANUAL.md)

## Windows

Descarga los archivos desde [Releases](https://github.com/Peskysa/marco-video/releases/latest), no el ZIP de código fuente.

- **Portable:** abre `Marco-Video-Portable.exe`. Incorpora Python, Qt y el motor multimedia; no requiere VLC, códecs ni Python instalados. Descomprime componentes automáticamente en la carpeta temporal del usuario. Guarda preferencias en el perfil del usuario.
- **Portable web:** abre `Marco-Video-Web-Portable.exe`. Se abre tu navegador habitual con una dirección `http://127.0.0.1:PUERTO/`. Conserva la pequeña ventana del lanzador abierta. Todo está incluido; los vídeos locales no pasan por el servidor.
- **Instalador:** abre `Marco-Video-Windows-Instalador.exe`. Instala en `%LOCALAPPDATA%\Programs\Marco Video` y crea accesos directos para tu usuario. Se desinstala desde Aplicaciones de Windows.

Windows 10/11 x64. No se requiere administrador para las tres variantes; una política de empresa puede prohibir ejecutar EXE, usar carpetas temporales o abrir un servidor local. Los EXE no están firmados con un certificado comercial de Windows; el sistema puede mostrar su aviso de editor desconocido. No desactives las políticas de un equipo ajeno.

## Web normal y web sin Internet

La [web alojada](https://marco-video.peskysa.chatgpt.site) tiene acceso privado para la cuenta del propietario y necesita Internet para cargar la aplicación.

Descomprime `Marco-Video-Web.zip` y abre **`index.html`** en un navegador actual. Conserva los demás archivos junto a él. Funciona por `file://` sin instalar un servidor; se ha probado con Microsoft Edge. Otras políticas/navegadores pueden limitar las descargas, pantalla completa o ventana flotante.

En otro ordenador, copia la carpeta completa en un USB. No basta con guardar un enlace a una web de Internet: una dirección alojada requiere conexión para cargar la aplicación. No se promete caché automática ni instalación PWA.

Para alojarla, sirve el contenido del ZIP mediante HTTPS. No necesita backend, cuentas ni base de datos. Las URL de vídeo remotas requieren conexión y pueden estar bloqueadas por HTTPS/CORS, autenticación o política del servidor.

## Linux

El DEB está dirigido a **Ubuntu 22.04/24.04 x64 y sistemas compatibles con glibc ≥ 2.35**; Qt requiere además las bibliotecas gráficas y de sonido indicadas en el paquete.

```sh
sudo apt install ./Marco-Video-Linux-amd64.deb
marco-video
```

El instalador sí requiere permisos de administrador y puede necesitar Internet para resolver dependencias del sistema. La alternativa `Marco-Video-Linux-Portable.tar.gz` permite extraer y ejecutar `Marco Video/Marco Video` sin instalar el paquete, siempre que las bibliotecas del sistema estén presentes. No es compatible con todas las distribuciones ni con Linux ARM.

## Android

Instala `Marco-Video-Android.apk`, firmado con la clave propia del proyecto. Autoriza la instalación desde la aplicación que abre el APK. Android 7 o posterior, sujeto a los requisitos de WebView y Capacitor de esa versión. Selecciona vídeos con el selector de archivos del sistema; no solicita acceso general a todos tus archivos. La selección de carpetas depende del selector de Android.

Las capturas y listas se comparten mediante el diálogo del sistema. Mantén la aplicación en primer plano para usar el temporizador; Android puede suspenderla en segundo plano. La reproducción en segundo plano y PiP nativo Android no se anuncian como funciones garantizadas.

## Comprobar la descarga

`SHA256SUMS.txt` contiene el SHA-256 de cada archivo publicado. En PowerShell:

```powershell
Get-FileHash .\Marco-Video-Portable.exe -Algorithm SHA256
```

Compara el resultado completo. Estas sumas comprueban integridad; no sustituyen una firma comercial del editor.
