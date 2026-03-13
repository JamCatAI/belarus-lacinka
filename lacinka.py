"""
belarus-lacinka: Belarusian Cyrillic → Classical Łacinka converter

Standard: Taraškievič (1929), classical Łacinka
NOT the 2007 Belarusian government geographical romanization.

Key difference from government romanization:
  Classical:   л → ł (hard),  ль → l (soft)
  Government:  л → l (hard),  ль → ĺ (soft)  ← what most converters incorrectly implement
"""

# ── Mapping tables ────────────────────────────────────────────────────────────

# Simple 1:1 consonants (hard, non-palatalized)
SIMPLE = {
    'б': 'b',  'Б': 'B',
    'в': 'v',  'В': 'V',
    'г': 'h',  'Г': 'H',
    'ґ': 'g',  'Ґ': 'G',
    'д': 'd',  'Д': 'D',
    'ж': 'ž',  'Ж': 'Ž',
    'з': 'z',  'З': 'Z',
    'й': 'j',  'Й': 'J',
    'к': 'k',  'К': 'K',
    'л': 'ł',  'Л': 'Ł',   # hard L → ł  (NOT plain l — that's the gov romanization)
    'м': 'm',  'М': 'M',
    'н': 'n',  'Н': 'N',
    'п': 'p',  'П': 'P',
    'р': 'r',  'Р': 'R',
    'с': 's',  'С': 'S',
    'т': 't',  'Т': 'T',
    'ф': 'f',  'Ф': 'F',
    'ч': 'č',  'Ч': 'Č',
    'ш': 'š',  'Ш': 'Š',
    'ц': 'c',  'Ц': 'C',
    'х': 'ch', 'Х': 'Ch',
    # vowels
    'а': 'a',  'А': 'A',
    'э': 'e',  'Э': 'E',
    'і': 'i',  'І': 'I',
    'о': 'o',  'О': 'O',
    'у': 'u',  'У': 'U',
    'ў': 'ŭ',  'Ў': 'Ŭ',
    'ы': 'y',  'Ы': 'Y',
    'и': 'i',  'И': 'I',   # Russian и — not standard Belarusian but appears in mixed texts
}

# Soft (palatalized) forms — applied when followed by ь or iotated vowel
SOFTEN = {
    'ł': 'l',   'Ł': 'L',    # ль → l
    'n': 'ń',   'N': 'Ń',    # нь → ń
    's': 'ś',   'S': 'Ś',    # сь → ś
    'z': 'ź',   'Z': 'Ź',    # зь → ź
    'c': 'ć',   'C': 'Ć',    # ць → ć
    'dz': 'dź', 'Dz': 'Dź',  # дзь → dź
}

# Iotated vowels — three forms depending on context
IOTATED = {
    #          initial/after-vowel   after-soft-cons   after-hard-cons
    'я': ('ja',  'a',  'ia'),  'Я': ('Ja',  'A',  'Ia'),
    'е': ('je',  'e',  'ie'),  'Е': ('Je',  'E',  'Ie'),
    'ё': ('jo',  'o',  'io'),  'Ё': ('Jo',  'O',  'Io'),
    'ю': ('ju',  'u',  'iu'),  'Ю': ('Ju',  'U',  'Iu'),
}

# Cyrillic consonants that palatalize before iotated vowels (and before ь)
PALATALIZABLE = {'л', 'Л', 'н', 'Н', 'с', 'С', 'з', 'З', 'ц', 'Ц'}
CYR_VOWELS = set('аеёіоуыэюяАЕЁІОУЫЭЮЯ')


# ── Converter ─────────────────────────────────────────────────────────────────

def to_lacinka(text: str) -> str:
    result = []
    i = 0
    n = len(text)

    # Tracks the last meaningful Cyrillic element for iotated vowel context:
    # 'start'         — beginning of word / after separator
    # 'vowel'         — last Cyrillic char was a vowel
    # 'palatalizable' — last Cyrillic char can become soft (л н с з ц, or дз digraph)
    # 'hard'          — last Cyrillic char was a non-palatalizable consonant
    prev_type = 'start'

    while i < n:
        ch = text[i]
        lo = ch.lower()

        # ── 3-char digraph: дзь ──────────────────────────────────────────────
        if text[i:i+3].lower() == 'дзь':
            result.append('Dź' if ch.isupper() else 'dź')
            prev_type = 'hard'  # дзь is already soft, treated as non-palatalizable
            i += 3
            continue

        # ── 2-char digraphs: дж дз шч ────────────────────────────────────────
        two = text[i:i+2].lower()
        if two == 'дж':
            result.append('Dž' if ch.isupper() else 'dž')
            prev_type = 'hard'
            i += 2
            continue
        if two == 'дз':
            result.append('Dz' if ch.isupper() else 'dz')
            prev_type = 'palatalizable'  # дз can become дзь (soft дзь)
            i += 2
            continue
        if two == 'шч':
            result.append('Šč' if ch.isupper() else 'šč')
            prev_type = 'hard'
            i += 2
            continue

        # ── Soft sign ь ───────────────────────────────────────────────────────
        if lo == 'ь':
            result = _soften_last(result)
            prev_type = 'hard'  # after softening, consonant is now definitively soft
            i += 1
            continue

        # ── Hard sign ъ and apostrophe ────────────────────────────────────────
        if lo in ('ъ', "'"):
            prev_type = 'start'
            i += 1
            continue

        # ── Iotated vowels я е ё ю ────────────────────────────────────────────
        if ch in IOTATED:
            forms = IOTATED[ch]  # (initial, after-soft, after-hard)
            if prev_type in ('start', 'vowel'):
                result.append(forms[0])
            elif prev_type == 'palatalizable':
                # The preceding consonant palatalizes → soften it, use plain vowel
                result = _soften_last(result)
                result.append(forms[1])
            else:
                result.append(forms[2])
            prev_type = 'vowel'
            i += 1
            continue

        # ── Plain Cyrillic (vowels + consonants) ──────────────────────────────
        if ch in SIMPLE:
            result.append(SIMPLE[ch])
            if ch in CYR_VOWELS:
                prev_type = 'vowel'
            elif ch in PALATALIZABLE:
                prev_type = 'palatalizable'
            else:
                prev_type = 'hard'
            i += 1
            continue

        # ── Non-Cyrillic: pass through ────────────────────────────────────────
        result.append(ch)
        prev_type = 'start'  # any non-Cyrillic char breaks context (Latin, digits, punctuation, URLs)
        i += 1

    return ''.join(result)


def _soften_last(result: list) -> list:
    """Replace the last Łacinka consonant token with its soft form."""
    if not result:
        return result

    # Check last two tokens first (for 'dz' → 'dź')
    if len(result) >= 2:
        two = result[-2] + result[-1]
        if two in SOFTEN:
            result[-2] = SOFTEN[two][0]
            result[-1] = SOFTEN[two][1] if len(SOFTEN[two]) > 1 else ''
            return [r for r in result if r]

    # Single token
    if result[-1] in SOFTEN:
        result[-1] = SOFTEN[result[-1]]

    return result
