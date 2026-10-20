# -*- coding: utf-8 -*-
"""Gate de publicación: python3 src/check.py <carpeta> [--allow-holes]  -> exit 1 si algo falla.

Lo llama build.py (prod no publica si falla). Comprueba SEO, enlaces, huecos y presupuesto de peso
sobre la SALIDA generada, no sobre el código.
"""
import gzip, json, os, re, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, LANGS
# Portada de cada idioma (ruta → idioma): la lista vive en content.py
HOMES = {T[l]['path']: l for l in LANGS}

HOLE = 'HUECO:'
# Restos de la plantilla original tipo [NÚMERO], [CIF], [UNA FRASE SOBRE JUAN]
TEMPLATE_HOLE = re.compile(r'\[[A-ZÁÉÍÓÚÑ0-9 +]{2,}\]')

MAX_TITLE, MAX_DESC = 60, 160
FAQ_WORDS = (25, 90)           # GEO: respuesta que se entiende sola, ni frase suelta ni muro
MAX_HTML_GZ = 18 * 1024        # cada HTML comprimido
MAX_FONTS = 80 * 1024          # todas las fuentes
MAX_HOME = 120 * 1024          # portada sin fotos: HTML + fuentes precargadas + favicon
ALLOWED_TXT = {'robots.txt'}   # + la clave de IndexNow (<32 hex>.txt)
FORBIDDEN_EXT = ('.py', '.md', '.pyc', '.sh', '.json')


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None; self.title = ''; self.desc = None; self.robots = None; self.canonical = None
        self.alternates = {}; self.h1 = 0; self.ids = set(); self.links = []; self.ld = []
        self.wa_same_tab = []; self.forms = []; self.summaries = []; self.answers = []; self.external = []; self.preloads = []
        self._details = False
        self._in = None; self._buf = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        elif tag == 'meta' and a.get('name') == 'description':
            self.desc = a.get('content', '')
        elif tag == 'meta' and a.get('name') == 'robots':
            self.robots = a.get('content', '')
        elif tag == 'link':
            rel = a.get('rel', '')
            if rel == 'canonical':
                self.canonical = a.get('href')
            elif rel == 'alternate' and a.get('hreflang'):
                self.alternates[a['hreflang']] = a.get('href')
            elif rel == 'stylesheet':
                self.external.append('hoja de estilos externa ' + a.get('href', ''))
            elif rel in ('preload', 'icon', 'apple-touch-icon'):
                self.links.append(a.get('href', ''))
                if rel == 'preload':
                    self.preloads.append(a.get('href', ''))
        elif tag == 'form':
            self.forms.append(a.get('action', ''))
        elif tag == 'a' and a.get('href'):
            self.links.append(a['href'])
            if a['href'].startswith('https://wa.me/') and a.get('target') != '_blank':
                self.wa_same_tab.append(a['href'])
        elif tag in ('img', 'source') and a.get('src'):
            self.links.append(a['src'])
        elif tag == 'script':
            if a.get('src'):
                self.external.append('<script src> ' + a['src'])
            elif a.get('type') == 'application/ld+json':
                self._in, self._buf = 'ld', ''
        if tag == 'h1':
            self.h1 += 1
        elif tag == 'title':
            self._in, self._buf = 'title', ''
        elif tag == 'summary' and self._details:
            self._in, self._buf = 'summary', ''
        elif tag == 'details':
            # Las FAQ son <details> sin clase; el selector de idioma (<details class="langs">) no es una pregunta
            self._details = not dict(attrs).get('class')
        elif tag == 'p' and self._details:
            self._in, self._buf = 'answer', ''

    def handle_endtag(self, tag):
        if tag == 'details':
            self._details = False
        if self._in == 'answer' and tag == 'p':
            self.answers.append(self._buf.strip())
        elif self._in == 'ld' and tag == 'script':
            self.ld.append(self._buf)
        elif self._in == 'title' and tag == 'title':
            self.title = self._buf.strip()
        elif self._in == 'summary' and tag == 'summary':
            self.summaries.append(self._buf.strip())
        else:
            return
        self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf += data


def html_files(root):
    for d, _, files in os.walk(root):
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(d, f)

def url_path(root, file):
    rel = '/' + os.path.relpath(file, root).replace(os.sep, '/')
    return rel[:-len('index.html')] if rel.endswith('/index.html') else rel

