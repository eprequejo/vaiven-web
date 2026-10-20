# yavoy · web pública (yavoymalaga.com)

Transfer privado y chófer en Málaga y Costa del Sol. Web estática: HTML plano, CSS incrustado, 0 JS, fuentes autoalojadas. Se sirve con **GitHub Pages** desde la carpeta `docs/`.

```
src/   → fuentes (Python 3, sin librerías): datos, textos, estilos, generador y gate
docs/  → la web publicada (generada; NO se edita a mano)
```

| Fichero | Qué contiene |
|---|---|
| `src/config.py` | **Todos los datos del negocio** (marca, dominio, WhatsApp, nº VTC, CIF, reseñas…). Cada dato está una sola vez: la marca (`BRAND`) también, y el logotipo «ya» + V + «oy» se deriva de ella. |
| `src/content.py` | Textos ES y EN: portada, destinos, FAQ… Y la lista de idiomas (`LANGS`). |
| `src/content_i18n.py` | Textos DE, NL y FR. Atendemos en español e inglés: en estas páginas lo que va por WhatsApp (mensajes, chat de ejemplo) sale de la versión inglesa y se avisa junto al botón. |
| `src/legal.py` | Aviso legal y privacidad (solo ES, noindex) |
| `src/site.css` | Estilos (se incrustan minificados en cada página) |
| `src/build.py` | Generador |
| `src/check.py` | Gate de publicación: SEO, enlaces, huecos y peso |
| `src/test_check.py` | Tests del gate (cada rotura debe hacerlo fallar) |
| `src/make_assets.py` | Genera una vez favicon, icono iPhone e imágenes para redes (`src/static/`) |

## Cambiar algo
```bash
python3 src/build.py preview                      # → preview/, con los huecos en naranja
python3 -m http.server 8931 -d preview            # http://localhost:8931
python3 src/build.py prod                         # → docs/ ; si falta algo o check falla, NO toca docs/
python3 -m unittest src/test_check.py             # tests del gate
git add -A && git commit -m "…" && git push       # GitHub Pages publica en ~1 min
```
- Datos (teléfono, VTC, reseñas…): `src/config.py`. Textos: `src/content.py`.
- Reseñas: solo **reales** de Google, copiadas literalmente en `REVIEWS`. Sin reseñas, la sección no sale.
- Idiomas: `/` (es), `/en/`, `/de/`, `/nl/`, `/fr/`; x-default → `/en/`. Para añadir uno: su bloque en `content_i18n.py`, su nombre en `LANG_NAMES` y `python3 src/make_assets.py <ttf>` para su imagen de redes. Las legales siguen solo en español.
- Si cambia el contenido de verdad, actualiza `CONTENT_DATE` (va al `lastmod` del sitemap). No en cada build.

## Qué bloquea la publicación (`build.py prod`)
Faltan datos obligatorios (`REQUIRED` en config.py) · quedan huecos · JSON-LD inválido · FAQ visibles ≠ FAQPage · ≠1 `<h1>` · `lang` incorrecto · title >60 / description >160 · canonical o hreflang mal · sitemap ≠ páginas indexables · enlace o ancla rota · CSS/JS externo · ficheros internos en `docs/` · HTML >18 KB gzip, fuentes >80 KB, portada >120 KB.

## Puesta en marcha
1. Rellenar en `src/config.py` todo lo de `REQUIRED` → `python3 src/build.py prod` → commit + push.
2. GitHub → Settings → Pages: *Deploy from a branch* → `main` → `/docs` (ya configurado). Custom domain: el de `DOMAIN` (el build escribe `docs/CNAME`).
3. DNS del dominio:
   - `A` @ → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA` @ → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME` www → `eprequejo.github.io`
4. Cuando propague: **Enforce HTTPS**. Recomendado: verificar el dominio en *Settings de la cuenta → Pages → Verified domains*.

## Alta en buscadores (tras publicar con dominio)
1. **Google Business Profile** (lo más importante para «transfer Mijas / aeropuerto Málaga»): nombre «yavoy · Transfer Málaga», categoría principal *Servicio de transporte al aeropuerto*, secundaria *Servicio de chófer*; **nunca «Taxi»**. Zona de servicio sin dirección pública si no recibís clientes. Foto de perfil: la V sobre azul (`src/brand/favicon.svg`). Sin teléfono de llamadas (solo WhatsApp), o Google mostrará «Llamar». Su URL → `GOOGLE_REVIEWS_URL` en config.py (va a `sameAs` del JSON-LD y al enlace de reseñas).
2. **Google Search Console**: propiedad de dominio (registro TXT) → enviar `https://DOMINIO/sitemap.xml` → Inspección de URL → «Solicitar indexación» de `/` y `/en/`.
3. **Bing Webmaster Tools**: *Importar desde Google Search Console* (alimenta también Copilot y ChatGPT Search).
4. **IndexNow** tras cada cambio de contenido (solo las URLs que cambian): la clave está en `config.INDEXNOW_KEY` y se publica en `/<clave>.txt`:
   `https://api.indexnow.org/indexnow?url=https://DOMINIO/&key=<clave>`

## Medir
- Velocidad: PageSpeed Insights móvil de `/` y `/en/` → esperado ≥95 y LCP <2 s. En local (19-oct-2026, con datos de prueba): **100/100/100/100, LCP 1,4 s, CLS 0, TBT 0 ms**.
- Rich Results Test de `/` → LocalBusiness + FAQPage sin errores.
- Search Console: `/` y `/en/` «URL is on Google» a los 3-7 días.

## Notas
- Instagram: comprobar y registrar **@yavoymalaga** (a mano; Instagram no deja comprobarlo sin sesión).
- Sin cookies ni analítica → no hace falta banner. Si algún día se añade analítica con cookies, hará falta banner.
- **Hojas de quejas y reclamaciones:** la web no las menciona (decisión de Estela, 20-oct-2026): las quejas, por WhatsApp o email (aviso legal, «Quejas»). Si alguien pide la hoja oficial, se la mandáis por WhatsApp.
- Los textos legales son un borrador; que los revise la gestoría. Si sois S.L., añadir datos registrales en `src/legal.py`.
- El chat del hero es un ejemplo (matrícula 1234 ABC inventada). Sin nombres de personas en la web, por privacidad.
