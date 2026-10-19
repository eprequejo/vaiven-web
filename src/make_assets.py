# -*- coding: utf-8 -*-
"""Genera UNA VEZ el favicon.ico, el icono de iPhone y las imágenes para redes en src/static/ (se versionan).

python3 src/make_assets.py <carpeta con Outfit.ttf y Manrope.ttf>
TTF variables de github.com/google/fonts (ofl/outfit, ofl/manrope). Requiere Pillow.
La geometría sale de src/brand/*.svg (la misma que pinta build.py): si cambia el logo, se vuelve a ejecutar.
"""
import os, re, sys
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

def font(path, size, wght):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([wght])
    return f

def og(ttf, out, lines):
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # Sobre fondo marino, los trazos del favicon (crema + amarillo); el del logo sería marino sobre marino.
    box, _, strokes = read_svg('favicon.svg')
    draw_strokes(d, strokes, 72, 70, 96 / box)
    d.text((190, 86), 'Vaivén', font=font(os.path.join(ttf, 'Outfit.ttf'), 64, 800), fill=CREAM)
    big = font(os.path.join(ttf, 'Outfit.ttf'), 92, 800)
    y = 210
    for line in lines[0]:
        d.text((80, y), line, font=big, fill=CREAM)
        y += 96
    d.text((80, y + 28), lines[1], font=font(os.path.join(ttf, 'Manrope.ttf'), 34, 600), fill=YELLOW)
    im.save(os.path.join(STATIC, out), 'JPEG', quality=86, optimize=True, progressive=True)

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ttf = sys.argv[1]
    os.makedirs(STATIC, exist_ok=True)
    icon(32).save(os.path.join(STATIC, 'favicon.ico'), sizes=[(32, 32)])
    icon(180, rounded=False).convert('RGB').save(os.path.join(STATIC, 'apple-touch-icon.png'), optimize=True)
    og(ttf, 'og.jpg', (['Un mensaje.', 'Una persona.', 'Un precio.'], 'Transfer privado · Málaga y Costa del Sol'))
    og(ttf, 'og-en.jpg', (['One message.', 'One person.', 'One price.'], 'Private transfers · Málaga & Costa del Sol'))
    for f in sorted(os.listdir(STATIC)):
        print(f, os.path.getsize(os.path.join(STATIC, f)), 'bytes')

if __name__ == '__main__':
    main()
