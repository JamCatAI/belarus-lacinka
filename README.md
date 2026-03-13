# belarus-lacinka

Belarusian Cyrillic → Classical Łacinka converter (Python).

Implements the **Taraškievič (1929)** standard — the classical Łacinka used by *Naša Niva*, the Belarusian diaspora, and cultural publications.

## Why this exists

Many converters implement the **2007 Belarusian government geographical romanization** rather than classical Łacinka. The two systems differ in a fundamental way:

| | Classical Łacinka | Gov. romanization |
|--|--|--|
| Hard Л | **ł** | l |
| Soft Ль | **l** | ĺ |

This repo gets it right.

## Usage

```bash
# Convert a string
python cli.py "Беларусь мова"
# → Biełaruś mova

# Pipe
echo "Вільня" | python cli.py
# → Vilńa

# File
python cli.py --file input.txt
```

As a library:

```python
from lacinka import to_lacinka

to_lacinka("Беларусь")   # → 'Biełaruś'
to_lacinka("зямля")      # → 'źamla'
to_lacinka("дзень")      # → 'dźeń'
```

## Rules implemented

- **Hard L**: `л → ł`
- **Soft L**: `ль → l`, `ля → la`, `лю → lu`, etc.
- **Palatalizable consonants** (л н с з ц дз) automatically soften before iotated vowels
- **Iotated vowels** (я е ё ю) in three contexts:
  - Word-initial or after vowel: `ja je jo ju`
  - After soft consonant: plain `a e o u`
  - After hard consonant: `ia ie io iu`
- **Digraphs**: `дж → dž`, `дз → dz`, `дзь → dź`, `шч → šč`, `х → ch`
- **Apostrophe** resets iotated context (word boundary)

## Standard

Taraškievič, Branisłaŭ. *Biełaruskaja hramatyka dla škoł*, 5th ed. Vilnia, 1929.

Reference: [Belarusian Latin alphabet — Wikipedia](https://en.wikipedia.org/wiki/Belarusian_Latin_alphabet)
