# -*- coding: utf-8 -*-
"""python3 src/build.py prod|preview  ->  docs/ (lo que publica GitHub Pages)  o  preview/ (local, con huecos)

prod: si falta un dato obligatorio de config.py o check.py encuentra un fallo, no toca docs/ y sale con 1.
"""
import html, json, os, re, shutil, sys, tempfile
from urllib.parse import quote

import config as C
import check
from content import T, DEST, AREA
from legal import LEGAL

MODE = sys.argv[1] if len(sys.argv) > 1 else 'preview'
SRC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SRC)
OUT = os.path.join(REPO, 'docs' if MODE == 'prod' else 'preview')
HOLE = check.HOLE
FONTS = ['outfit-latin-wght.woff2', 'manrope-latin-wght.woff2']
PHOTO_EXT = ('.jpg', '.jpeg', '.png', '.webp')


# --- datos de config: un hueco se pinta visible en preview y nunca llega a prod ------------
def val(name):
    v = getattr(C, name)
    return f'{HOLE}{name}' if v in (None, '') else str(v)

def hv(name):
    """Valor para texto HTML: escapado, o marcado en naranja si es un hueco."""
    v = val(name)
    return f'<mark class="hole">{v}</mark>' if v.startswith(HOLE) else html.escape(v)

def esc(s):
    return html.escape(s, quote=True)

SITE = 'https://' + val('DOMAIN')

def phone_display():
    p = val('PHONE')
    if p.startswith(HOLE):
        return hv('PHONE')
    if p.startswith('34') and len(p) == 11:
        return f'+34 {p[2:5]} {p[5:8]} {p[8:]}'
    return '+' + p

def fmt(s):
    """Texto de content.py con {vtc} para HTML."""
    return s.format(vtc=hv('VTC_NO'))

def plain(s):
    """El mismo texto sin etiquetas, para JSON-LD (debe coincidir con lo visible)."""
    return re.sub(r'<[^>]+>', '', s.format(vtc=val('VTC_NO')))

def wa(text):
    return esc(f'https://wa.me/{val("PHONE")}?text={quote(text)}')


# --- iconos (SVG inline: cero peticiones) ---------------------------------------------------
def wa_icon(size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.7-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8c-1-.5-1.8-1.3-2.3-2.3l.8-1-1-2z" fill="currentColor"/></svg>')

CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l4 4L19 6" fill="none" stroke="#F0A202" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BRAND = os.path.join(SRC, 'brand')  # logo.svg y favicon.svg: única fuente del logo (make_assets.py lee los mismos)
LOGO = open(os.path.join(BRAND, 'logo.svg'), encoding='utf-8').read().strip().replace(
    'xmlns="http://www.w3.org/2000/svg"', 'width="30" height="30" aria-hidden="true"', 1)
DOT = '<svg width="8" height="8" viewBox="0 0 8 8" aria-hidden="true"><circle cx="4" cy="4" r="4" fill="#F0A202"/></svg>'


# --- CSS incrustado y minificado ------------------------------------------------------------
def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,>])\s*', r'\1', css)
    return css.replace(';}', '}').strip()

CSS = minify_css(open(os.path.join(SRC, 'site.css'), encoding='utf-8').read())

def minify_html(s):
    return re.sub(r'\n\s*', '\n', s).strip() + '\n'


# --- <head> ---------------------------------------------------------------------------------
INDEX = 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'
NOINDEX = 'noindex,follow'

def head(lang, title, desc, path, robots=INDEX, alternates=(), og=None, ld=None):
    url = SITE + path
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{SITE}{p}">\n' for h, p in alternates)
    pre = ''.join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in FONTS)
    ogs = ''
    if og:
        t = T[lang]
        other = 'en_GB' if lang == 'es' else 'es_ES'
        img = f'{SITE}/og{"" if lang == "es" else "-en"}.jpg'
        ogs = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="Vaivén">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{other}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(t['og_title'])}">
