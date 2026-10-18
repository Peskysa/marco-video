# Desarrollo y compilación

[Portada](../README.md) · [Contribuir](../CONTRIBUTING.md)

Proyecto independiente en `marco-video`; no modifica Marco PDF ni comparte sus claves de firma.

## Escritorio

Requiere Python 3.12 y entorno gráfico. En Linux instala también las bibliotecas X11/Qt/sonido declaradas en el DEB y Xvfb para las pruebas de CI.

```sh
python -m venv .venv
# Linux: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt pyinstaller==6.22.3
python -m unittest discover -s tests -v
python player.py
python player.py --self-test test-output/native-report.json
```

`core.py` contiene selección de fuentes, listas y subtítulos. `player.py` implementa la interfaz y Qt Multimedia. `native_check.py` comprueba decodificación real de VP8, presencia de pista Opus, búsqueda y las tres traducciones; `--smoke-test` solo comprueba la ventana y traducciones. La autoprueba real se usa también en los EXE compilados.

## Web y Android

Node.js 24 y pnpm 11.25.0:

```sh
cd web
pnpm install --frozen-lockfile
pnpm test
cd ..
python scripts/build.py
python -m http.server 5180 --bind 127.0.0.1 --directory dist/web
```

En otra terminal: `cd web` y `pnpm run test:browser`. Si no hay Edge, instala Chromium con `pnpm exec playwright install chromium` y selecciona `BROWSER_CHANNEL=chromium` (PowerShell: `$env:BROWSER_CHANNEL='chromium'`). El informe se guarda en `test-output/browser-report.json`.

La interfaz principal es HTML/CSS/JavaScript sin framework ni peticiones de recursos externos. El puente de exportación Android se empaqueta con esbuild. `translations.json` es el catálogo común ES/EN/FR; `scripts/build.py` genera su versión JavaScript y el ZIP web, apto para `file://` y HTTPS. No edites `web/translations.js` ni `web/native.js` generados.

Para Android, instala JDK 21, SDK 36 y build-tools 36.0.0. Desde `web/`, ejecuta `pnpm exec cap sync android`, entra en `android/` y ejecuta `./gradlew assembleDebug` (Windows: `gradlew.bat`). La publicación usa `assembleRelease`, un PKCS#12 privado `app/marco-video.p12`, alias `marco-video`, y `ANDROID_KEY_PASSWORD`. En GitHub se recuperan de `ANDROID_KEYSTORE` y `ANDROID_KEY_PASSWORD`; nunca se guardan en el repositorio.

## Paquetes

Primero instala las dependencias de ambos entornos y ejecuta `python scripts/licenses.py` y `python scripts/build.py`. Después:

```sh
python packaging/build.py
```

Genera la aplicación en carpeta `dist/Marco Video/`; en Windows también los dos EXE de un archivo. Conserva las bibliotecas dinámicas de Qt/FFmpeg. Las bibliotecas de la variante en carpeta están en `_internal`; pueden sustituirse por otras ABI compatibles y el programa puede reconstruirse desde sus fuentes con la versión modificada.

En Windows compila `packaging/windows.iss` con Inno Setup 6. En Linux ejecuta `bash packaging/linux.sh` para DEB y portable en carpeta. Los paquetes se compilan en sus propios sistemas; no se promete compilación cruzada.

`python packaging/docs.py` genera la documentación. La publicación de GitHub ejecuta pruebas, construye los seis formatos principales y la alternativa portable Linux, adjunta el ZIP de documentación, el fuente correspondiente del proyecto y sus sumas SHA-256. Se activa al enviar una etiqueta `v*` o manualmente. La versión 1.1.0 se mantiene coherente en Android, Inno, DEB y aplicación antes de crear otra etiqueta.

## Reemplazar o modificar dependencias

Las versiones y enlaces de fuentes se documentan en [THIRD_PARTY.md](../THIRD_PARTY.md), con licencias en `licenses/`. Para modificar Qt/PySide/FFmpeg utiliza sus fuentes de la misma versión, construye bibliotecas compatibles e instálalas en el entorno Python antes de empaquetar. No se han modificado esas bibliotecas para Marco Vídeo.

## Alcance verificado

Los informes reales deben corresponder al mismo código que se publica. Las pruebas de escritorio validan decodificación y búsqueda; las del navegador incluyen SRT, A–B, PNG, M3U, EQ, marcadores, reanudación, traducciones, ancho móvil y apertura offline. La compilación APK no equivale a una prueba en teléfono físico.
