# -*- coding: utf-8 -*-
"""Genera UNA VEZ el favicon.ico, el icono de iPhone y las imágenes para redes en src/static/ (se versionan).

python3 src/make_assets.py <carpeta con Outfit.ttf y Manrope.ttf>
TTF variables de github.com/google/fonts (ofl/outfit, ofl/manrope). Requiere Pillow.
La geometría sale de src/brand/*.svg (la misma que pinta build.py): si cambia el logo, se vuelve a ejecutar.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BRAND as BRAND_NAME, WM_V
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(SRC, 'static')
BRAND = os.path.join(SRC, 'brand')
NAVY, YELLOW, CREAM = '#0E2B40', '#F0A202', '#FBF8F2'


def read_svg(name):
    """viewBox, rect de fondo (o None) y trazos [(x1, y1, x2, y2, color, grosor)] de un SVG de src/brand/."""
    root = ET.parse(os.path.join(BRAND, name)).getroot()
    box = float(root.get('viewBox').split()[2])
    rect, strokes = None, []
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag == 'rect':
            rect = (el.get('fill'), float(el.get('rx', 0)))
        elif tag == 'path':
            x1, y1, x2, y2 = map(float, re.findall(r'-?\d+(?:\.\d+)?', el.get('d')))
            strokes.append((x1, y1, x2, y2, el.get('stroke'), float(el.get('stroke-width'))))
    return box, rect, strokes

def draw_strokes(d, strokes, x, y, s):
    """Trazos con extremos redondeados (stroke-linecap:round) a escala s, origen x, y."""
    for x1, y1, x2, y2, color, w in strokes:
        a, b, r = (x + x1 * s, y + y1 * s), (x + x2 * s, y + y2 * s), w * s / 2
        d.line([a, b], fill=color, width=round(w * s))
        for cx, cy in (a, b):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def icon(size, rounded=True):
    """El favicon a 'size' px. rounded=False: cuadrado opaco (iOS redondea él solo; evita esquinas negras)."""
    box, rect, strokes = read_svg('favicon.svg')
    big = size * 4
    im = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rect:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=rect[1] * big / box if rounded else 0, fill=rect[0])
    draw_strokes(d, strokes, 0, 0, big / box)
    return im.resize((size, size), Image.LANCZOS)

def wordmark(d, ttf, x, baseline, size):
    """«ya» + V + «oy» como en la cabecera (mismas proporciones: config.WM_V). Sobre azul: trazo izquierdo crema."""
    f = font(os.path.join(ttf, 'Outfit.ttf'), size, 800)
    left, right = BRAND_NAME.split('v', 1)
    asc = f.getmetrics()[0]
    d.text((x, baseline - asc), left, font=f, fill=CREAM)
    x += f.getlength(left) - WM_V['overlap'] * size
    box, _, strokes = read_svg('logo.svg')
    v = WM_V['size'] * size
    strokes = [(*s[:4], CREAM if s[4] == NAVY else s[4], WM_V['stroke']) for s in strokes]
    draw_strokes(d, strokes, x, baseline - v + WM_V['drop'] * size, v / box)
    d.text((x + v - WM_V['overlap'] * size, baseline - asc), right, font=f, fill=CREAM)

def font(path, size, wght):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([wght])
    return f

def og(ttf, out, lines):
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(im)
    wordmark(d, ttf, 80, 150, 72)
    big = font(os.path.join(ttf, 'Outfit.ttf'), 92, 800)
    y = 210
    for line in lines[0]:
        d.text((80, y), line, font=big, fill=CREAM)
        y += 96
    d.text((80, y + 28), lines[1], font=font(os.path.join(ttf, 'Manrope.ttf'), 30, 600), fill=YELLOW)
    im.save(os.path.join(STATIC, out), 'JPEG', quality=86, optimize=True, progressive=True)

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ttf = sys.argv[1]
    os.makedirs(STATIC, exist_ok=True)
    icon(32).save(os.path.join(STATIC, 'favicon.ico'), sizes=[(32, 32)])
    icon(180, rounded=False).convert('RGB').save(os.path.join(STATIC, 'apple-touch-icon.png'), optimize=True)
    # Una por idioma: el lema (h1) en tres líneas y la etiqueta debajo, de los mismos textos que la web
    from build import T, LANGS, og_image
    for lang in LANGS:
        t = T[lang]
        og(ttf, og_image(lang), ([x.strip() for x in re.findall(r'[^.]+\.', t['h1'])], t['eyebrow'] + t['eyebrow_more']))
    for f in sorted(os.listdir(STATIC)):
        print(f, os.path.getsize(os.path.join(STATIC, f)), 'bytes')

if __name__ == '__main__':
    main()
