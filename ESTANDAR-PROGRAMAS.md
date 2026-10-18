# Estándar de la colección

Autor: Marco Pescador. Licencia del código original: AGPL-3.0-only. Cada programa mantiene su repositorio y su arquitectura, y comparte la misma organización de documentación, distribución y publicación.

## Estructura común

`README.md`, `LICENSE`, `NOTICE`, `THIRD_PARTY.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `project.json`, `assets/`, `docs/`, `licenses/`, `scripts/distribution.py` y `.github/workflows/release.yml`.

En `docs/`: README, INSTALACION, MANUAL, DESARROLLO, PRIVACIDAD, CAPTURAS, LICENCIA y DISTRIBUCION. En `docs/images/`: escritorio.png, funcion.png y movil.png. Las imágenes muestran cada aplicación real; se comparte el criterio y la colocación, no una misma captura para programas distintos.

## Entrega obligatoria

Cinco modalidades: Linux, Windows, portable, web y Android. Cada Release contiene, con el prefijo de su programa:

1. `-Windows-Instalador.exe`
2. `-Portable.exe`
3. `-Web-Portable.exe`
4. `-Linux-amd64.deb`
5. `-Linux-Portable.tar.gz`
6. `-Web.zip`
7. `-Android.apk`, firmado con clave propia estable
8. `-Documentacion.zip`
9. `-Source.zip`, del mismo commit
10. `SHA256SUMS.txt`

Los sistemas tienen funciones y requisitos distintos que deben explicarse. Portable no significa eludir permisos del ordenador. Android firmado no significa publicado en Google Play ni probado físicamente. Las sumas verifican integridad; no sustituyen una firma comercial.

## Publicación

**Todo en GitHub debe ser público**, incluidos los repositorios existentes y futuros y sus descargas. Es una instrucción permanente de Marco. Las credenciales y claves de firma se guardan como secretos, nunca en el código.

La autorización permanente está en AGENTS.md. Autenticación mediante GitHub CLI ya iniciada como Peskysa y almacenada en el gestor de credenciales, con permisos repo y workflow. Los trabajos usan GITHUB_TOKEN con permisos de su repositorio, y secretos de firma Android independientes. Nunca copiar tokens a código o chat.

Las etiquetas de versión activan compilación, pruebas, verificación de paquetes y publicación automática. Antes de finalizar, confirmar los nueve paquetes, hashes, commit, resultado de Actions y acceso al sitio. Mantener registro de limitaciones reales.

La aplicación tiene además sus propios permisos de archivos/red y aprobación. Si Marco desea eliminar las consultas técnicas rutinarias, puede elegir Full access en los permisos del proyecto; esta elección da acceso amplio a su equipo y red. La sesión actual usa workspace-write y revisión automática. Las instrucciones de AGENTS.md no pueden cambiar ese ajuste ni impedir una renovación de login exigida por GitHub.
