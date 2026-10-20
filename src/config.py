# -*- coding: utf-8 -*-
"""Datos del negocio. Cada dato vive AQUÍ y solo aquí: build.py lo pinta en todas las páginas.

None = hueco. Los de REQUIRED bloquean `build.py prod` (no se publica con huecos).
Los opcionales, si faltan, no se pintan (nunca se inventan).
"""

# Marca: una palabra, en minúsculas, en todas partes (brief 19-oct-2026). El logotipo es «ya» + V + «oy».
BRAND = 'yavoy'
# La V del logotipo, en em del texto: tamaño (altura de mayúscula), solape con las letras y bajada bajo la base.
# stroke: grosor del trazo en unidades del SVG (de 64). El palo de Outfit 800 mide 0,174 em (medido 19-oct);
# 15,5/64 × 0,86 = 0,208 em: más que las letras, porque es la letra protagonista y la diagonal se ve más fina
# (Estela, 19-oct: «un pelín más gruesa»). Lo usan build.py y make_assets.py.
WM_V = {'size': .86, 'overlap': .06, 'drop': .09, 'stroke': 15.5}

# --- obligatorios -----------------------------------------------------------
DOMAIN = 'yavoymalaga.com'  # sin https:// ni barra final
PHONE = '34633366570'  # WhatsApp (formato wa.me: 34 delante, sin + ni espacios). El de Juteber Gestión (20-oct-2026)
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

# Base del negocio (JSON-LD address y ficha «en pocas palabras»)
BASE_TOWN, BASE_REGION = 'Mijas', 'Málaga'

MAX_PAX = 4                          # plazas por coche
INCLUDED = ['toll', 'night', 'luggage']  # qué incluye el precio (claves de content.INCLUDED_LABELS)


# Fecha del último cambio REAL de contenido (va al <lastmod> del sitemap).
# Cámbiala solo cuando cambie el texto, no en cada build.
CONTENT_DATE = '2026-10-20'
# Fecha de los textos legales (su «Última actualización»). Aparte: cambiar la portada no cambia lo legal.
LEGAL_DATE = '2026-10-20'

# Clave pública de IndexNow (no es secreta: se publica en /<clave>.txt)
INDEXNOW_KEY = 'b7e41c9a0f5d4e2a8c63d1f09a7b5e24'
