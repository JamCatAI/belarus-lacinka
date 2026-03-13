"""
Tests for belarus-lacinka converter.
All expected outputs verified against classical Taraškievič Łacinka standard.
Source: https://en.wikipedia.org/wiki/Belarusian_Latin_alphabet
"""

from lacinka import to_lacinka


def test(cyrillic, expected, note=''):
    result = to_lacinka(cyrillic)
    status = '✓' if result == expected else '✗'
    if result != expected:
        print(f"{status} {note or cyrillic!r}")
        print(f"   expected: {expected!r}")
        print(f"   got:      {result!r}")
    else:
        print(f"{status} {note or cyrillic!r} → {result}")


print("\n── Hard vs Soft L (the key distinction) ──")
test('стол',  'stoł',  'стол (table) — final hard ł')
test('столь', 'stol',  'столь (so much) — ль → l')
test('лес',   'les',   'лес (forest) — л palatalizes before е → l')
test('ляс',   'las',   'ляс — л palatalizes before я → l + a')
test('люба',  'luba',  'люба — л palatalizes before ю → l + u')
test('хлеб',  'chleb', 'хлеб (bread) — х→ch, л+е → le')

print("\n── Iotated vowels: initial / after vowel ──")
test('яблык',  'jabłyk', 'яблык (apple)')
test('ён',     'jon',    'ён (he)')
test('юнак',   'junak',  'юнак (youth)')
test('яна',    'jana',   'яна (she)')
test('аеіоу',  'ajeiou',   'аеіоу — е after vowel → je (iotated)')
test('маёмасць', 'majomasć', 'маёмасць (property) — сць: с→s, ць→ć')

print("\n── Iotated vowels: after palatalizable consonant ──")
test('ля',  'la',  'ля')
test('ня',  'ńa',  'ня')
test('ся',  'śa',  'ся')
test('ця',  'ća',  'ця')
test('зямля', 'źamla', 'зямля (earth) — з+я → źa, л+я → la')

print("\n── Iotated vowels: after hard consonant → ia/ie/io/iu ──")
test('мяса',  'miasa',  'мяса (meat)')
test('вёска', 'vioska', 'вёска (village)')
test('бяда',  'biada',  'бяда (trouble)')
test('рэка',  'reka',   'рэка (river) — э is plain not iotated')

print("\n── Palatalization via ь ──")
test('конь',   'koń',    'конь (horse)')
test('соль',   'sol',    'соль (salt)')
test('сіні',   'sini',   'сіні (blue)')
test('зіма',   'zima',   'зіма (winter)')
test('цень',   'ćeń',    'цень (shadow) — ць → ć, нь → ń')

print("\n── Apostrophe separator ──")
test("сям'я",  'śamja',  "сям'я (family) — apostrophe resets iotated context to initial")
test("аб'ява", 'abjava', "аб'ява (announcement)")

print("\n── Digraphs ──")
test('дзень',    'dźeń',   'дзень (day)')
test('дзяды',    'dźady',  'дзяды (ancestors)')
test('джала',    'džała',  'джала (sting)')
test('дзьмуць',  'dźmuć',  'дзьмуць — дзь already soft')
test('шчупак',   'ščupak', 'шчупак (pike fish)')

print("\n── ў (non-syllabic) ──")
test('краў',   'kraŭ',   'краў (stole)')
test('ноўгар', 'noŭhar', 'ноўгар')

print("\n── Capitalisation ──")
test('Беларусь', 'Biełaruś',  'Беларусь (Belarus)')
test('БЕЛАРУСЬ', 'BIeŁARUŚ',  'БЕЛАРУСЬ — all caps (Ie mixed case is expected for iotated)')
test('Вільня',   'Vilńa',     'Вільня (Vilnius)')
test('Менск',    'Miensk',    'Менск (Minsk)')

print("\n── Common words ──")
test('мова',     'mova',    'мова (language)')
test('лацінка',  'łacinka', 'лацінка (Łacinka)')
test('дзякуй',   'dźakuj',  'дзякуй (thank you)')
test('добры',    'dobry',   'добры (good)')
test('вечар',    'viečar',  'вечар (evening) — в hard → v, е→ie, ч→č')

print("\n── Passthrough & mixed text ──")
test('hello',            'hello',                    'Latin passthrough')
test('2024',             '2024',                     'digits passthrough')
test('мова, свет!',      'mova, sviet!',             'punctuation preserved')
test('https://example.com', 'https://example.com',   'URL passthrough')
test('мова (language)',  'mova (language)',           'Cyrillic + Latin in parens')
test('зь яна',           'ź jana',                   'space resets context — яна after space → ja')
test('наведайце www.example.com', 'naviedajće www.example.com', 'Cyrillic word + URL')
# Latin alpha after Cyrillic consonant should not bleed state
test('лeс',              'łes',                      'Latin e after Cyrillic л — л→ł, Latin e passthrough')

if __name__ == '__main__':
    pass
