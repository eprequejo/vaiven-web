# -*- coding: utf-8 -*-
"""python3 -m unittest src/test_check.py  — el gate debe pasar con datos completos y caer con cada rotura."""
import os, re, shutil, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
CIF_REAL, ADDRESS_REAL = config.CIF, config.LEGAL_ADDRESS  # antes de que FAKE los sustituya

FAKE = dict(DOMAIN='example.test', PHONE='34600000000', VTC_NO='MA-0000', RAZON_SOCIAL='Prueba S.L.',
            CIF='B00000000', LEGAL_ADDRESS='Calle Prueba 1, Mijas', EMAIL='hola@example.test',
            PRICES=[('airport', 'mijas', 45), ('mijas', 'marbella', 55), ('lacala', 'fuengirola', 30), ('airport', 'marbella', 75)],
            MAX_PAX=4, MAX_BAGS=4, INCLUDED=['toll', 'night', 'luggage'])
for k, v in FAKE.items():
    setattr(config, k, v)
import build, check  # build lee config al importarse: después de rellenarlo


class Gate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = tempfile.mkdtemp()
        build.build(cls.good)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.good)

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        shutil.copytree(self.good, self.dir, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def edit(self, rel, old, new):
        p = os.path.join(self.dir, rel)
        txt = open(p, encoding='utf-8').read()
        self.assertIn(old, txt)
        open(p, 'w', encoding='utf-8').write(txt.replace(old, new, 1))

    def errors(self):
        return check.run(self.dir, domain='example.test')

    def assertFails(self, needle):
        errs = self.errors()
        self.assertTrue(any(needle in e for e in errs), f'esperaba "{needle}" en {errs}')

    def test_complete_site_passes(self):
        self.assertEqual(self.errors(), [])

    def test_hole(self):
        self.edit('index.html', 'MA-0000', 'HUECO:VTC_NO')
        self.assertFails('hueco sin rellenar: VTC_NO')

    def test_template_hole(self):
        self.edit('index.html', 'Prueba S.L.', '[RAZÓN SOCIAL]')
        self.assertFails('hueco sin rellenar: [RAZÓN SOCIAL]')

    def test_wrong_domain(self):
        self.assertTrue(any('esperado https://otro.test' in e for e in check.run(self.dir, domain='otro.test')))

    def test_one_way_hreflang(self):
        self.edit('en/index.html', '<link rel="alternate" hreflang="es" href="https://example.test/">\n', '')
        self.assertFails('hreflang no recíproco')

    def test_bad_jsonld(self):
        self.edit('index.html', '"@graph":[', '"@graph":[,')
        self.assertFails('JSON-LD no parsea')

    def test_faq_diverges(self):
        self.edit('index.html', '<summary>¿Puedo cancelar un transfer?', '<summary>¿Puedo anular un transfer?')
        self.assertFails('FAQPage no coinciden')

    def test_broken_link(self):
        self.edit('index.html', 'href="/privacidad/"', 'href="/privacy/"')
        self.assertFails('enlace roto /privacy/')

    def test_broken_anchor(self):
        self.edit('index.html', 'id="faq"', 'id="preguntas"')
        self.assertFails('ancla inexistente')

    def test_two_h1(self):
        self.edit('index.html', '<h2>Preguntas frecuentes</h2>', '<h1>Preguntas frecuentes</h1>')
        self.assertFails('2 <h1>')

    def test_long_title(self):
        self.edit('en/index.html', '<title>', '<title>' + 'x' * 30)
        self.assertFails('title de')

    def test_noindex_on_home(self):
        self.edit('index.html', 'content="index,follow', 'content="noindex,follow')
        self.assertFails('sitemap')

    def test_canonical(self):
        self.edit('en/index.html', '<link rel="canonical" href="https://example.test/en/">', '<link rel="canonical" href="https://example.test/">')
        self.assertFails('canonical')

    def test_external_css(self):
        self.edit('index.html', '</head>', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit"></head>')
        self.assertFails('hoja de estilos externa')

    def test_internal_file_published(self):
        open(os.path.join(self.dir, 'notas.md'), 'w').write('x')
        self.assertFails('no debe publicarse: notas.md')

    def test_html_budget(self):
        self.edit('index.html', '</main>', os.urandom(20000).hex() + '</main>')
        self.assertFails('bytes gzip')

    def test_no_phone_calls(self):
        self.edit('index.html', '</main>', '<a href="tel:+34600000000">Llámanos</a></main>')
        self.assertFails('enlace de llamada')

    def test_no_telephone_in_jsonld(self):
        self.edit('index.html', '"@type":"LocalBusiness",', '"@type":"LocalBusiness","telephone":"+34600000000",')
        self.assertFails('telephone en JSON-LD')

    def first_answer(self, rel):
        txt = open(os.path.join(self.dir, rel), encoding='utf-8').read()
        return re.search(r'<details><summary>[^<]*</summary><p>([^<]*)</p>', txt).group(1)

    def replace_answer(self, rel, new):
        """Cambia la primera respuesta en el <details> y en el FAQPage a la vez (siguen coincidiendo)."""
        p = os.path.join(self.dir, rel)
        old = self.first_answer(rel)
        txt = open(p, encoding='utf-8').read()
        self.assertEqual(txt.count(old), 2)
        open(p, 'w', encoding='utf-8').write(txt.replace(old, new))

    def test_faq_answer_too_short(self):
        self.replace_answer('index.html', 'Sí, claro.')
        self.assertFails('palabras')

    def test_faq_answer_too_long(self):
        self.replace_answer('en/index.html', ' '.join(['word'] * 120))
        self.assertFails('palabras')

    def test_faq_visible_answer_differs_from_jsonld(self):
        self.edit('index.html', self.first_answer('index.html'), 'Otra respuesta distinta a la del JSON-LD, ' * 4)
        self.assertFails('respuesta visible')

    def test_faq_price_not_in_table(self):
        self.edit('index.html', '<td>55 €</td>', '<td>99 €</td>')
        self.assertFails('precio')

    def test_lang(self):
        self.edit('en/index.html', '<html lang="en">', '<html lang="es">')
        self.assertFails('lang="es", esperado "en"')


class TitularMirror(unittest.TestCase):
    """El titular es el mismo que el de Nautelia: si allí cambia el CIF, aquí debe cambiar también."""
    NAUTELIA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'nautelia-landing', 'src', 'parts.py')

    # Sin skipUnless: un guard entre repos que se salta solo cuando falta el otro repo se apaga
    # sin avisar (lección de Padelia, CLAUDE.md). Saltarlo es un acto explícito: VAIVEN_SKIP_MIRROR=1.
    def test_cif_matches_nautelia(self):
        if os.environ.get('VAIVEN_SKIP_MIRROR') == '1':
            self.skipTest('VAIVEN_SKIP_MIRROR=1')
        self.assertTrue(os.path.exists(self.NAUTELIA), f'falta el espejo {self.NAUTELIA}')
        with open(self.NAUTELIA, encoding='utf-8') as f:
            src = f.read()
        self.assertEqual(re.search(r"^CIF = '([^']+)'", src, re.M).group(1), CIF_REAL)

    def test_address_matches_nautelia(self):
        if os.environ.get('VAIVEN_SKIP_MIRROR') == '1':
            self.skipTest('VAIVEN_SKIP_MIRROR=1')
        path = os.path.join(os.path.dirname(self.NAUTELIA), 'build.py')
        self.assertTrue(os.path.exists(path), f'falta el espejo {path}')
        with open(path, encoding='utf-8') as f:
            src = f.read()
        self.assertEqual(re.search(r"^ADDRESS = '([^']+)'", src, re.M).group(1), ADDRESS_REAL)


class NoInventedData(unittest.TestCase):
    def test_without_prices_no_price_question_nor_table(self):
        saved = config.PRICES
        config.PRICES = []
        out = tempfile.mkdtemp()
        try:
            build.build(out)
            for rel in ('index.html', 'en/index.html'):
                txt = open(os.path.join(out, rel), encoding='utf-8').read()
                self.assertNotIn('class="prices"', txt)
                lang = 'en' if rel.startswith('en/') else 'es'
                price_q = next(q for q, a, needs in build.T[lang]['faq'] if 'PRICES' in needs)
                self.assertNotIn(price_q, txt)
                self.assertNotIn('€', re.sub(r'<script.*?</script>', '', txt, flags=re.S).split('id="faq"')[1])
            self.assertEqual(check.run(out, domain='example.test'), [])
        finally:
            config.PRICES = saved
            shutil.rmtree(out)


if __name__ == '__main__':
    unittest.main()
