# Cambridge · A tu aire

Guía de referencia en español para una estancia de tres semanas en Cambridge, Inglaterra. Contiene 72 lugares en seis categorías, con al menos la mitad de opciones locales en cada categoría. No es un itinerario.

## Abrir la guía

Abre `index.html` en un navegador. Conserva a su lado `styles.css`, `guide.js` y la carpeta `imágenes`. El contenido y las fotografías se leen sin conexión; los mapas y las páginas de visita requieren internet. Las fuentes tipográficas remotas son opcionales y tienen alternativas del sistema.

En un teléfono, resulta más cómodo abrir la versión web. Para trasladar la versión local, descomprime la carpeta completa: abrir únicamente el HTML sin sus imágenes no basta.

## Contenido y fotografías

`places.json` contiene las fichas, fuentes de visita, atribuciones y procedencia de cada fotografía. Los créditos también se pueden desplegar al pie de cada ficha. Las fotografías proceden de Wikimedia Commons, webs de los lugares y directorios locales. Las licencias varían; una atribución no equivale a una licencia abierta. Esta copia está preparada para consulta personal.

Las etiquetas clásico/local son una selección editorial, no mediciones de afluencia turística. Los lugares de barrio también pueden ser conocidos; se han priorizado opciones menos evidentes frente al circuito central. Todos se encuentran dentro de Cambridge, aunque los extremos de la ciudad pueden requerir caminatas largas. No se incluyen excursiones a pueblos cercanos.

Consulta las páginas enlazadas antes de visitar interiores de colleges, exposiciones o cafés. Horarios y entradas pueden cambiar. Las fotografías muestran el lugar real, pero algunas fueron tomadas años atrás.

## Actualizar

Edita `places.json` y ejecuta `python3 generate.py` para regenerar el HTML. `npm run build` crea una copia estática en `dist`. No requiere instalar dependencias. `npm run dev` inicia un servidor local en el puerto 4173.
