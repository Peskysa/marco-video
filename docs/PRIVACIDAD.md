# Privacidad y datos locales

La aplicación no tiene analítica, publicidad, cuentas propias, base de datos remota ni subida de vídeos. En las pruebas de archivos locales se bloquean todas las peticiones externas.

- Escritorio recuerda idioma, volumen, posiciones y marcadores con QSettings. En Windows se guarda en `HKEY_CURRENT_USER\Software\MarcoPescador\MarcoVideo`; en Linux, normalmente `~/.config/MarcoPescador/MarcoVideo.conf`. Las rutas y nombres pueden revelar qué archivos has abierto.
- Web/Android utiliza almacenamiento local del navegador/WebView con prefijo `marco-video:`. Conserva idioma, volumen, preferencia de reanudación, posiciones y marcadores; los identificadores locales contienen nombre, tamaño y fecha del archivo. No conserva el contenido de tus vídeos ni permisos permanentes sobre ellos.
- Las listas exportadas pueden contener nombres, rutas completas (escritorio) y URL. Revisa lo que compartes.
- Android guarda las exportaciones en la caché privada y abre el diálogo del sistema para compartirlas. Puedes borrar esa caché desde Ajustes de Android. La copia que guardes o compartas queda bajo tu control.
- Las URL remotas sí contactan con el servidor indicado y pueden transmitir tu IP y los datos habituales de una petición. Un navegador puede hacer sus propias comprobaciones ajenas a esta aplicación.

Para borrar lo recordado, elimina las preferencias indicadas o los datos del sitio/aplicación. Cerrar una sesión no borra automáticamente el historial de posiciones ni los marcadores.

El portable web sirve exclusivamente los recursos de la aplicación desde `127.0.0.1` en un puerto aleatorio y no acepta subidas de vídeos ni peticiones POST. El servidor termina al cerrar su ventana. No queda accesible para otros ordenadores de la red.

Una web alojada necesita Internet para cargar sus archivos. La autenticación y los registros del proveedor de alojamiento son independientes de la ausencia de analítica propia de Marco Vídeo. Usa el ZIP web o el portable si necesitas trabajar desconectado.
