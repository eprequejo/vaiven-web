# -*- coding: utf-8 -*-
"""Textos de la web en ES y EN. {brand} = config.BRAND (se resuelve al final de este fichero);
{vtc} y los de la FAQ los rellena build.py desde config.py.

Lo que es igual en los dos idiomas (minutos de trayecto, slugs) va una sola vez fuera del dict de idioma.
"""
from config import BRAND

T = {
'es': {
    'path': '/',
    'locale': 'es_ES',
    'title': 'Transfer privado y chófer en Málaga y Costa del Sol · {brand}',
    'desc': 'Transfer privado y chófer en Málaga y la Costa del Sol: aeropuerto, cenas, golf, bodas y excursiones. Precio cerrado por WhatsApp y pagas al llegar.',
    'og_title': '{brand} · Un mensaje. Una persona. Un precio.',
    'og_desc': 'Transfer privado en Málaga y Costa del Sol. Escribes por WhatsApp, te contesta una persona real con el precio cerrado y pagas al llegar.',
    'nav': [('#como', 'Cómo funciona'), ('#destinos', 'Destinos'), ('#equipo', 'Equipo'), ('#faq', 'Preguntas')],
    'nav_label': 'Secciones',
    'home_label': '{brand}, inicio',
    'cta_nav': 'Reservar',
    'wa_generic': 'Hola, quiero reservar un traslado',
    'wa_hero': 'Hola, quiero un traslado de [origen] a [destino] el [fecha] a las [hora], somos [n] personas',
    'eyebrow': 'Transfer privado y chófer · Málaga y Costa del Sol',
    'h1': 'Un mensaje.<br>Una persona.<br>Un precio.',
    'summary': '{brand} es un servicio de transfer privado y chófer con autorización VTC, con base en Mijas (Málaga). Te llevamos donde quieras: al aeropuerto, a cenar, al golf o a una boda en la Costa del Sol, o más lejos, a Granada, Sevilla o Gibraltar, con precio cerrado por coche, reserva por WhatsApp y pago al llegar.',
    'sub': 'Sin app, sin formulario, sin bot, sin pagar por adelantado. Escribes, te contesta una persona real con el precio cerrado y te dice quién te recoge.',
    'promise': 'Pagas cuando te dejamos en tu destino.',
    'cta_hero': 'Reservar por WhatsApp',
    'checks': ['Aeropuerto, puerto, bodas, golf, excursiones', 'Autorización VTC nº {vtc}', '24 h, 365 días'],
    'chat_label': 'Ejemplo de reserva por WhatsApp',
    'chat_status': 'en línea',
    'chat_wink': '«Ya voy» es lo que te escribe tu conductor cuando sale a buscarte.',
    'chat': [
        ('me', 'Hola! Somos 4, el sábado a las 21:00 de La Cala a Puerto Banús, vamos a cenar 🙂'),
        ('them', 'Hola 👋 La Cala → Puerto Banús, 4 personas, precio cerrado y sin suplementos. ¿Dónde os recojo?'),
        ('me', 'Urb. Calypso, portal 3'),
        ('them', 'Reservado ✅ El sábado a las 21:00 os espera Ibrahim en la puerta, Toyota gris 1234 ABC. Pagáis al llegar: efectivo, tarjeta o Bizum.'),
        ('them', 'Ya voy 🚗'),
    ],
    'strip_label': 'Garantías',
    'strip_reviews': '★★★★★ {n} reseñas en Google',
    'strip': ['Empresa de Mijas · hablamos español e inglés', 'Precio cerrado por escrito antes de confirmar', 'Efectivo, tarjeta o Bizum al terminar'],
    'how_eyebrow': 'Cómo funciona',
    'how_h2': 'Así de simple, de verdad',
    'how_lead': 'Nos escribes como escribirías a un amigo que te viene a buscar. Lo demás lo hacemos nosotros.',
    'steps': [
        ('Un mensaje', 'De dónde a dónde, día, hora y cuántos sois. Un WhatsApp y listo. Sin formularios ni cuentas.'),
        ('Una persona', 'Te contesta una persona real, no un bot. Al confirmar te dice quién es tu conductor, el coche y la matrícula, y el día antes te lo reconfirma.'),
        ('Un precio', 'El que te dimos por escrito, sin suplementos ni sorpresas. Llegamos a la hora. Pagas al llegar a tu destino.'),
    ],
    'dest_eyebrow': 'Destinos',
    'dest_h2': 'Transfer privado a donde tú quieras',
    'dest_lead': 'Precio fijo por coche, no por persona, y por escrito antes de confirmar. Te llevamos de puerta a puerta: a cenar, a la playa, al golf, a una boda o al aeropuerto. Estas son las zonas donde más nos movemos; para cualquier otra, pregunta.',
    'dest_cta': 'Pedir precio cerrado →',
    'dest_wa': 'Hola, quiero un traslado de [origen] a {to} el [fecha] a las [hora], somos [n] personas',
    'also': 'También:',
    'chips': [
        ('Aeropuerto de Málaga', 'Hola, quiero un traslado desde o hasta el aeropuerto de Málaga'),
        ('Puerto y estación María Zambrano', 'Hola, necesito un traslado desde el puerto o la estación de Málaga'),
        ('Bodas y eventos', 'Hola, quiero presupuesto para traslados de una boda o evento'),
        ('Golf', 'Hola, quiero un traslado a un campo de golf'),
        ('Ronda, Granada, Sevilla, Gibraltar', 'Hola, quiero una excursión a [ciudad]'),
        ('Chófer por horas', 'Hola, quiero un conductor por horas'),
        ('Hoteles, apartamentos y empresas', 'Hola, gestiono alojamientos y necesito traslados recurrentes'),
    ],
    'team_eyebrow': 'Quiénes somos',
    'team_h2': 'Tres personas de Mijas, no una app con 500 ciudades',
    'team_lead': 'El WhatsApp lo contesta alguien que sabe dónde está tu urbanización, tu finca o tu campo de golf.',
    'team_lead_photos': 'Fotos reales, coches reales. ',
    'roles': {'coord': 'Es quien te contesta. Coordina las reservas y te reconfirma el día antes.', 'driver': 'Conductor.'},
    'role_alt': {'coord': 'coordinador de reservas de {brand}', 'driver': 'conductor de {brand}'},
    'reviews_h2': 'Lo que dicen quienes ya han viajado',
    'reviews_all': 'Ver todas en Google →',
    'stars_label': '5 estrellas',
    'faq_h2': 'Preguntas frecuentes',
    # (pregunta, respuesta, datos de config.py que necesita). Sin ese dato, la pregunta no se pinta.
    # GEO: la respuesta va en la primera frase, 25-90 palabras, entidades con nombre (lo vigila check.py).
    'faq': [
        ('¿Cuánto cuesta un transfer privado?', 'Depende del trayecto y de la hora, y siempre es un precio cerrado por coche, no por persona. Escríbenos por WhatsApp con origen, destino, día y hora, y te damos el precio exacto por escrito antes de confirmar. Es el que pagas al llegar a tu destino, sin suplementos ni sorpresas.', []),
        ('¿Cómo se reserva un chófer? ¿Se puede por WhatsApp?', 'Sí: en {brand} se reserva solo por WhatsApp. Envíanos origen, destino, día, hora y cuántos sois. Una persona te contesta con el precio cerrado por escrito y, cuando confirmas, te manda el nombre del conductor, el coche y la matrícula. El día antes te lo reconfirmamos.', []),
        ('¿Hay que pagar el transfer por adelantado?', 'No. Con {brand} no pagas nada al reservar: pagas al conductor cuando te deja en tu destino, en efectivo, con tarjeta o por Bizum. El precio es el que te dimos por escrito al reservar. Si necesitas factura, te la hacemos.', []),
        ('¿Qué diferencia hay entre un VTC y un taxi en Málaga?', 'El precio y la reserva. Un taxi cobra por taxímetro según la tarifa oficial, más cara de noche y en festivos, y se puede coger en la parada. Un VTC como {brand} cobra un precio cerrado que acuerdas antes del viaje y solo puede trabajar con reserva previa: sabes lo que vas a pagar antes de subir.', []),
        ('¿Sois legales? ¿Tenéis licencia?', 'Sí. {brand} es una empresa con autorización VTC nº {vtc} de la Junta de Andalucía para el transporte de viajeros con conductor. Trabajamos solo con reserva previa, como exige la ley: tu confirmación por WhatsApp es el contrato. Por eso no recogemos a nadie en la calle ni en paradas sin reserva.', []),
        ('¿Qué incluye el precio? ¿Hay suplementos?', 'Todo lo del trayecto. El precio cerrado que te da {brand} por WhatsApp incluye {included}, así que no hay suplementos ni sorpresas: al llegar pagas exactamente la cifra que acordamos, en efectivo, con tarjeta o por Bizum.', ['INCLUDED']),
        ('¿Cuántas personas caben en el coche?', 'Hasta {pax} personas por coche, con su equipaje. Si sois más, lleváis bolsas de golf o mucho equipaje, dínoslo al reservar por WhatsApp y te proponemos la mejor opción para tu grupo, siempre con el precio cerrado antes de confirmar.', ['MAX_PAX']),
        ('¿Qué trayectos hacéis?', 'Cualquiera, dentro o fuera de la provincia de Málaga: aeropuerto, puerto y estación María Zambrano, cenas y salidas de noche, campos de golf, bodas, excursiones a Ronda, Granada, Sevilla o Gibraltar y servicios de chófer por horas. {brand} trabaja desde Mijas por toda la Costa del Sol, siempre con precio cerrado antes de salir.', []),
        ('¿Hacéis trayectos dentro del mismo pueblo o solo entre pueblos?', 'Los dos. {brand} hace trayectos dentro del mismo municipio, como de tu casa a un restaurante de Marbella o del centro de Málaga al aeropuerto, y entre municipios de toda la Costa del Sol, como de Mijas a Marbella o de La Cala a Fuengirola. Siempre con precio cerrado por coche antes de salir.', []),
        ('¿Puedo cancelar un transfer?', 'Sí, gratis hasta 24 horas antes del servicio. Basta con un mensaje de WhatsApp. Como con {brand} no se paga nada por adelantado, no hay nada que devolver ni ningún trámite: solo avísanos cuanto antes para que podamos liberar el coche.', []),
    ],
    'cta_h2': '¿Nos vamos?',
    'cta_final': 'Reservar mi traslado',
    'cta_p': 'Un mensaje por WhatsApp y tienes precio cerrado en un minuto.',
    'footer_tag': 'Transfer privado y chófer · Mijas, Málaga',
    'footer_vtc': 'Autorización VTC nº {vtc} · Servicio con reserva previa; no realizamos recogidas sin contratación previa.',
    'footer_transfers': 'Traslados',
    'footer_links': ['Transfer en Mijas y La Cala', 'Transfer en Fuengirola y Benalmádena', 'Transfer en Marbella', 'Transfer aeropuerto de Málaga', 'Chófer para bodas, golf y excursiones'],
    'footer_legal': 'Legal',
    'wa_float': 'Escribir por WhatsApp',
    'ld_desc': 'Transfer privado y chófer con autorización VTC en Málaga y Costa del Sol. Reserva por WhatsApp, precio cerrado, pago al llegar.',
    'offers': ['Transfer aeropuerto de Málaga', 'Chófer para bodas y eventos', 'Transfer golf Costa del Sol', 'Chófer por horas y excursiones'],
    'payment': 'Efectivo, tarjeta, Bizum',
},
'en': {
    'path': '/en/',
    'locale': 'en_GB',
    'title': 'Private Driver & Transfers on the Costa del Sol · {brand}',
    'desc': 'Private transfers and driver in Málaga and the Costa del Sol: airport, dinners, golf, weddings and day trips. Fixed price on WhatsApp, pay on arrival.',
    'og_title': '{brand} · One message. One person. One price.',
    'og_desc': 'Private transfers in Málaga and the Costa del Sol. Message us on WhatsApp, a real person replies with a fixed price and you pay when you arrive.',
    'nav': [('#como', 'How it works'), ('#destinos', 'Destinations'), ('#equipo', 'Team'), ('#faq', 'FAQ')],
    'nav_label': 'Sections',
    'home_label': '{brand}, home',
    'cta_nav': 'Book now',
    'wa_generic': 'Hi, I would like to book a transfer',
    'wa_hero': 'Hi, I would like a transfer from [pickup] to [destination] on [date] at [time], we are [n] people',
    'eyebrow': 'Private transfers & driver · Málaga and Costa del Sol',
    'h1': 'One message.<br>One person.<br>One price.',
    'summary': '{brand} is a licensed (VTC) private transfer and driver service based in Mijas, Málaga. We take you wherever you want: the airport, dinner, golf or a wedding on the Costa del Sol, or further afield to Granada, Seville or Gibraltar, at a fixed price per car, booked on WhatsApp and paid when you arrive.',
    'sub': 'No app, no forms, no bots, no prepayment. You message us, a real person replies with a fixed price and tells you who will pick you up.',
    'promise': 'You pay when we drop you off.',
    'cta_hero': 'Book on WhatsApp',
    'checks': ['Airport, port, weddings, golf, day trips', 'VTC licence no. {vtc}', '24/7, 365 days a year'],
    'chat_label': 'Example of a WhatsApp booking',
    'chat_status': 'online',
    'chat_wink': '“Ya voy” is what your driver texts you: “On my way.”',
    'chat': [
        ('me', 'Hi! There are 4 of us, Saturday at 9 pm from La Cala to Puerto Banús for dinner 🙂'),
        ('them', 'Hi 👋 La Cala → Puerto Banús, 4 people, fixed price with no extras. Where shall we pick you up?'),
        ('me', 'Urb. Calypso, block 3'),
        ('them', 'Booked ✅ On Saturday at 9 pm Ibrahim will be waiting at your door, grey Toyota 1234 ABC. Pay when you arrive: cash, card or Bizum.'),
        ('them', 'Ya voy 🚗'),
    ],
    'strip_label': 'Guarantees',
    'strip_reviews': '★★★★★ {n} Google reviews',
    'strip': ['Local company from Mijas · we speak English and Spanish', 'Fixed price in writing before you confirm', 'Cash, card or Bizum at the end'],
    'how_eyebrow': 'How it works',
    'how_h2': 'Really this simple',
    'how_lead': 'Message us the way you would message a friend who is picking you up. We take care of the rest.',
    'steps': [
        ('One message', 'From where to where, day, time and how many of you. One WhatsApp and that\'s it. No forms, no accounts.'),
        ('One person', 'A real person replies, not a bot. Once you confirm, we tell you who your driver is, the car and the plate, and we reconfirm the day before.'),
        ('One price', 'The one we gave you in writing, with no extras and no surprises. We arrive on time. You pay when you reach your destination.'),
    ],
    'dest_eyebrow': 'Destinations',
    'dest_h2': 'Private transfers wherever you want to go',
    'dest_lead': 'Fixed price per car, not per person, in writing before you confirm. Door to door: to dinner, the beach, golf, a wedding or the airport. These are the areas where we drive most; for anywhere else, just ask.',
    'dest_cta': 'Get a fixed price →',
    'dest_wa': 'Hi, I would like a transfer from [pickup] to {to} on [date] at [time], we are [n] people',
    'also': 'Also:',
    'chips': [
        ('Málaga Airport', 'Hi, I would like a transfer to or from Málaga Airport'),
        ('Port and María Zambrano station', 'Hi, I need a transfer from Málaga port or train station'),
        ('Weddings and events', 'Hi, I would like a quote for wedding or event transfers'),
        ('Golf', 'Hi, I would like a transfer to a golf course'),
        ('Ronda, Granada, Seville, Gibraltar', 'Hi, I would like a day trip to [city]'),
        ('Driver by the hour', 'Hi, I would like a driver by the hour'),
        ('Hotels, rentals and companies', 'Hi, I manage accommodation and need regular transfers'),
    ],
    'team_eyebrow': 'Who we are',
    'team_h2': 'Three people from Mijas, not an app with 500 cities',
    'team_lead': 'Your WhatsApp is answered by someone who knows where your urbanización, villa or golf course is.',
    'team_lead_photos': 'Real photos, real cars. ',
    'roles': {'coord': 'He is the one who replies. He coordinates bookings and reconfirms the day before.', 'driver': 'Driver.'},
    'role_alt': {'coord': 'booking coordinator at {brand}', 'driver': 'driver at {brand}'},
    'reviews_h2': 'What our passengers say',
    'reviews_all': 'See all on Google →',
    'stars_label': '5 stars',
    'faq_h2': 'Frequently asked questions',
    'faq': [
        ('How much does a private transfer cost?', 'It depends on the route and the time of day, and it is always a fixed price per car, not per person. Message us on WhatsApp with your pickup, destination, day and time, and we will give you the exact price in writing before you confirm. That is what you pay on arrival, with no extras and no surprises.', []),
        ('How do I book a driver? Can I book on WhatsApp?', 'Yes: {brand} bookings are made on WhatsApp only. Send us your pickup, destination, day, time and number of passengers. A real person replies with a fixed price in writing and, once you confirm, sends you the driver\'s name, the car and the plate. We reconfirm the day before.', []),
        ('Do I have to pay for the transfer in advance?', 'No. With {brand} you pay nothing when you book: you pay the driver when you are dropped off, in cash, by card or with Bizum. The price is the one we gave you in writing when you booked. If you need an invoice, we will issue one.', []),
        ('What is the difference between a VTC and a taxi in Málaga?', 'Price and booking. A taxi charges by the meter at the official rate, which is higher at night and on public holidays, and you can take one at a rank. A VTC like {brand} charges a fixed price agreed before the ride and can only work with a prior booking, so you know what you will pay before you get in.', []),
        ('Are you legal? Do you have a licence?', 'Yes. {brand} is a company with VTC licence no. {vtc} from the Junta de Andalucía for passenger transport with a driver. As the law requires, we only work with prior bookings: your WhatsApp confirmation is the contract. That is why we never pick up passengers on the street or at ranks without a booking.', []),
        ('What does the price include? Are there any extras?', 'Everything for the ride. The fixed price {brand} gives you on WhatsApp includes {included}, so there are no extras and no surprises: on arrival you pay exactly the amount we agreed, in cash, by card or with Bizum.', ['INCLUDED']),
        ('How many people fit in the car?', 'Up to {pax} passengers per car, with their luggage. If there are more of you, or you are bringing golf bags or a lot of luggage, tell us when you book on WhatsApp and we will suggest the best option for your group, always with a fixed price before you confirm.', ['MAX_PAX']),
        ('Which rides do you do?', 'Any ride inside or outside the province of Málaga: the airport, the port and María Zambrano station, dinners and nights out, golf courses, weddings, day trips to Ronda, Granada, Seville or Gibraltar, and hourly driver hire. {brand} is based in Mijas and drives all along the Costa del Sol, always with a fixed price before we set off.', []),
        ('Do you do rides within the same town, or only between towns?', 'Both. {brand} does rides within the same town, such as from your home to a restaurant in Marbella or from Málaga city centre to the airport, and between towns all along the Costa del Sol, such as Mijas to Marbella or La Cala to Fuengirola. Always with a fixed price per car before we set off.', []),
        ('Can I cancel a transfer?', 'Yes, free of charge up to 24 hours before the ride. A WhatsApp message is enough. Since you pay nothing in advance with {brand}, there is nothing to refund and no paperwork: just let us know as soon as you can so we can free up the car.', []),
    ],
    'cta_h2': 'Ready to go?',
    'cta_final': 'Book my transfer',
    'cta_p': 'One WhatsApp message and you have a fixed price in a minute.',
    'footer_tag': 'Private transfers & driver · Mijas, Málaga',
    'footer_vtc': 'VTC licence no. {vtc} · Pre-booked service only; we do not pick up passengers without a prior booking.',
    'footer_transfers': 'Transfers',
    'footer_links': ['Transfers in Mijas and La Cala', 'Transfers in Fuengirola and Benalmádena', 'Transfers in Marbella', 'Málaga Airport transfers', 'Driver for weddings, golf and day trips'],
    'footer_legal': 'Legal (in Spanish)',
    'wa_float': 'Message us on WhatsApp',
    'ld_desc': 'Licensed (VTC) private transfers and driver service in Málaga and the Costa del Sol. Book on WhatsApp, fixed price, pay on arrival.',
    'offers': ['Málaga Airport transfers', 'Wedding and event driver', 'Costa del Sol golf transfers', 'Hourly driver and day trips'],
    'payment': 'Cash, card, Bizum',
},
}

