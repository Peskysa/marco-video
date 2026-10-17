# Manual de Marco Vídeo

[Portada](../README.md) · [Instalación](INSTALACION.md) · [Compatibilidad](COMPATIBILIDAD.md)

## Primera sesión

Selecciona Español, English o Français en la parte superior. Pulsa **Abrir archivos** para añadir uno o varios vídeos/audios; también puedes arrastrarlos. **Abrir carpeta** añade los medios de esa carpeta (escritorio no recorre subcarpetas; en web la selección puede incluirlas). Haz doble clic en la lista del escritorio, o clic en la web, para reproducir una entrada.

El proyecto incluye `assets/demo.webm` y `assets/demo.srt`, un paisaje animado original con sonido de prueba. Puedes abrirlos para probar los controles sin aportar archivos personales.

Las URL admitidas son HTTP/HTTPS de archivos directos. Pulsa **Abrir URL** e introduce la dirección. No introduzcas contraseñas ni enlaces con credenciales incorporadas; no se admiten esos enlaces. La aplicación no obtiene vídeos de páginas de plataformas ni descifra DRM.

## Reproducción

Pulsa ▶/Ⅱ o Espacio para reproducir o pausar. La barra permite buscar una posición; los botones ±10 saltan diez segundos. El escritorio también dispone de **Ir al segundo** en el menú. Velocidades entre 0,25× y 4×; la conservación del tono y las velocidades extremas dependen del motor y del archivo. **Detener** pausa y vuelve al inicio.

La repetición puede estar desactivada, limitarse a un archivo o recorrer toda la lista. Aleatorio elige otra entrada cuando hay más de una. Al finalizar la última entrada, la reproducción se detiene salvo repetición de lista/archivo. Los botones siguiente/anterior manuales permiten volver al otro extremo de la lista.

La última posición se recuerda localmente; se recupera cuando quedan más de tres segundos antes del final y ya habían transcurrido más de tres. Desmarca **Recordar posición** para no restaurarla. Esto no conserva permisos sobre archivos locales en la web: tendrás que seleccionarlos de nuevo.

## Bucle A–B

Colócate en el inicio y pulsa **Marcar A**; después busca el final y pulsa **Marcar B**. Debe haber al menos 0,2 segundos entre ambos puntos. Se repite ese tramo. **Borrar A–B** cancela el bucle. Cambiar de archivo también lo cancela.

## Listas

Usa el filtro para localizar un nombre. Las flechas de orden y el botón quitar actúan sobre la entrada seleccionada (en web, la que se está reproduciendo). Quitar o vaciar una lista **no borra los archivos del disco**.

**Exportar lista M3U** guarda el orden. Escritorio conserva rutas completas/URL y puede importar rutas relativas a la carpeta de la lista. Web y Android exportan nombres de archivos locales y URL; al importar, selecciona de nuevo los archivos correspondientes. No se guardan los vídeos dentro de una M3U. Los comentarios `#EXTINF` se omiten al importar; no hay soporte de listas HLS/IPTV ni seguimiento de enlaces de playlists remotas.

## Subtítulos

Abre un archivo **SRT o WebVTT** desde el botón dedicado. Se muestra texto plano: no se ejecuta HTML ni se conserva estilismo ASS/SSA. Admite UTF-8, UTF-16 con marca BOM y Windows-1252 como alternativa. Los subtítulos externos se restablecen al cambiar de vídeo.

En el menú de escritorio o **Detalles → Subtítulos** de la web, ajusta tamaño y retraso. El retraso se aplica a los SRT/VTT externos: un valor positivo retrasa el texto y uno negativo lo adelanta. **Ocultar subtítulos** desactiva los externos y las pistas internas.

Escritorio permite escoger las pistas internas que detecta Qt. La web muestra las que expone `video.textTracks`; muchos navegadores no exponen los subtítulos incrustados en un MKV. No se promete compatibilidad con todos los estilos/formas de subtítulo interno.

## Imagen y sonido

Pantalla completa amplía la sesión. **Modo concentración** oculta la lista; en escritorio, **Siempre visible** conserva la ventana por encima de otras. Web ofrece ventana flotante si el navegador la admite y el vídeo está cargado.

En la web, **Detalles → Imagen** permite encajar/rellenar, girar y modificar brillo, contraste y saturación. Los ajustes son visuales y no modifican el archivo. La captura PNG guarda el fotograma original, sin esos filtros, giro ni subtítulos superpuestos.

El ecualizador web/Android dispone de graves, medios y agudos de −12 a +12 dB. Actívalo con un archivo local; no se aplica por defecto. Las URL pueden necesitar permiso CORS si ya se ha conectado el elemento al motor de audio: si un servidor no lo permite, recarga la aplicación y reproduce la URL sin activar el ecualizador. Esto no afecta al archivo original. El escritorio permite elegir pista de audio y salida detectada por el sistema; no incluye ecualizador.

## Marcadores, capturas y temporizador

**Añadir marcador** guarda la posición y un nombre. Abre Marcadores para saltar a uno. En web puedes eliminarlos individualmente; se conservan localmente entre sesiones para el mismo archivo. No se sincronizan entre equipos.

**Guardar fotograma** exporta una imagen PNG. En Android se abre el diálogo para compartir/guardar. Las URL de otros servidores pueden impedir capturas por CORS. En escritorio el menú incluye avance de fotograma aproximado: usa los FPS declarados o 25 si no están disponibles; no es una herramienta de edición precisa.

El temporizador recibe minutos, hasta 1440. Cero lo cancela; al cumplirse, **pausa la reproducción**, no apaga el ordenador ni el teléfono. El navegador/Android puede retrasar el temporizador en segundo plano o con el equipo suspendido.

## Atajos

| Tecla | Acción |
| --- | --- |
| Espacio | Pausa/reproducción |
| ← / → | Saltar 5 segundos |
| ↑ / ↓ | Volumen |
| F / Esc | Pantalla completa / salir |
| M | Silencio |
| N / P | Siguiente / anterior |
| A / B | Puntos del bucle |
| Ctrl+O / Ctrl+Mayús+O | Abrir archivos / carpeta (escritorio) |
| Ctrl+B / Ctrl+S | Marcador / captura (escritorio) |

En web los atajos no interfieren con campos, selectores ni botones que tengan el foco. En Android se utilizan principalmente los controles táctiles.
