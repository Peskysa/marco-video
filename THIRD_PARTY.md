# Componentes de terceros

Marco Vídeo utiliza estas bibliotecas sin alterar sus licencias originales.

| Componente | Versión | Licencia / función | Fuentes |
| --- | --- | --- | --- |
| PySide6, Essentials, Addons, Shiboken6 | 6.10.3 | LGPL-3.0 / alternativas GPL según el módulo. Enlace dinámico con Qt; sin licencia comercial | [Qt for Python](https://code.qt.io/cgit/pyside/pyside-setup.git/tree/?h=v6.10.3) |
| Qt Core, Gui, Widgets, Network, OpenGL, Multimedia y sus dependencias | 6.10.3 | LGPL-3.0 / alternativas GPL; motor de ventanas y multimedia | [Qt 6.10.3](https://download.qt.io/archive/qt/6.10/6.10.3/single/), [licencias y atribuciones](https://doc.qt.io/qt-6.10/licenses-used-in-qt.html) |
| FFmpeg, distribuido con Qt | rama 7.1, bibliotecas ABI 61/59 | LGPL-2.1 o posterior y avisos de sus componentes; decodificación multimedia | [Fuentes FFmpeg](https://github.com/FFmpeg/FFmpeg/tree/n7.1.3), [atribución de Qt Multimedia](https://doc.qt.io/qt-6.10/qtmultimedia-attribution-ffmpeg.html) |
| Capacitor Core / Android | 8.5.3 | MIT; contenedor Android | [Fuente y licencia](https://github.com/ionic-team/capacitor) |
| Capacitor Filesystem / Share | 8.1.5 / 8.0.3 | MIT; exportación y compartición en Android | [Fuentes](https://github.com/ionic-team/capacitor-plugins) |
| Python | 3.12 en las compilaciones | PSF y avisos de biblioteca estándar; intérprete incorporado en los ejecutables | [Python 3.12](https://www.python.org/downloads/source/), [licencia](https://docs.python.org/3.12/license.html) |

Las copias de licencia y los metadatos de los paquetes instalados están en `licenses/`; el campo `License` del inventario conserva la declaración de upstream. El archivo comercial incluido en algunas ruedas PySide se conserva como aviso de upstream; no significa que Marco Vídeo use esa opción.

Los avisos adicionales de los módulos Qt y de sus componentes internos están en la documentación de atribuciones de Qt enlazada arriba. El paquete usa bibliotecas dinámicas, no modifica Qt ni FFmpeg, y permite sustituirlas por versiones ABI compatibles en la distribución en carpeta (`_internal`). También se incluye el procedimiento completo para reconstruir los ejecutables desde el código del proyecto. Las licencias de las bibliotecas siguen permitiendo su estudio y modificación según sus condiciones.

Para recuperar el código fuente correspondiente de Qt/PySide, utiliza exactamente las etiquetas 6.10.3 enlazadas, y los fuentes/recetas de FFmpeg de Qt Multimedia de esa versión. No uses una versión `latest` para reconstruir el paquete publicado. [Fuentes Qt Multimedia](https://code.qt.io/cgit/qt/qtmultimedia.git/tree/?h=v6.10.3).

Herramientas de desarrollo: PyInstaller 6.22.3 (GPL con excepción para los ejecutables), Playwright 1.64.1 (Apache-2.0), esbuild 0.27.3 (MIT), pnpm, Inno Setup y Android Gradle Plugin. No se atribuyen al autor ni se relicencian como código original del proyecto. `web/pnpm-lock.yaml` fija las dependencias transitivas.

La reproducción concreta depende del contenedor, códec y plataforma. No se distribuyen películas, medios DRM, servicios de streaming ni credenciales de terceros.
