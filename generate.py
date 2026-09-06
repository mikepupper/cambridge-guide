import json,html,shutil
from pathlib import Path
from urllib.parse import urlencode
root=Path(__file__).resolve().parent
H=lambda value:html.escape(str(value),quote=True)
categories=[
 ('simbolos','Símbolos e historia','Símbolos','Los grandes colleges y el patrimonio que se esconde a su alrededor.'),
 ('locales','El Cambridge más local','Vida local','Barrios, pasajes y espacios con vida propia, más allá de la postal.'),
 ('parques','Una pausa en verde','Parques','Praderas junto al Cam, jardines y rincones para abrir un libro.'),
 ('cultura','Arte, ciencia y libros','Cultura','Colecciones extraordinarias, pequeñas galerías y librerías para perder la noción del tiempo.'),
 ('miradores','Pararse a mirar','Contemplar','Torres, puentes y orillas donde merece la pena quedarse un rato.'),
 ('cafes','Café con carácter','Cafés','Cafeterías independientes de Cambridge: algunas célebres, otras de barrio.')
]
places=json.loads((root/'places.json').read_text())
nav=''.join(f'<a href="#{cid}" aria-current="{str(i==0).lower()}"><span class="nav-number">0{i+1}</span>{short}</a>' for i,(cid,title,short,desc) in enumerate(categories))
sections=[]
for i,(cid,title,short,desc) in enumerate(categories):
 group=[p for p in places if p['category']==cid]
 if not group:continue
 cards=[]
 for j,p in enumerate(group):
  url='https://www.google.com/maps/dir/?'+urlencode({'api':'1','destination':p['name']+', '+p['address']+', Cambridge, England','travelmode':'walking'})
  credit=p.get('attribution','Fotografía del lugar. Consulta la fuente original.')
  cards.append(f'''<article class="card" data-lat="{p['lat']}" data-lng="{p['lng']}">
   <figure class="photo"><img src="{H(p['image'])}" alt="{H(p.get('alt',p['name']+' en Cambridge'))}" width="720" height="480" loading="{'eager' if i==0 and j==0 else 'lazy'}" decoding="async"><span class="tag {'local' if p['local'] else ''}">{'↗ Espíritu local' if p['local'] else '✦ Clásico / imperdible'}</span></figure>
   <div class="card-body"><p class="card-meta">{short}</p><h3>{H(p['name'])}</h3><p class="description">{H(p['description'])}</p>{('<p class="practical">'+H(p['practical'])+'</p>') if p.get('practical') else ''}<p class="address">{H(p['address'])}</p><p class="distance" hidden></p></div>
   <div class="card-bottom"><a class="map-link" href="{H(url)}" target="_blank" rel="noopener noreferrer" aria-label="Cómo llegar a pie a {H(p['name'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m21 3-7 18-3-8-8-3 18-7Z"/><path d="m11 13 10-10"/></svg>Cómo llegar a pie</a><a class="source-link" href="{H(p['source'])}" target="_blank" rel="noopener noreferrer" aria-label="Información de visita: {H(p['name'])}">Visita ↗</a></div>
   <details class="photo-credit"><summary>Crédito de la fotografía</summary><p>{H(credit)} <a href="{H(p['image_source'])}" target="_blank" rel="noopener noreferrer">Fuente original ↗</a></p></details>
  </article>''')
 sections.append(f'<section class="category" id="{cid}" aria-labelledby="title-{cid}"><header class="section-heading"><div><span class="section-number">Capítulo 0{i+1}</span><h2 id="title-{cid}">{title}</h2><p>{desc}</p></div><span class="count">{len(group)} lugares · {sum(p["local"] for p in group)} locales</span></header><div class="cards">'+''.join(cards)+'</div></section>')
page=f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#264f43"><meta name="description" content="Guía de bolsillo de Cambridge: {len(places)} lugares a pie, entre clásicos y rincones locales. Parques, cultura, miradores y cafés independientes con fotografías y mapas."><title>Cambridge · Guía de bolsillo</title><link rel="stylesheet" href="styles.css"><script src="guide.js" defer></script></head>
<body id="arriba"><a class="skip" href="#guia">Saltar a los lugares</a><header class="masthead"><a class="wordmark" href="#arriba">Cambridge<span>GUÍA DE BOLSILLO</span></a><button type="button" class="surprise-btn" id="surprise-btn">Sorpréndeme</button></header>
<div class="intro"><p class="intro-lead">Una guía para tus tres semanas: elige un rincón según lo que te apetezca hoy, sin horarios ni días asignados.</p><div class="stats"><span><strong>{len(places)}</strong> lugares</span><span><strong>6</strong> categorías</span><span><strong>{sum(p['local'] for p in places)}</strong> con espíritu local</span></div><button type="button" class="locate-btn" id="locate-btn">Activar distancias a tu ubicación</button></div>
<nav class="category-nav" aria-label="Categorías de lugares"><div class="nav-inner">{nav}</div></nav>
<section id="surprise-view" class="surprise-view" hidden aria-label="Lugar sorpresa"><button type="button" class="back-btn" id="surprise-back">← Volver</button><div id="surprise-card"></div></section>
<main class="guide" id="guia">{''.join(sections)}
<aside class="guide-note"><h2>Un par de cosas<br>antes de salir.</h2><div><p>Todos los lugares están dentro de Cambridge. Las distancias cambian según dónde te alojes: algunos rincones de barrio requieren una caminata más larga desde el centro. «Cómo llegar» calcula una ruta a pie desde tu ubicación en Google Maps.</p><p>«Espíritu local» señala opciones menos obvias o ligadas a la vida de barrio; no significa que sean secretas ni que no reciban visitantes. Representan al menos la mitad de cada categoría.</p><p>Los colleges son espacios de estudio: el acceso puede cambiar por exámenes, ceremonias o servicios religiosos. Consulta «Visita» antes de salir, especialmente para interiores, exposiciones y cafés. No se fijan precios ni horarios para evitar que la guía quede desactualizada.</p><p>Textos y fuentes consultados en septiembre de 2026. Cada fotografía tiene su fuente y atribución en la ficha; algunas imágenes son históricas y la apariencia actual puede variar.</p></div></aside><a class="back-top" href="#arriba">↑ Volver al principio</a></main>
<footer class="footer"><span>Cambridge · Guía de bolsillo · Septiembre 2026</span><span>Para pasear sin prisa.</span></footer></body></html>'''
(root/'index.html').write_text(page)
print(f'Generated {len(places)} places')