<meta property="og:description" content="{esc(t['og_desc'])}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(t['og_title'])}">
<meta name="twitter:card" content="summary_large_image">
'''
    lds = ''
    if ld:
        graph = json.dumps({'@context': 'https://schema.org', '@graph': ld}, ensure_ascii=False, separators=(',', ':'))
        graph = graph.replace('</', '<\\/')
        lds = f'<script type="application/ld+json">{graph}</script>\n'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#0E2B40">
<!-- Verificación (si no se usa la del DNS): -->
<!-- <meta name="google-site-verification" content="CODIGO_GSC"> -->
<!-- <meta name="msvalidate.01" content="CODIGO_BING"> -->
{ogs}{pre}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>{CSS}</style>
{lds}</head>
'''


# --- piezas comunes -------------------------------------------------------------------------
def header(lang):
    t = T[lang]
    base = t['path']
    links = ''.join(f'<a href="{base}{h}">{n}</a>' for h, n in t['nav'])
    if lang == 'es':
        sw = '<a class="lang" href="/en/" hreflang="en" lang="en">EN</a>'
    else:
        sw = '<a class="lang" href="/" hreflang="es" lang="es">ES</a>'
    return f'''<header class="nav">
<div class="wrap">
<a class="brand" href="{base}" aria-label="{t['home_label']}">{LOGO}Vaivén</a>
<nav class="nav-links" aria-label="{t['nav_label']}">{links}</nav>
<div class="nav-right">
{sw}
<a class="btn btn-wa btn-sm" href="{wa(t['wa_generic'])}">{wa_icon(18)}{t['cta_nav']}</a>
</div>
</div>
</header>
'''

def footer(lang):
    t = T[lang]
    tr = ''.join(f'<a href="{t["path"]}#destinos">{n}</a>' for n in t['footer_links'])
    lg = ''.join(f'<a href="/{slug}/">{p["title"]}</a>' for slug, p in LEGAL.items())
    return f'''<footer>
<div class="wrap">
<div class="col">
<span class="brand-f">Vaivén</span>
<span>{t['footer_tag']}</span>
<span>{fmt(t['footer_vtc'])}</span>
<span>{hv('RAZON_SOCIAL')} · {hv('CIF')}</span>
</div>
<div class="col"><strong>{t['footer_transfers']}</strong>{tr}</div>
<div class="col"><strong>{t['footer_legal']}</strong>{lg}</div>
</div>
</footer>
<a class="wa-float" href="{wa(t['wa_generic'])}" aria-label="{t['wa_float']}">{wa_icon(28)}</a>
</body>
</html>
'''


# --- equipo: fotos de src/photos/<slug>.jpg -> assets/img/<slug>.webp ---------------------
def photo_src(slug):
    for ext in PHOTO_EXT:
        p = os.path.join(SRC, 'photos', slug + ext)
        if os.path.exists(p):
            return p
    return None

def build_photos(out):
    for m in C.TEAM:
        src = photo_src(m['slug'])
        if not src:
            continue
        from PIL import Image, ImageOps  # solo hace falta en la máquina que genera, no en la web
        os.makedirs(os.path.join(out, 'assets', 'img'), exist_ok=True)
        im = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert('RGB'), (400, 500), Image.LANCZOS)
        im.save(os.path.join(out, 'assets', 'img', m['slug'] + '.webp'), 'WEBP', quality=78, method=6)


