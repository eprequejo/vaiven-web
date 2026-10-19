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

LEGAL = {
'aviso-legal': {
    'title': 'Aviso legal',
    'desc': 'Aviso legal de Vaivén, transfer privado y chófer con autorización VTC en Mijas (Málaga).',
    'body': '''<h2>Quiénes somos</h2>
<p>En cumplimiento de la Ley 34/2002, de servicios de la sociedad de la información (LSSI), te informamos de que esta web ({DOMAIN}) es de:</p>
''' + TITULAR + '''
<h2>Actividad</h2>
<p>Transporte de viajeros en vehículo de turismo con conductor (VTC), con autorización nº {VTC_NO} de la Junta de Andalucía. Prestamos el servicio solo con contratación previa: la confirmación por escrito (WhatsApp) de origen, destino, fecha, hora y precio es el contrato. No recogemos pasajeros sin reserva.</p>
<h2>Precio, pago y cancelación</h2>
<p>El precio se comunica por escrito antes de confirmar y es cerrado por vehículo. Se paga al terminar el trayecto, en efectivo, tarjeta o Bizum. La cancelación es gratuita hasta 24 horas antes del servicio.</p>
<h2>Uso de la web</h2>
<p>Esta web es informativa: no vende nada ni recoge datos. Los textos, el logotipo y el diseño son nuestros; no los copies sin permiso. No respondemos del contenido de webs de terceros a las que enlacemos.</p>
<h2>Ley aplicable</h2>
<p>Se aplica la legislación española. Si eres consumidor, te corresponden los juzgados de tu domicilio.</p>
''',
},
'privacidad': {
    'title': 'Política de privacidad',
    'desc': 'Cómo trata Vaivén los datos de quien reserva un traslado por WhatsApp. Web sin cookies.',
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
'reclamaciones': {
    'title': 'Hojas de reclamaciones',
    'desc': 'Cómo presentar una queja o reclamación a Vaivén: hojas oficiales de la Junta de Andalucía.',
    'body': '''<p>Si algo no ha ido bien, escríbenos primero por WhatsApp o a {EMAIL}: casi todo se arregla con un mensaje.</p>
<h2>Hojas oficiales de quejas y reclamaciones</h2>
<p>Tenemos a tu disposición las hojas oficiales de quejas y reclamaciones de la Junta de Andalucía. Pídeselas al conductor durante el servicio o pídenoslas por WhatsApp ({PHONE}) y te las hacemos llegar.</p>
<p>También puedes presentar tu reclamación por vía electrónica en Consumo Responde, el servicio de consumo de la Junta de Andalucía (consumoresponde.es), o acudir a la Junta Arbitral del Transporte de Andalucía.</p>
''' + TITULAR,
},
}
