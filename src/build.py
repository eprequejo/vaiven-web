# -*- coding: utf-8 -*-
"""python3 src/build.py prod|preview  ->  docs/ (lo que publica GitHub Pages)  o  preview/ (local, con huecos)

prod: si falta un dato obligatorio de config.py o check.py encuentra un fallo, no toca docs/ y sale con 1.
"""
import html, json, os, re, shutil, sys, tempfile
from urllib.parse import quote

import config as C
import check
from content import T, DEST, AREA, INCLUDED_LABELS, LANGS, LANG_NAMES
from legal import LEGAL

MODE = sys.argv[1] if len(sys.argv) > 1 else 'preview'
SRC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SRC)
OUT = os.path.join(REPO, 'docs' if MODE == 'prod' else 'preview')
HOLE = check.HOLE
FONTS = ['outfit-latin-wght.woff2', 'manrope-latin-wght.woff2']


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

def fmt(s, **extra):
    """Texto de content.py con {vtc} (y los campos de extra) para HTML."""
    return s.format(vtc=hv('VTC_NO'), **extra)

def plain(s, **extra):
    """El mismo texto sin etiquetas, para JSON-LD (debe coincidir con lo visible)."""
    return re.sub(r'<[^>]+>', '', s.format(vtc=val('VTC_NO'), **extra))


# --- lo incluido y la FAQ: una fuente para el <details> y el FAQPage -------------------------
def and_list(items, lang, serial=False):
    """«a, b y c» en el idioma de la página. serial: coma también antes de la «y» (cuando los elementos ya llevan «y»)."""
    if len(items) < 2:
        return ''.join(items)
    return ', '.join(items[:-1]) + (',' if serial else '') + f" {T[lang]['and_word']} " + items[-1]

def included_text(lang):
    return and_list([INCLUDED_LABELS[k][lang] for k in (C.INCLUDED or [])], lang)

# hreflang de las portadas (HTML y sitemap). x-default → inglés: en la Costa del Sol el visitante que no habla
# español (alemán, neerlandés, escandinavo…) entiende antes el inglés.
ALTERNATES = [(l, T[l]['path']) for l in LANGS] + [('x-default', T['en']['path'])]

GROUP_N = 10  # el grupo del ejemplo (sección Grupos y FAQ)