# --- JSON-LD --------------------------------------------------------------------------------
def ld_home(lang):
    t = T[lang]
    url = SITE + t['path']
    biz = {
        '@type': 'LocalBusiness', '@id': SITE + '/#business', 'name': 'Vaivén',
        'description': t['ld_desc'], 'url': SITE + '/', 'email': val('EMAIL'),
        'image': SITE + '/og.jpg', 'logo': SITE + '/apple-touch-icon.png', 'priceRange': '€€',
        'currenciesAccepted': 'EUR', 'paymentAccepted': t['payment'], 'knowsLanguage': ['es', 'en'],
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Mijas', 'addressRegion': 'Málaga', 'addressCountry': 'ES'},
        'areaServed': [{'@type': 'City', 'name': a} for a in AREA],
        'openingHoursSpecification': {'@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'opens': '00:00', 'closes': '23:59'},
        # Solo WhatsApp: sin 'telephone', para que Google no ofrezca un botón de llamar.
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'reservations', 'url': f'https://wa.me/{val("PHONE")}',
                         'availableLanguage': ['es', 'en']},
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': o}} for o in t['offers']],
    }
    if C.GEO:
        biz['geo'] = {'@type': 'GeoCoordinates', 'latitude': C.GEO[0], 'longitude': C.GEO[1]}
    same = list(C.SAME_AS) + ([C.GOOGLE_REVIEWS_URL] if C.GOOGLE_REVIEWS_URL else [])
    if same:
        biz['sameAs'] = list(dict.fromkeys(same))
    web = {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Vaivén',
           'inLanguage': ['es', 'en'], 'publisher': {'@id': SITE + '/#business'}}
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': t['title'], 'description': t['desc'],
            'inLanguage': lang, 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#business'}}
    # Misma lista que las FAQ visibles: no pueden divergir.
    faq = {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in t['faq']]}
    return [biz, web, page, faq]


