# -*- coding: utf-8 -*-
"""Datos del negocio. Cada dato vive AQUÍ y solo aquí: build.py lo pinta en todas las páginas.

None = hueco. Los de REQUIRED bloquean `build.py prod` (no se publica con huecos).
Los opcionales, si faltan, no se pintan (nunca se inventan).
"""

# Marca: una palabra, en minúsculas, en todas partes (brief 19-oct-2026). El logotipo es «ya» + V + «oy».
BRAND = 'yavoy'
# La V del logotipo, en em del texto: tamaño (altura de mayúscula), solape con las letras y bajada bajo la base.
# Lo usan la CSS (build.py) y la imagen para redes (make_assets.py).
WM_V = {'size': .86, 'overlap': .06, 'drop': .09}

# --- obligatorios -----------------------------------------------------------
DOMAIN = 'yavoymalaga.com'  # sin https:// ni barra final
PHONE = '34658428681'  # WhatsApp (formato wa.me: 34 delante, sin + ni espacios). Provisional: el de Estela
VTC_NO = '12011555'    # autorización VTC (Registro de Empresas y Actividades de Transporte)
# Mismo titular que Padelia y Nautelia (espejo de nautelia-landing/src/parts.py y build.py; test_check.py falla si divergen)
RAZON_SOCIAL = 'SIMPLYLE, S. Coop. And.'
CIF = 'F93649564'
LEGAL_ADDRESS = 'Calle Altabaca de la Torre 31, Urb. La Cala Hills, Fase 3, Apto. 319, 29650 Mijas Costa (Málaga), España'
EMAIL = 'hola@yavoymalaga.com'  # mismo patrón que hola@nautelia.com (crear el buzón)

REQUIRED = ['DOMAIN', 'PHONE', 'VTC_NO', 'RAZON_SOCIAL', 'CIF', 'LEGAL_ADDRESS', 'EMAIL']

# --- opcionales (si faltan, la parte correspondiente no se pinta) ----------
GOOGLE_REVIEWS_URL = None   # enlace a la ficha de Google Business Profile (reseñas)
GOOGLE_REVIEWS_COUNT = None # nº de reseñas en Google, p. ej. 37
# Reseñas REALES de Google, copiadas literalmente. lang = idioma en que se escribió.
# {'text': '...', 'name': 'Sarah', 'route': 'Aeropuerto → Marbella', 'lang': 'en'}
REVIEWS = []
SAME_AS = []                # URLs de perfiles reales: ficha de Google, Instagram, Facebook…
GEO = None                  # (lat, lng) de la base, si la ficha de Google tiene dirección pública

MAX_PAX = 4                          # plazas por coche
INCLUDED = ['toll', 'night', 'luggage']  # qué incluye el precio (claves de content.INCLUDED_LABELS)

# Equipo. Foto: deja src/photos/<slug>.jpg y build.py la convierte a WebP 400×500.
# bio / langs: frase opcional por idioma.
TEAM = [
    {'slug': 'juan', 'name': 'Juan', 'role': 'coord', 'langs': None, 'bio': {'es': None, 'en': None}},
    {'slug': 'ibrahim', 'name': 'Ibrahim', 'role': 'driver', 'langs': {'es': 'Español e inglés.', 'en': 'Spanish and English.'}, 'bio': {'es': None, 'en': None}},
    {'slug': 'nasuri', 'name': 'Nasuri', 'role': 'driver', 'langs': None, 'bio': {'es': None, 'en': None}},
]

# Fecha del último cambio REAL de contenido (va al <lastmod> del sitemap).
# Cámbiala solo cuando cambie el texto, no en cada build.
CONTENT_DATE = '2026-10-19'

# Clave pública de IndexNow (no es secreta: se publica en /<clave>.txt)
INDEXNOW_KEY = 'b7e41c9a0f5d4e2a8c63d1f09a7b5e24'
