# -*- coding: utf-8 -*-
"""Páginas legales (solo español, noindex). {CAMPOS} = datos de config.py, los rellena build.py.

Borrador razonable para un VTC autónomo/S.L. sin cookies; que lo revise vuestra gestoría.
Si sois S.L., añadid en el aviso legal los datos de inscripción en el Registro Mercantil.
"""

TITULAR = '''<ul>
<li>Titular: {RAZON_SOCIAL}</li>
<li>CIF/NIF: {CIF}</li>
<li>Domicilio: {LEGAL_ADDRESS}</li>
<li>Email: {EMAIL}</li>
<li>WhatsApp: {PHONE}</li>
</ul>'''

from config import BRAND

LEGAL = {
'aviso-legal': {
    'title': 'Aviso legal',
    'desc': 'Aviso legal de {brand}, transfer privado y chófer con autorización VTC en Mijas (Málaga).',
    'body': '''<h2>Quiénes somos</h2>
<p>En cumplimiento de la Ley 34/2002, de servicios de la sociedad de la información (LSSI), te informamos de que esta web ({DOMAIN}) es de:</p>
''' + TITULAR + '''
<h2>Actividad</h2>
<p>Transporte de viajeros en vehículo de turismo con conductor (VTC), con autorización nº {VTC_NO} de la Junta de Andalucía. Prestamos el servicio solo con contratación previa: la confirmación por escrito (WhatsApp) de origen, destino, fecha, hora y precio es el contrato. No recogemos pasajeros sin reserva.</p>
<h2>Precio, pago y cancelación</h2>
<p>El precio se comunica por escrito antes de confirmar y es cerrado por vehículo. Se paga al terminar el trayecto, en efectivo, tarjeta o Bizum. Se puede cancelar en cualquier momento con un mensaje de WhatsApp; como no se paga nada por adelantado, no hay nada que devolver.</p>
<h2>Quejas</h2>
<p>Si algo no ha ido bien, escríbenos por WhatsApp ({PHONE}) o a {EMAIL} y te contestamos. Si quieres la hoja oficial de quejas y reclamaciones de la Junta de Andalucía, pídenosla por WhatsApp.</p>
<h2>Uso de la web</h2>
<p>Esta web es informativa: no vende nada ni recoge datos. Los textos, el logotipo y el diseño son nuestros; no los copies sin permiso. No respondemos del contenido de webs de terceros a las que enlacemos.</p>
<h2>Ley aplicable</h2>
<p>Se aplica la legislación española. Si eres consumidor, te corresponden los juzgados de tu domicilio.</p>
''',
},
'privacidad': {
    'title': 'Política de privacidad',
    'desc': 'Cómo trata {brand} los datos de quien reserva un traslado por WhatsApp. Web sin cookies.',
    'body': '''<h2>Responsable</h2>
''' + TITULAR + '''
<h2>Esta web no te rastrea</h2>
<p>No usamos cookies, analítica ni publicidad. Las fuentes y las imágenes se sirven desde este mismo dominio, sin llamadas a terceros. El alojamiento (GitHub Pages, de GitHub Inc.) puede registrar la dirección IP de las visitas por seguridad.</p>
<h2>Qué datos tratamos al reservar</h2>
<p>Cuando nos escribes por WhatsApp: tu nombre, número de teléfono, origen y destino, fecha y hora, número de vuelo y número de pasajeros. Si pides factura, los datos de facturación.</p>
<h2>Para qué y con qué base</h2>
<ul>
<li>Prestar el traslado que reservas (ejecución del contrato, art. 6.1.b RGPD).</li>
<li>Hacer las comunicaciones obligatorias de cada servicio VTC a la Administración y cumplir obligaciones fiscales (obligación legal, art. 6.1.c RGPD).</li>
</ul>
<p>No usamos tus datos para publicidad ni los vendemos.</p>
<h2>Cuánto tiempo</h2>
<p>Lo necesario para el servicio y, después, los plazos que exige la ley (fiscales y de transporte).</p>
<h2>Quién más los ve</h2>
<p>La Administración, cuando la ley lo exige. WhatsApp (Meta Platforms) actúa como plataforma de mensajería; puede implicar transferencias internacionales amparadas en el Marco de Privacidad de Datos UE-EE. UU. o en cláusulas contractuales tipo.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {EMAIL}. Si crees que no lo hemos hecho bien, puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
<p>Última actualización: {CONTENT_DATE}.</p>
''',
},
}

for _p in LEGAL.values():
    _p['desc'] = _p['desc'].replace('{brand}', BRAND)