def group_example():
    """(personas, coches) del ejemplo: los coches salen de MAX_PAX, no se escriben a mano (10 → 3 coches de 4)."""
    return GROUP_N, (-(-GROUP_N // C.MAX_PAX) if C.MAX_PAX else None)

def group_types_text(lang):
    """«bodas e invitados, grupos de golf, … y empresas o eventos»: la misma lista que las tarjetas de Grupos."""
    return and_list([g[1] for g in T[lang]['group_types']], lang, serial=True)

def faq_items(lang):
    """[(pregunta, respuesta, campos)] que se pintan: fuera las que piden un dato que falta en config."""
    n, cars = group_example()
    extra = {'included': included_text(lang), 'pax': C.MAX_PAX, 'group_n': n, 'group_cars': cars,
             'group_types': group_types_text(lang)}
    return [(q, a, extra) for q, a, needs in T[lang]['faq'] if all(getattr(C, n) for n in needs)]


def wa(text):
    return esc(f'https://wa.me/{val("PHONE")}?text={quote(text)}')


# --- iconos (SVG inline: cero peticiones) ---------------------------------------------------
def wa_icon(size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.7-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8c-1-.5-1.8-1.3-2.3-2.3l.8-1-1-2z" fill="currentColor"/></svg>')

CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l4 4L19 6" fill="none" stroke="#F0A202" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

BRAND = os.path.join(SRC, 'brand')  # logo.svg y favicon.svg: única fuente del logo (make_assets.py lee los mismos)
LOGO = read(os.path.join(BRAND, 'logo.svg')).strip().replace(
    'xmlns="http://www.w3.org/2000/svg"', 'class="wm-v" aria-hidden="true"', 1)
# El favicon tal cual (la V sobre azul): avatar del chat de ejemplo
FAVICON = read(os.path.join(BRAND, 'favicon.svg')).strip()

def wordmark(on_dark=False):
    """«ya» + V del logo + «oy», en una pieza (Outfit 800). Sobre azul, el trazo izquierdo va en crema."""
    left, right = C.BRAND.split('v', 1)
    v = re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{C.WM_V["stroke"]}"', LOGO)
    v = v.replace('#0E2B40', '#FBF8F2') if on_dark else v
    # El dibujo se oculta al lector y el nombre va como texto oculto a la vista: así el nombre accesible
    # coincide con el texto (WCAG 2.5.3) y la V no se lee como «ya oy».
    return f'<span class="wm" aria-hidden="true">{left}{v}{right}</span><span class="vh">{C.BRAND}</span>'
DOT = '<svg width="8" height="8" viewBox="0 0 8 8" aria-hidden="true"><circle cx="4" cy="4" r="4" fill="#F0A202"/></svg>'


# --- CSS incrustado y minificado ------------------------------------------------------------
def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,>])\s*', r'\1', css)
    return css.replace(';}', '}').strip()

CSS = minify_css(read(os.path.join(SRC, 'site.css')))
for _k, _v in ((k, v) for k, v in C.WM_V.items() if k != 'stroke'):
    CSS = CSS.replace(f'%WM_{_k.upper()}%', f'{_v:g}')

WA_LINK = re.compile(r'<a ([^>]*href="https://wa\.me/[^"]*")')

def wa_new_tab(s):
    """Todo enlace a WhatsApp abre en pestaña nueva (Estela, 19-oct): un solo sitio, no en cada <a>."""
    return WA_LINK.sub(r'<a target="_blank" rel="noopener" \1', s)

def minify_html(s):
    return re.sub(r'\n\s*', '\n', s).strip() + '\n'


# --- <head> ---------------------------------------------------------------------------------
def _icon_version():
    """Huella de los iconos: si cambia el logo, cambia la URL y el navegador deja su caché (son muy pegajosos)."""
    import hashlib
    h = hashlib.sha1()
    for p in (os.path.join(BRAND, 'favicon.svg'), os.path.join(SRC, 'static', 'favicon.ico'), os.path.join(SRC, 'static', 'apple-touch-icon.png')):
        with open(p, 'rb') as f:
            h.update(f.read())
    return h.hexdigest()[:8]

ICON_V = _icon_version()

def og_image(lang):
    """Imagen para redes de cada idioma (la generan make_assets.py): og.jpg la raíz, og-<lang>.jpg el resto."""
    return 'og.jpg' if lang == LANGS[0] else f'og-{lang}.jpg'
INDEX = 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'
NOINDEX = 'noindex,follow'

def head(lang, title, desc, path, robots=INDEX, alternates=(), og=None, ld=None):
    url = SITE + path
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{SITE}{p}">\n' for h, p in alternates)
    pre = ''.join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in FONTS)
    ogs = ''
    if og:
        t = T[lang]
        others = ''.join(f'<meta property="og:locale:alternate" content="{T[l]["locale"]}">\n' for l in LANGS if l != lang)
        img = f'{SITE}/{og_image(lang)}'
        ogs = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="{C.BRAND}">
<meta property="og:locale" content="{t['locale']}">
{others}<meta property="og:url" content="{url}">
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
{ogs}{pre}<link rel="icon" href="/favicon.svg?v={ICON_V}" type="image/svg+xml">
<link rel="icon" href="/favicon.ico?v={ICON_V}" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={ICON_V}">
<style>{CSS}</style>
{lds}</head>
'''


# --- piezas comunes -------------------------------------------------------------------------
def header(lang):
    t = T[lang]
    base = t['path']
    # #grupos solo existe si hay MAX_PAX (los coches del ejemplo salen de ahí)
    links = ''.join(f'<a href="{base}{h}">{n}</a>' for h, n in t['nav'] if h != '#grupos' or C.MAX_PAX)
    # Selector de idioma sin JS: <details> con un enlace por idioma (hreflang/lang en cada uno)
    opts = ''.join(f'<a href="{T[l]["path"]}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{LANG_NAMES[l]}</a>'
                   for l in LANGS)
    sw = f'<details class="langs"><summary class="lang">{lang.upper()}<span class="vh"> {LANG_NAMES[lang]}</span></summary><div class="langs-menu">{opts}</div></details>'
    return f'''<header class="nav">
