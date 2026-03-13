# Classical Łacinka transliteration rules
# Based on Taraškievič (1929) standard as documented in:
# - Wikipedia: https://en.wikipedia.org/wiki/Belarusian_Latin_alphabet
# - BINIM: https://binim.org/index.php/transliteration/
#
# NOT the 2007/2008 Belarusian government geographical romanization,
# which inverts Л/Ль: (л=l, ль=ĺ) vs classical (л=ł, ль=l)

# Simple 1:1 consonant mappings (hard, non-palatalized)
CONSONANTS = {
    'б': 'b', 'Б': 'B',
    'в': 'v', 'В': 'V',
    'г': 'h', 'Г': 'H',
    'ґ': 'g', 'Ґ': 'G',  # plosive G, rare, abolished 1933 but present in classical
    'д': 'd', 'Д': 'D',
    'ж': 'ž', 'Ж': 'Ž',
    'з': 'z', 'З': 'Z',
    'й': 'j', 'Й': 'J',
    'к': 'k', 'К': 'K',
    'л': 'ł', 'Л': 'Ł',  # hard/dark L — ł, NOT plain l (that's the gov romanization)
    'м': 'm', 'М': 'M',
    'н': 'n', 'Н': 'N',
    'п': 'p', 'П': 'P',
    'р': 'r', 'Р': 'R',
    'с': 's', 'С': 'S',
    'т': 't', 'Т': 'T',
    'ф': 'f', 'Ф': 'F',
    'ш': 'š', 'Ш': 'Š',
    'ч': 'č', 'Ч': 'Č',
}

# Soft (palatalized) consonants — triggered by following ь or і/е/ё/ю/я after consonant
SOFT_CONSONANTS = {
    'л': 'l',  'Л': 'L',   # soft ль → plain l (opposite of hard ł)
    'н': 'ń',  'Н': 'Ń',
    'с': 'ś',  'С': 'Ś',
    'з': 'ź',  'З': 'Ź',
    'ц': 'ć',  'Ц': 'Ć',
    'дз': 'dź', 'ДЗ': 'Dź', 'Дз': 'Dź',
}

# Digraphs — must be checked before single-letter mappings
DIGRAPHS = {
    'дж': 'dž', 'ДЖ': 'Dž', 'Дж': 'Dž',
    'дз': 'dz', 'ДЗ': 'Dz', 'Дз': 'Dz',
    'дзь': 'dź', 'ДЗЬ': 'Dź', 'Дзь': 'Dź',
    'шч': 'šč', 'ШЧ': 'Šč', 'Шч': 'Šč',
    'х':  'ch', 'Х':  'Ch',
    'ц':  'c',  'Ц':  'C',
}

# Vowels (plain)
VOWELS = {
    'а': 'a', 'А': 'A',
    'э': 'e', 'Э': 'E',
    'і': 'i', 'І': 'I',
    'о': 'o', 'О': 'O',
    'у': 'u', 'У': 'U',
    'ў': 'ŭ', 'Ў': 'Ŭ',
    'ы': 'y', 'Ы': 'Y',
}

# Iotated vowels: three contexts
# Context A — word-initial or after a vowel: ja/je/jo/ju
# Context B — after soft consonant (ć, dź, l, ń, ś, ź): plain a/e/o/u (drop the j)
# Context C — after any other consonant: ia/ie/io/iu
IOTATED_INITIAL = {
    'я': 'ja', 'Я': 'Ja',
    'е': 'je', 'Е': 'Je',
    'ё': 'jo', 'Ё': 'Jo',
    'ю': 'ju', 'Ю': 'Ju',
}

IOTATED_AFTER_SOFT = {
    'я': 'a', 'Я': 'A',
    'е': 'e', 'Е': 'E',
    'ё': 'o', 'Ё': 'O',
    'ю': 'u', 'Ю': 'U',
}

IOTATED_AFTER_HARD = {
    'я': 'ia', 'Я': 'Ia',
    'е': 'ie', 'Е': 'Ie',
    'ё': 'io', 'Ё': 'Io',
    'ю': 'iu', 'Ю': 'Iu',
}

# Consonants whose Łacinka forms are "soft" (palatalized)
# After these, iotated vowels take the plain form (context B)
SOFT_LACINKA_CONSONANTS = {'l', 'L', 'ń', 'Ń', 'ś', 'Ś', 'ź', 'Ź', 'ć', 'Ć', 'dź', 'Dź'}

# Cyrillic vowels (for context detection)
CYR_VOWELS = set('аеёіоуыэюяАЕЁІОУЫЭЮЯ')

# Cyrillic consonants that become soft in Łacinka
# (i.e., their Łacinka output is in SOFT_LACINKA_CONSONANTS)
SOFTENING_CYRILLIC = {'л', 'Л', 'н', 'Н', 'с', 'С', 'з', 'З', 'ц', 'Ц'}
