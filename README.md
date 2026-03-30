# Sistema de Certificados REVEM

## Archivos del sistema

| Archivo | Para qué sirve |
|---|---|
| `generator.html` | Abre esto en tu navegador para generar certificados |
| `verify.html` | Va en GitHub Pages — es la página que muestra el QR |
| `certs.json` | Se genera automáticamente — contiene los datos para verificar |

---

## Paso 1 — Configurar GitHub Pages (una sola vez)

1. Ve a [github.com](https://github.com) e inicia sesión
2. Crea un repositorio nuevo llamado `revem-certs` (público)
3. Sube el archivo `verify.html` a ese repositorio
4. Ve a **Settings → Pages → Source → main branch → Save**
5. GitHub te dará una URL tipo: `https://TU-USUARIO.github.io/revem-certs/verify.html`
6. **Copia esa URL** — la necesitas en el Paso 2

---

## Paso 2 — Generar certificados

1. Abre `generator.html` con doble clic (se abre en el navegador)
2. En **Configuración del Evento** llena:
   - Nombre del evento
   - Fecha
   - Ciudad
   - URL de verificación (la URL de GitHub del Paso 1)
3. En **Firmantes** escribe los nombres y cargos, y sube las imágenes de las firmas
4. En **Participantes** escribe cada nombre y presiona Enter (o el botón +)
5. Haz clic en el nombre para ver la vista previa del certificado
6. Cuando estén todos listos, clic en **Descargar todos (ZIP)**

---

## Paso 3 — Activar la verificación por QR

1. En la herramienta, clic en **Exportar certs.json para GitHub**
2. Se descarga un archivo `certs.json`
3. Sube ese archivo al mismo repositorio de GitHub (`revem-certs`)
4. ¡Listo! Los QR de los certificados ya funcionan

---

## Preguntas frecuentes

**¿Puedo agregar más participantes después?**
Sí. Abre `generator.html`, llena los mismos datos del evento, agrega los nuevos nombres, genera sus certificados, y exporta un nuevo `certs.json` (que incluirá todos los anteriores si los vuelves a ingresar). *Recomendación: guarda la lista de nombres en un archivo de Word o Excel.*

**¿Los códigos son únicos?**
Sí. Cada certificado tiene un código tipo `REV-20260330-0001` con fecha y número de orden.

**¿El QR funciona sin internet?**
No. El QR apunta a GitHub Pages, que requiere conexión. El PDF y el código de barras funcionan offline.

**¿Cómo sé que el certificado es auténtico?**
El QR lleva a `verify.html` que consulta el `certs.json` en GitHub y muestra los datos del certificado si el código existe.
