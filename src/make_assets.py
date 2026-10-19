# -*- coding: utf-8 -*-
"""Genera UNA VEZ los iconos y las imágenes para redes en src/static/ (se versionan; build.py solo los copia).

python3 src/make_assets.py <carpeta con Outfit.ttf y Manrope.ttf>
TTF variables de github.com/google/fonts (ofl/outfit, ofl/manrope). Requiere Pillow.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(SRC, 'static')
NAVY, YELLOW, CREAM, MUTED = '#0E2B40', '#F0A202', '#FBF8F2', '#C8D3DB'

# El mismo bocadillo que el logo SVG de build.py (viewBox 30×30), con tema oscuro para pestañas oscuras.
FAVICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><style>path{fill:#0E2B40}@media (prefers-color-scheme:dark){path{fill:#FBF8F2}}</style><path d="M15 3C8.4 3 3 7.7 3 13.6c0 3.3 1.7 6.2 4.4 8.1L6 27l6.1-2.3c.9.2 1.9.3 2.9.3 6.6 0 12-4.7 12-10.6S21.6 3 15 3z"/><circle cx="15" cy="13.6" r="3" fill="#F0A202"/></svg>
'''

def bubble(draw, x, y, s, fill, dot=YELLOW):
    """Bocadillo del logo a escala s (1 = 30 px) con esquina superior izquierda en x, y."""
    P = lambda px, py: (x + px * s, y + py * s)
    draw.ellipse([P(3, 3), P(27, 24.2)], fill=fill)
    draw.polygon([P(7.4, 19.5), P(6, 27), P(13, 23.5)], fill=fill)
    draw.ellipse([P(12, 10.6), P(18, 16.6)], fill=dot)

def icon(size, bg):
    big = size * 4
    im = Image.new('RGBA', (big, big), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bg:
        bubble(d, big * 0.17, big * 0.15, big * 0.66 / 30, CREAM)
    else:
        bubble(d, 0, 0, big / 30, NAVY)
    return im.resize((size, size), Image.LANCZOS)

def font(path, size, wght):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes([wght])
    return f

def og(ttf, out, lines):
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(im)
    bubble(d, 80, 72, 3.2, CREAM)
    d.text((196, 86), 'Vaivén', font=font(os.path.join(ttf, 'Outfit.ttf'), 64, 800), fill=CREAM)
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
    with open(os.path.join(STATIC, 'favicon.svg'), 'w') as f:
        f.write(FAVICON_SVG)
    icon(32, None).save(os.path.join(STATIC, 'favicon.ico'), sizes=[(32, 32)])
    icon(180, NAVY).convert('RGB').save(os.path.join(STATIC, 'apple-touch-icon.png'), optimize=True)
    og(ttf, 'og.jpg', (['Un mensaje.', 'Una persona.', 'Un precio.'], 'Transfer privado · Málaga y Costa del Sol'))
    og(ttf, 'og-en.jpg', (['One message.', 'One person.', 'One price.'], 'Private transfers · Málaga & Costa del Sol'))
    for f in sorted(os.listdir(STATIC)):
        print(f, os.path.getsize(os.path.join(STATIC, f)), 'bytes')

if __name__ == '__main__':
    main()