<div class="wrap">
<a class="brand" href="{base}">{wordmark()}</a>
<nav class="nav-links" aria-label="{t['nav_label']}">{links}</nav>
<div class="nav-right">
{sw}
{share_link(lang, 'share_nav', 'share btn btn-sm btn-line share-nav')}
<a class="btn btn-wa btn-sm nav-cta" href="{wa(t['wa_generic'])}">{wa_icon(18)}{t['cta_nav']}</a>
</div>
</div>
</header>
{SHARE_JS}
'''

# Botón flotante: escondido mientras se ve el buscador «¿A dónde vas?» (ya es el CTA). Sin JS o sin buscador, siempre visible.
FLOAT_JS = ("<script>(function(){var f=document.querySelector('.wa-float'),g=document.querySelector('form.go');"
            "if(f&&g&&'IntersectionObserver'in window)new IntersectionObserver(function(e){"
            "f.classList.toggle('off',e[0].isIntersecting)}).observe(g)})()</script>")

def footer(lang):
    t = T[lang]
    lg = ''.join(f'<a href="/{slug}/">{p["title"]}</a>' for slug, p in LEGAL.items())
    return f'''<footer>
<div class="wrap">
<div class="col">
<span class="brand-f">{wordmark(on_dark=True)}</span>
<span>{t['footer_tag']}</span>
<span>{fmt(t['footer_vtc'])}</span>
<span>WhatsApp: {phone_display()}</span>
<span>{hv('RAZON_SOCIAL')} · {hv('CIF')}</span>
</div>
<div class="col"><strong>{t['footer_legal']}</strong>{lg}</div>
</div>
</footer>
<a class="wa-float" href="{wa(t['wa_generic'])}" aria-label="{t['wa_float']}">{wa_icon(28)}</a>
{FLOAT_JS}
</body>
</html>
'''


# --- «¿A dónde vas?» → WhatsApp con el destino ya escrito ----------------------------------
# Sin JS el formulario va igual a wa.me con el mensaje genérico. El destino solo viaja a WhatsApp.
# Con JS el enlace se arma con encodeURIComponent (espacios como %20, no «+», que es lo que manda un form GET).
GO_JS = ("<script>document.querySelectorAll('form.go').forEach(function(f){f.addEventListener('submit',function(e){"
         "var d=f.querySelector('.go-dest').value.trim(),h=f.querySelector('[name=text]'),s=d?f.dataset.to+d:'';"
         "if(f.dataset.al)s=s.replace(/^ a el /i,' al ');e.preventDefault();"
         "window.open(f.action+'?text='+encodeURIComponent(h.dataset.msg+s),'_blank','noopener')})})</script>")

def go_form(lang):
    t = T[lang]
    al = ' data-al="1"' if lang == 'es' else ''  # «a el aeropuerto» → «al aeropuerto»
    # DE/NL/FR: atendemos en español e inglés y el mensaje sale en inglés: se dice junto al botón
    note = f'<p class="go-note">{t["lang_note"]}</p>' if t.get('lang_note') else ''
    return f'''<form class="go" action="https://wa.me/{esc(val('PHONE'))}" method="get" target="_blank" data-to="{esc(t['wa_to'])}"{al}>
