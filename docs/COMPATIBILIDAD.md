# Funciones y compatibilidad

[Portada](../README.md)

| Función | Escritorio Windows/Linux | Web / portable web | Android |
| --- | --- | --- | --- |
| Motor | Qt Multimedia / FFmpeg | HTMLMediaElement del navegador | WebView del sistema |
| Interfaz ES / EN / FR | Sí | Sí | Sí |
| Archivos locales sin Internet | Sí | Sí | Sí |
| URL HTTP/HTTPS directa | Sí | Según HTTPS/CORS/códec | Según políticas de WebView/HTTPS |
| Listas, repetición, aleatorio, A–B | Sí | Sí | Sí |
| Reanudación y marcadores locales | Sí | Sí | Sí |
| SRT/VTT con retraso y tamaño | Sí | Sí | Sí |
| Pistas internas de audio/subtítulos | Según motor/contenedor | Solo subtítulos expuestos por navegador; sin selector de audio | Igual que web |
| Salida de audio seleccionable | Sí, dispositivos detectados | Salida predeterminada | Salida del sistema |
| Captura PNG | Sí | Sí, salvo restricciones CORS | Compartir mediante sistema |
| Brillo, contraste, saturación, giro | No | Sí, visuales | Sí, visuales |
| Ecualizador de tres bandas | No | Sí, archivos locales | Sí, archivos locales |
| Ventana flotante | Siempre visible | Picture-in-Picture si el navegador lo permite | No se garantiza PiP nativo |
| Avance de fotograma aproximado | Sí | No | No |
| Ejecución en segundo plano | Ventana abierta | Según navegador | No hay servicio de reproducción en segundo plano |

## Extensión no equivale a códec

MP4/MKV/AVI son contenedores, y cada uno puede alojar distintas codificaciones. Que un archivo tenga una extensión conocida no garantiza que el motor pueda decodificar su vídeo o audio. Si falla, se muestra un error sin modificarlo. MP4 H.264/AAC y WebM VP8/VP9+Opus suelen ser opciones interoperables, sujetas a plataforma.

La demo probada es WebM VP8+Opus, 960×540, diez segundos. Las comprobaciones automatizadas acreditan decodificación de vídeo y presencia de audio, búsqueda, controles y exportación. No certifican todos los códecs ni aceleración 4K/8K. El sonido de la demo es un tono sintético suave; no se ha hecho una evaluación auditiva humana de calidad.

El APK se compila y firma, pero no se anuncia como probado en un teléfono físico. La captura móvil es una ventana web de 390×844, no una prueba de Android físico. La compilación Linux ejecuta una prueba real bajo Xvfb; no acredita todos los escritorios y controladores gráficos.

No hay DRM, reproducción de discos ópticos, transcodificación, emisión Chromecast/DLNA, servicios de plataformas ni catálogo de películas. Tampoco se realiza búsqueda o descarga automática de subtítulos.