# --- portada (ES y EN) ----------------------------------------------------------------------
def home(lang):
    t = T[lang]
    alternates = [('es', '/'), ('en', '/en/'), ('x-default', '/')]
    out = head(lang, t['title'], t['desc'], t['path'], alternates=alternates, og=True, ld=ld_home(lang))
    out += '<body>\n' + header(lang) + '<main>\n'

    checks = ''.join(f'<span>{CHECK}{fmt(c)}</span>' for c in t['checks'])
    chat = ''.join(f'<div class="msg {who}">{fmt(m)}</div>' for who, m in t['chat'])
    out += f'''<section id="top" class="hero">
<div class="wrap">
<div class="hero-copy">
<span class="eyebrow on-dark">{DOT}{t['eyebrow']}</span>
<h1>{t['h1']}</h1>
<p class="summary">{t['summary']}</p>
<p class="promise">{t['promise']}</p>
<div class="hero-cta">
<a class="btn btn-wa" href="{wa(t['wa_hero'])}">{wa_icon(20)}{t['cta_hero']}</a>
</div>
<p class="sub">{t['sub']}</p>
<div class="hero-checks">{checks}</div>
</div>
<div class="chat" role="img" aria-label="{t['chat_label']}">
<div class="chat-head"><div class="chat-avatar" aria-hidden="true">J</div><div><span class="chat-name">Juan · Vaivén</span><span class="chat-status">{t['chat_status']}</span></div></div>
{chat}
</div>
</div>
</section>
'''
    strip = list(t['strip'])
    if C.GOOGLE_REVIEWS_COUNT:
        r = t['strip_reviews'].format(n=C.GOOGLE_REVIEWS_COUNT)
        strip.insert(0, f'<a href="{esc(C.GOOGLE_REVIEWS_URL)}">{r}</a>' if C.GOOGLE_REVIEWS_URL else r)
    out += f'<section class="strip" aria-label="{t["strip_label"]}"><div class="wrap">' + ''.join(f'<span>{s}</span>' for s in strip) + '</div></section>\n'

    steps = ''.join(f'<div class="card"><span class="step-num">{i}</span><h3>{h}</h3><p class="dest-note">{p}</p></div>' for i, (h, p) in enumerate(t['steps'], 1))
    out += f'''<section id="como" class="section">
<div class="wrap">
<div class="section-head"><span class="eyebrow">{t['how_eyebrow']}</span><h2>{t['how_h2']}</h2><p class="lead">{t['how_lead']}</p></div>
<div class="grid-3">{steps}</div>
</div>
</section>
'''
    cards = ''
    for d in DEST:
        name, note, to = d[lang]
        cards += (f'<a class="card dest" href="{wa(t["dest_wa"].format(to=to))}">'
                  f'<div class="dest-top"><h3>{name}</h3><span class="dest-time">{d["min"]} min</span></div>'
                  f'<p class="dest-note">{note}</p><span class="dest-cta">{t["dest_cta"]}</span></a>\n')
    chips = ''.join(f'<a class="chip" href="{wa(m)}">{n}</a>' for n, m in t['chips'])
    out += f'''<section id="destinos" class="section sand">
<div class="wrap">
<div class="section-head"><span class="eyebrow">{t['dest_eyebrow']}</span><h2>{t['dest_h2']}</h2><p class="lead">{t['dest_lead']}</p></div>
<div class="grid-3">
{cards}</div>
<div class="chips"><strong>{t['also']}</strong>{chips}</div>
</div>
</section>
'''
    people = ''
    all_photos = all(photo_src(m['slug']) for m in C.TEAM)
    for m in C.TEAM:
        img = ''
        if photo_src(m['slug']):
            img = (f'<img class="photo" src="/assets/img/{m["slug"]}.webp" alt="{m["name"]}, {t["role_alt"][m["role"]]}" '
                   f'width="400" height="500" loading="lazy" decoding="async">')
        bits = [t['roles'][m['role']]] + [x[lang] for x in (m['langs'], m['bio']) if x and x.get(lang)]
        people += f'<div class="person">{img}<h3>{m["name"]}</h3><p>{esc(" ".join(bits))}</p></div>\n'
    lead = (t['team_lead_photos'] if all_photos else '') + t['team_lead']
    out += f'''<section id="equipo" class="section team">
<div class="wrap">
<div class="section-head"><span class="eyebrow on-dark">{t['team_eyebrow']}</span><h2>{t['team_h2']}</h2><p class="lead">{lead}</p></div>
<div class="grid-3">
{people}</div>
</div>
</section>
'''
    if C.REVIEWS:
        quotes = ''
        for r in C.REVIEWS:
            la = f' lang="{r["lang"]}"' if r.get('lang') and r['lang'] != lang else ''
            quotes += (f'<blockquote class="card"{la}><span class="stars" role="img" aria-label="{t["stars_label"]}">★★★★★</span>'
                       f'<p>{esc(r["text"])}</p><cite>{esc(r["name"])} · {esc(r["route"])}</cite></blockquote>\n')
        more = f'<a href="{esc(C.GOOGLE_REVIEWS_URL)}">{t["reviews_all"]}</a>' if C.GOOGLE_REVIEWS_URL else ''
        out += f'''<section class="section" aria-labelledby="reviews-title">
<div class="wrap">
<div class="reviews-head"><h2 id="reviews-title">{t['reviews_h2']}</h2>{more}</div>
<div class="grid-3">
{quotes}</div>
</div>
</section>
'''
    faq = ''.join(f'<details><summary>{fmt(q)}</summary><p>{fmt(a)}</p></details>\n' for q, a in t['faq'])
    out += f'''<section id="faq" class="section sand faq">
<div class="wrap">
<h2>{t['faq_h2']}</h2>
<div>
{faq}</div>
</div>
</section>
<section class="section">
<div class="wrap">
<div class="cta-box">
<div><h2>{t['cta_h2']}</h2><p>{t['cta_p']}</p></div>
<a class="btn btn-navy" href="{wa(t['wa_generic'])}">{wa_icon(20)}{t['cta_final']}</a>
</div>
</div>
</section>
</main>
'''
    return out + footer(lang)


# --- páginas legales (solo ES, noindex) y 404 --------------------------------------------
def legal_page(slug):
    p = LEGAL[slug]
    body = p['body'].format(**{k: hv(k) for k in ('RAZON_SOCIAL', 'CIF', 'LEGAL_ADDRESS', 'EMAIL', 'VTC_NO', 'DOMAIN')},
                            PHONE=phone_display(), CONTENT_DATE=C.CONTENT_DATE)
    out = head('es', f'{p["title"]} · Vaivén', p['desc'], f'/{slug}/', robots=NOINDEX)
    return out + '<body>\n' + header('es') + f'<main class="wrap doc">\n<h1>{p["title"]}</h1>\n{body}\n</main>\n' + footer('es')