def resolve(root, path):
    """Ruta del sitio -> fichero en disco, como lo sirve GitHub Pages."""
    p = os.path.join(root, path.lstrip('/'))
    if path.endswith('/'):
        p = os.path.join(p, 'index.html')
    return p if os.path.isfile(p) else None

def holes(root):
    found = set()
    for d, _, files in os.walk(root):
        for f in files:
            if f.endswith(('.html', '.xml', '.txt')):
                txt = Path(d, f).read_text(encoding='utf-8')
                found.update(re.findall(HOLE + r'([A-Z_]+)', txt))
                found.update(TEMPLATE_HOLE.findall(txt))
    return sorted(found)


def run(root, domain=None, allow_holes=False):
    errors = []
    err = errors.append
    pages = {}
    for f in html_files(root):
        p = Page(); p.feed(Path(f).read_text(encoding='utf-8'))
        pages[url_path(root, f)] = (f, p)
    missing = [h for h in HOMES if h not in pages]
    if missing:
        err(f'faltan portadas: {missing}')
        return errors

    # 1. huecos
    if not allow_holes:
        for h in holes(root):
            err(f'hueco sin rellenar: {h}')
        if not domain:
            err('DOMAIN sin definir')
    for path, (f, _) in pages.items():
        if re.search(r'\bNone\b', Path(f).read_text(encoding='utf-8')):
            err(f'{path}: "None" pintado en la página')

    # origen común: el del canonical de la portada (y el de config en prod)
    origin = '{0.scheme}://{0.netloc}'.format(urlparse(pages['/'][1].canonical or ''))
    if domain and origin != f'https://{domain}':
        err(f'canonical de / en {origin}, esperado https://{domain}')

    indexable = set()
    for path, (f, p) in pages.items():
        tag = path
        # 2. JSON-LD
        for block in p.ld:
            try:
                data = json.loads(block)
            except ValueError as e:
                err(f'{tag}: JSON-LD no parsea ({e})')
                continue
            for node in data.get('@graph', [data]):
                if 'telephone' in node:
                    err(f'{tag}: telephone en JSON-LD (solo WhatsApp: Google mostraría «Llamar»)')
                if node.get('@type') == 'FAQPage':
                    qs = [q['name'] for q in node['mainEntity']]
                    ans = [q['acceptedAnswer']['text'] for q in node['mainEntity']]
                    if qs != p.summaries:
                        err(f'{tag}: las preguntas del FAQPage no coinciden con las FAQ visibles')
                    if ans != p.answers:
                        err(f'{tag}: la respuesta visible de la FAQ no coincide con la del JSON-LD')
                    for q, a in zip(qs, ans):
                        n = len(a.split())
                        if not FAQ_WORDS[0] <= n <= FAQ_WORDS[1]:
                            err(f'{tag}: FAQ «{q}» tiene {n} palabras ({FAQ_WORDS[0]}-{FAQ_WORDS[1]})')
        # 3. h1 y lang
        if p.h1 != 1:
            err(f'{tag}: {p.h1} <h1> (debe haber 1)')
        want_lang = next((l for h, l in HOMES.items() if h != '/' and path.startswith(h)), LANGS[0])
        if p.lang != want_lang:
            err(f'{tag}: lang="{p.lang}", esperado "{want_lang}"')
        # 4. title y description
        if not p.title or len(p.title) > MAX_TITLE:
            err(f'{tag}: title de {len(p.title)} caracteres (máx {MAX_TITLE})')
        if not p.desc or len(p.desc) > MAX_DESC:
            err(f'{tag}: description de {len(p.desc or "")} caracteres (máx {MAX_DESC})')
        # 5. canonical
        if p.canonical != origin + path:
            err(f'{tag}: canonical {p.canonical}, esperado {origin + path}')
        # 8. robots
        robots = p.robots or ''
        if 'noindex' not in robots:
            indexable.add(path)
        # 7. enlaces internos y assets
        for href in p.links:
            u = urlparse(href)
            if u.netloc == 'wa.me' and '[' in ''.join(parse_qs(u.query).get('text', [])):
                err(f'{tag}: mensaje de WhatsApp con huecos para rellenar: {href}')
            if u.scheme in ('https', 'http'):
                if u.netloc in ('', origin.split('//')[-1]):
                    err(f'{tag}: enlace interno absoluto {href}')
                continue
            if u.scheme == 'tel':
                err(f'{tag}: enlace de llamada {href} (solo atendemos por WhatsApp)')
                continue
            if u.scheme == 'mailto':
                continue
            if u.scheme:
                err(f'{tag}: esquema no permitido {href}')
                continue
            target = u.path or path
            if not target.startswith('/'):
                err(f'{tag}: enlace relativo {href} (usar rutas desde /)')
                continue
            if target not in pages and not resolve(root, target):
                err(f'{tag}: enlace roto {href}')
            elif u.fragment:
                tp = pages.get(target)
                if tp and u.fragment not in tp[1].ids:
                    err(f'{tag}: ancla inexistente {href}')
        for href in p.wa_same_tab:
            err(f'{tag}: enlace de WhatsApp que no abre en pestaña nueva: {href[:60]}')
        # sin servidor propio: un formulario solo puede llevar a WhatsApp, nunca mandar datos a otro sitio
        for action in p.forms:
            if not action.startswith('https://wa.me/'):
                err(f'{tag}: formulario que envía a {action or "esta página"} (solo se permite wa.me)')
        # 10. nada externo que bloquee el pintado
        for x in p.external:
            err(f'{tag}: {x}')
        # presupuesto por HTML
        gz = len(gzip.compress(Path(f).read_bytes()))
        if gz > MAX_HTML_GZ:
            err(f'{tag}: {gz} bytes gzip (máx {MAX_HTML_GZ})')

    # 5. hreflang recíproco: cada página que declara alternates está en los alternates de las otras
    for path, (_, p) in pages.items():
        if not p.alternates:
            continue
        for lang, href in p.alternates.items():
            tpath = urlparse(href).path
            if not href.startswith(origin) or tpath not in pages:
                err(f'{path}: hreflang {lang} apunta a {href}, que no existe')
                continue
            back = pages[tpath][1].alternates
            if back != p.alternates:
                err(f'{path}: hreflang no recíproco con {tpath}')
        if p.alternates.get(p.lang) != origin + path:
            err(f'{path}: falta hreflang a sí misma ({p.lang})')

    # 6. sitemap = páginas indexables
    sm = os.path.join(root, 'sitemap.xml')
    if not os.path.isfile(sm):
        err('falta sitemap.xml')
    else:
        try:
            ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            locs = [e.text for e in ET.parse(sm).getroot().findall('s:url/s:loc', ns)]
            in_sm = {urlparse(l).path for l in locs if l.startswith(origin)}
            if len(in_sm) != len(locs):
                err('sitemap con URLs de otro dominio')
            if in_sm != indexable:
                err(f'sitemap {sorted(in_sm)} != indexables {sorted(indexable)}')
        except ET.ParseError as e:
            err(f'sitemap.xml no parsea ({e})')
    rb = os.path.join(root, 'robots.txt')
    if not os.path.isfile(rb) or f'Sitemap: {origin}/sitemap.xml' not in Path(rb).read_text(encoding='utf-8'):
        err('robots.txt sin la línea Sitemap correcta')

    # 9. nada interno publicado
    for d, _, files in os.walk(root):
        for fn in files:
            if fn.endswith(FORBIDDEN_EXT) or (fn.endswith('.txt') and fn not in ALLOWED_TXT and not re.fullmatch(r'[0-9a-f]{32}\.txt', fn)):
                err(f'fichero que no debe publicarse: {os.path.relpath(os.path.join(d, fn), root)}')

    # 10. presupuesto de peso
    fonts_dir = os.path.join(root, 'assets', 'fonts')
    fonts = sum(os.path.getsize(os.path.join(fonts_dir, x)) for x in os.listdir(fonts_dir)) if os.path.isdir(fonts_dir) else 0
    if fonts > MAX_FONTS:
        err(f'fuentes: {fonts} bytes (máx {MAX_FONTS})')
    for path in HOMES:
        f, p = pages[path]
        total = len(gzip.compress(Path(f).read_bytes()))
        total += sum(os.path.getsize(resolve(root, h) or os.devnull) for h in p.preloads)
        total += os.path.getsize(resolve(root, '/favicon.svg') or os.devnull)
        if total > MAX_HOME:
            err(f'{path}: {total} bytes antes de las fotos (máx {MAX_HOME})')
    return errors


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit('uso: python3 src/check.py <carpeta> [--allow-holes]')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import config
    allow = '--allow-holes' in sys.argv
    errs = run(args[0], domain=None if allow else config.DOMAIN, allow_holes=allow)
    for e in errs:
        print('FALLO -', e)
    print(f'{len(errs)} fallos' if errs else 'OK: 0 fallos')
    sys.exit(1 if errs else 0)