<label class="go-label" for="go-{lang}">{t['go_q']}</label>
<div class="go-row"><input id="go-{lang}" class="go-dest" type="text" autocomplete="off" enterkeyhint="go" maxlength="80" placeholder="{esc(t['go_ph'])}">
<input type="hidden" name="text" value="{esc(t['wa_generic'])}" data-msg="{esc(t['wa_generic'])}">
<button class="btn btn-wa" type="submit">{wa_icon(20)}{t['cta_hero']}</button></div>
<p class="go-alt">{t['wa_alt']} <strong>{phone_display()}</strong></p>{note}
</form>
{GO_JS}
'''


# --- «Pásaselo a quien venga»: menú nativo de compartir en el móvil; si no hay, WhatsApp sin destinatario ---
SHARE_ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3m0 0L7.5 7.5M12 3l4.5 4.5'
              'M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')
# Solo «text», con el enlace dentro: si se pasa «url» aparte, WhatsApp se queda solo con el enlace (19-oct).
# Delegado en document: va una vez por página (en la cabecera) y sirve a todos los botones, también a los de abajo.
SHARE_JS = ("<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.share');"
            "if(!a||!navigator.share)return;e.preventDefault();"
            "navigator.share({text:a.dataset.text}).catch(function(){})})</script>")

def share_link(lang, label_key='share_btn', cls='share'):
    """Botón de compartir. Mismo texto y destino en la cabecera y en el bloque final: solo cambia la etiqueta."""
    t = T[lang]
    url = SITE + t['path']
    text = f"{t['share_text']} {url}"
    href = 'https://wa.me/?text=' + quote(text)
    return (f'<a class="{cls}" href="{esc(href)}" data-text="{esc(text)}" aria-label="{t[label_key]}">'
            f'{SHARE_ICON}<span>{t[label_key]}</span></a>')


# --- «yavoy en pocas palabras»: cada valor sale de config/content, nada escrito dos veces ------
def facts(lang):
    t = T[lang]
    rows = [('base', f'{C.BASE_TOWN} ({C.BASE_REGION})'), ('vtc', hv('VTC_NO')),
            ('area', f"{', '.join(AREA)} {t['area_more']}"), ('hours', t['hours']),
            ('langs', t['langs'][0].upper() + t['langs'][1:])]
    if C.MAX_PAX:
        rows.append(('pax', t['pax_value'].format(n=C.MAX_PAX)))
        rows.append(('groups', t['groups_value']))
    rows += [('book', t['book_value']), ('pay', f"{t['payment']} · {t['pay_when']}")]
    dl = ''.join(f'<div><dt>{t["facts"][k]}</dt><dd>{v}</dd></div>' for k, v in rows)
    return f'<div class="facts"><h3>{t["facts_h"]}</h3><dl>{dl}</dl></div>'


# --- JSON-LD --------------------------------------------------------------------------------
def ld_home(lang):
    t = T[lang]
    url = SITE + t['path']
    biz = {
        '@type': 'LocalBusiness', '@id': SITE + '/#business', 'name': C.BRAND,
        'description': t['ld_desc'], 'url': SITE + '/', 'email': val('EMAIL'),
        'image': SITE + '/og.jpg', 'logo': SITE + '/apple-touch-icon.png',
        'currenciesAccepted': 'EUR', 'paymentAccepted': t['payment'], 'knowsLanguage': ['es', 'en'],
        'address': {'@type': 'PostalAddress', 'addressLocality': C.BASE_TOWN, 'addressRegion': C.BASE_REGION, 'addressCountry': 'ES'},
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
    web = {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': C.BRAND,
           'inLanguage': LANGS, 'publisher': {'@id': SITE + '/#business'}}
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': t['title'], 'description': t['desc'],
            'inLanguage': lang, 'dateModified': C.CONTENT_DATE, 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#business'}}
    # Misma lista que las FAQ visibles: no pueden divergir.
    faq = {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a, **x)}} for q, a, x in faq_items(lang)]}
    return [biz, web, page, faq]


# --- portada (ES y EN) ----------------------------------------------------------------------
def home(lang):
    t = T[lang]
    alternates = ALTERNATES
    out = head(lang, t['title'], t['desc'], t['path'], alternates=alternates, og=True, ld=ld_home(lang))
    out += '<body>\n' + header(lang) + '<main>\n'

    # «Grupos: varios coches a la vez»: la misma etiqueta y valor que la ficha
    groups = f"{t['facts']['groups']}{t.get('colon', ':')} {t['groups_value'][0].lower()}{t['groups_value'][1:]}"
    checks = ''.join(f'<span>{CHECK}{fmt(c, hours=t["hours"], langs=t["langs"], groups=groups)}</span>' for c in t['checks'])
    chat = ''.join(f'<div class="msg {who}">{fmt(m)}</div>' for who, m in t['chat'])
    out += f'''<section id="top" class="hero">
