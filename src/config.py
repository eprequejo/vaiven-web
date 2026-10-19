# -*- coding: utf-8 -*-
"""Datos del negocio. Cada dato vive AQUÍ y solo aquí: build.py lo pinta en todas las páginas.

None = hueco. Los de REQUIRED bloquean `build.py prod` (no se publica con huecos).
Los opcionales, si faltan, no se pintan (nunca se inventan).
"""

# --- obligatorios -----------------------------------------------------------
DOMAIN = None          # 'vaiven.es' — sin https:// ni barra final
PHONE = None           # '34600000000' — formato wa.me: prefijo de país, sin + ni espacios
VTC_NO = None          # nº de autorización VTC de la Junta de Andalucía
RAZON_SOCIAL = None    # 'Vaivén Transfer S.L.' o nombre y apellidos si es autónomo
CIF = None             # CIF / NIF
LEGAL_ADDRESS = None   # domicilio social completo (aviso legal y privacidad)
EMAIL = None           # email de contacto (obligatorio por LSSI y RGPD)
CHAT_PRICE = None      # precio del ejemplo del chat aeropuerto → La Cala, 3 pax: '45'

REQUIRED = ['DOMAIN', 'PHONE', 'VTC_NO', 'RAZON_SOCIAL', 'CIF', 'LEGAL_ADDRESS', 'EMAIL', 'CHAT_PRICE']

# --- opcionales (si faltan, la parte correspondiente no se pinta) ----------
GOOGLE_REVIEWS_URL = None   # enlace a la ficha de Google Business Profile (reseñas)
GOOGLE_REVIEWS_COUNT = None # nº de reseñas en Google, p. ej. 37
# Reseñas REALES de Google, copiadas literalmente. lang = idioma en que se escribió.
# {'text': '...', 'name': 'Sarah', 'route': 'Aeropuerto → Marbella', 'lang': 'en'}
REVIEWS = []
SAME_AS = []                # URLs de perfiles reales: ficha de Google, Instagram, Facebook…
GEO = None                  # (lat, lng) de la base, si la ficha de Google tiene dirección pública

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