# Zonas donde más trabajamos (tarjetas de Destinos).
DEST = [
    {'es': ('Mijas Pueblo', 'Pueblo, Mijas Golf, Osunillas y Valtocado.', 'Mijas Pueblo'),
     'en': ('Mijas Pueblo', 'The village, Mijas Golf, Osunillas and Valtocado.', 'Mijas Pueblo')},
    {'es': ('La Cala y Mijas Costa', 'La Cala, Calahonda, Riviera, Miraflores, El Chaparral.', 'La Cala de Mijas'),
     'en': ('La Cala and Mijas Costa', 'La Cala, Calahonda, Riviera, Miraflores, El Chaparral.', 'La Cala de Mijas')},
    {'es': ('Fuengirola', 'Los Boliches, Torreblanca, Carvajal y centro.', 'Fuengirola'),
     'en': ('Fuengirola', 'Los Boliches, Torreblanca, Carvajal and the centre.', 'Fuengirola')},
    {'es': ('Benalmádena y Torremolinos', 'Costa, pueblo y Arroyo de la Miel.', 'Benalmádena'),
     'en': ('Benalmádena and Torremolinos', 'Coast, village and Arroyo de la Miel.', 'Benalmádena')},
    {'es': ('Marbella', 'Centro, Elviria, Puerto Banús, San Pedro.', 'Marbella'),
     'en': ('Marbella', 'Centre, Elviria, Puerto Banús, San Pedro.', 'Marbella')},
    {'es': ('Málaga centro', 'Centro histórico, puerto y estación María Zambrano.', 'Málaga centro'),
     'en': ('Málaga city centre', 'Old town, port and María Zambrano station.', 'Málaga city centre')},
]

# Zonas servidas (JSON-LD areaServed): nombres propios, iguales en los dos idiomas.
AREA = ['Mijas', 'Fuengirola', 'Benalmádena', 'Torremolinos', 'Marbella', 'Málaga']


# Qué incluye el precio (config.INCLUDED los referencia por clave). (ES, EN).
INCLUDED_LABELS = {
    'toll': ('el peaje de autopista', 'motorway tolls'),
    'night': ('el servicio de noche', 'night service'),
    'luggage': ('el equipaje', 'luggage'),
}


def _brand(x):
    """La marca vive en config.BRAND: aquí se pone en todos los textos, una vez."""
    if isinstance(x, str):
        return x.replace('{brand}', BRAND)
    if isinstance(x, dict):
        return {k: _brand(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return type(x)(_brand(v) for v in x)
    return x

T, DEST = _brand(T), _brand(DEST)