def page_404():
    out = head('es', 'Página no encontrada · Vaivén', 'Esta página no existe. Vuelve al inicio de Vaivén, transfer privado en Málaga y Costa del Sol.', '/404.html', robots=NOINDEX)
    return out + '<body>\n' + header('es') + f'''<main class="wrap doc">
<h1>Esta página no existe</h1>
<p>Puede que el enlace esté mal escrito o que la página se haya movido.</p>
<p><a href="/">Ir al inicio</a> · <a href="/en/" lang="en" hreflang="en">Go to the English version</a></p>
<a class="btn btn-wa" href="{wa(T['es']['wa_generic'])}">{wa_icon(20)}{T['es']['cta_nav']}</a>
</main>
''' + footer('es')


# --- ficheros de indexación ------------------------------------------------------------------
def robots_txt():
    return f'''# Vaivén · robots.txt
# Política: la tienda abierta. Buscadores y asistentes de IA (búsqueda, citas y entrenamiento)
# pueden leer toda la web; que nos citen es lo que buscamos. No hay zonas privadas que proteger:
# las páginas legales llevan noindex en su propia etiqueta, no aquí (si se bloquearan, Google
# no podría ver ese noindex).
User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
'''

def sitemap_xml():
    urls = ''
    for lang in ('es', 'en'):
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{p}"/>' for h, p in (('es', '/'), ('en', '/en/'), ('x-default', '/')))
        urls += f'<url><loc>{SITE}{T[lang]["path"]}</loc><lastmod>{C.CONTENT_DATE}</lastmod>{alts}</url>\n'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + urls + '</urlset>\n')


# --- montaje --------------------------------------------------------------------------------
def write(out, rel, content):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(minify_html(content) if rel.endswith('.html') else content)

def build(out):
    write(out, 'index.html', home('es'))
    write(out, 'en/index.html', home('en'))
    for slug in LEGAL:
        write(out, f'{slug}/index.html', legal_page(slug))
    write(out, '404.html', page_404())
    write(out, 'robots.txt', robots_txt())
    write(out, 'sitemap.xml', sitemap_xml())
    write(out, f'{C.INDEXNOW_KEY}.txt', C.INDEXNOW_KEY)
    write(out, '.nojekyll', '')
    if C.DOMAIN:
        write(out, 'CNAME', C.DOMAIN + '\n')
    shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(out, 'assets'), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(SRC, 'static')):
        shutil.copy(os.path.join(SRC, 'static', f), os.path.join(out, f))
    shutil.copy(os.path.join(BRAND, 'favicon.svg'), os.path.join(out, 'favicon.svg'))
    build_photos(out)

def main():
    if MODE not in ('prod', 'preview'):
        sys.exit('uso: python3 src/build.py prod|preview')
    if MODE == 'prod':
        missing = [n for n in C.REQUIRED if getattr(C, n) in (None, '')]
        if missing:
            print('NO SE PUBLICA: faltan datos obligatorios en src/config.py:')
            for n in missing:
                print('  -', n)
            sys.exit(1)
        tmp = tempfile.mkdtemp(prefix='vaiven-')
        build(tmp)
        errors = check.run(tmp, domain=C.DOMAIN)
        if errors:
            print('NO SE PUBLICA: check.py ha encontrado fallos (docs/ sin tocar):')
            for e in errors:
                print('  -', e)
            shutil.rmtree(tmp)
            sys.exit(1)
        shutil.rmtree(OUT, ignore_errors=True)
        shutil.move(tmp, OUT)
        print(f'OK: docs/ generado y verificado ({SITE})')
    else:
        shutil.rmtree(OUT, ignore_errors=True)
        build(OUT)
        errors = check.run(OUT, allow_holes=True)
        holes = check.holes(OUT)
        print(f'preview/ generado · huecos pendientes: {", ".join(holes) or "ninguno"}')
        for e in errors:
            print('  FALLO -', e)
        sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
