#!/usr/bin/env python3
"""
belarus-lacinka CLI

Usage:
  echo "Беларусь" | python cli.py
  python cli.py "Беларусь мова"
  python cli.py --file input.txt
"""

import argparse
import sys
from lacinka import to_lacinka


def main():
    parser = argparse.ArgumentParser(
        description="Convert Belarusian Cyrillic to classical Łacinka (Taraškievič standard)",
        epilog="Standard: Taraškievič 1929. л→ł (hard), ль→l (soft). NOT the 2007 gov romanization.",
    )
    parser.add_argument("text", nargs="?", help="Text to convert (or pipe via stdin)")
    parser.add_argument("--file", "-f", help="Input file path")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    print(to_lacinka(text), end="")


if __name__ == "__main__":
    main()