<div class="wrap">
<div class="hero-top">
<h1><span class="eyebrow on-dark">{DOT}<span>{t['eyebrow']}<span class="eb-more">{t['eyebrow_more']}</span></span></span> <span class="h1-main">{t['h1']}</span></h1>
</div>
<div class="hero-copy">
{go_form(lang)}<p class="promise">{t['promise']}</p>
<p class="summary">{t['summary']}</p><p class="sub">{t['sub']}</p>
<div class="hero-checks">{checks}</div>
</div>
<div class="chat-col">
<div class="chat" role="img" aria-label="{t['chat_label']}">
<div class="chat-head"><div class="chat-avatar" aria-hidden="true">{FAVICON}</div><div><span class="chat-name">{C.BRAND}</span><span class="chat-status">{t['chat_status']}</span></div></div>
{chat}
</div>
<p class="chat-note" aria-hidden="true">{t['chat_label']}</p>
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
                  f'<h3>{name}</h3>'
                  f'<p class="dest-note">{note}</p><span class="dest-cta">{t["dest_cta"]}</span></a>\n')
    chips = ''.join(f'<a class="chip" href="{wa(m)}">{n}</a>' for n, m in t['chips'])
    out += f'''<section id="destinos" class="section sand">
<div class="wrap">
<div class="section-head"><span class="eyebrow">{t['dest_eyebrow']}</span><h2>{t['dest_h2']}</h2><p class="lead">{t['dest_lead']}</p></div>
<div class="grid-3">
{cards}</div>
<div class="chips">{chips}</div>
</div>
</section>
'''
    if C.MAX_PAX:
        n, cars = group_example()
        gcards = ''.join(f'<a class="card dest" href="{wa(m)}"><h3>{h}</h3><p class="dest-note">{d}</p>'
                         f'<span class="dest-cta">{t["dest_cta"]}</span></a>\n' for h, _, d, m in t['group_types'])
        out += f'''<section id="grupos" class="section">
<div class="wrap">
<div class="section-head"><span class="eyebrow">{t['groups_eyebrow']}</span><h2>{t['groups_h2']}</h2><p class="lead">{t['groups_lead']}</p></div>
<p class="group-example">{t['groups_example'].format(n=n, cars=cars)}</p>
<div class="grid-4">
{gcards}</div>
</div>
</section>
'''
    out += f'''<section id="equipo" class="section team">
<div class="wrap">
<div class="section-head"><span class="eyebrow on-dark">{t['team_eyebrow']}</span><h2>{t['team_h2']}</h2><p class="lead">{t['team_lead']}</p></div>
{facts(lang)}
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
    faq = ''.join(f'<details><summary>{fmt(q)}</summary><p>{fmt(a, **x)}</p></details>\n' for q, a, x in faq_items(lang))
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
<div class="cta-actions">
<a class="btn btn-navy" href="{wa(t['wa_generic'])}">{wa_icon(20)}{t['cta_final']}</a>
{share_link(lang)}
</div>
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
                            PHONE=phone_display(), LEGAL_DATE=C.LEGAL_DATE)
    out = head('es', f'{p["title"]} · {C.BRAND}', p['desc'], f'/{slug}/', robots=NOINDEX)
    return out + '<body>\n' + header('es') + f'<main class="wrap doc">\n<h1>{p["title"]}</h1>\n{body}\n</main>\n' + footer('es')

def page_404():
    out = head('es', f'Página no encontrada · {C.BRAND}', f'Esta página no existe. Vuelve al inicio de {C.BRAND}, transfer privado en Málaga y Costa del Sol.', '/404.html', robots=NOINDEX)
    return out + '<body>\n' + header('es') + f'''<main class="wrap doc">
<h1>Esta página no existe</h1>
<p>Puede que el enlace esté mal escrito o que la página se haya movido.</p>
<p><a href="/">Ir al inicio</a> · <a href="/en/" lang="en" hreflang="en">Go to the English version</a></p>
<a class="btn btn-wa" href="{wa(T['es']['wa_generic'])}">{wa_icon(20)}{T['es']['cta_nav']}</a>
</main>
''' + footer('es')


# --- ficheros de indexación ------------------------------------------------------------------
def robots_txt():
    return f'''# {C.BRAND} · robots.txt
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
    for lang in LANGS:
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{p}"/>' for h, p in ALTERNATES)
        urls += f'<url><loc>{SITE}{T[lang]["path"]}</loc><lastmod>{C.CONTENT_DATE}</lastmod>{alts}</url>\n'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + urls + '</urlset>\n')


# --- montaje --------------------------------------------------------------------------------
def write(out, rel, content):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(minify_html(wa_new_tab(content)) if rel.endswith('.html') else content)

def build(out):
    for lang in LANGS:
        write(out, T[lang]['path'].lstrip('/') + 'index.html', home(lang))
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
