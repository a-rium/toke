from __future__ import annotations

import argparse
import sys
import dataclasses

from enum import Enum


STATE_0 = 0
STATE_1 = 1


class TokenKind(Enum):
    SPACE = 0
    WORD = 1
    NUMBER = 2
    QUOTATION = 3
    PUNCTUATION = 4


@dataclasses.dataclass
class Token:
    kind: TokenKind
    text: str


def action0(text: str, at: int) -> tuple[int, int, Token]:
    length = 1
    if is_spacelike(text[at]):
        while at + length < len(text) and is_spacelike(text[at + length]):
            length += 1
        token = Token(kind=TokenKind.SPACE, text=text[at:at + length])
        return (STATE_0, at + length, token)
    elif is_numberlike(text[at]):
        while at + length < len(text) and is_numberlike(text[at + length]):
            length += 1
        token = Token(kind=TokenKind.NUMBER, text=text[at:at + length])
        return (STATE_1, at + length, token)
    elif is_wordlike(text[at]):
        while at + length < len(text) and is_wordlike(text[at + length]):
            length += 1
        token = Token(kind=TokenKind.WORD, text=text[at:at + length])
        return (STATE_1, at + length, token)
    elif is_quotation(text[at]):
        escaped = False
        quotation = text[at]
        while at + length < len(text):
            if quotation == text[at + length]:
                if escaped:
                    escaped = False
                else:
                    break
            if is_escape(text[at + length]):
                escaped = not escaped
            length += 1
        length += 1
        token = Token(kind=TokenKind.QUOTATION, text=text[at:at + length])
        return (STATE_1, at + length, token)
    elif is_punctuation(text[at]):
        token = Token(kind=TokenKind.PUNCTUATION, text=text[at:at + length])
        return (STATE_0, at + length, token)
    print('Panic!')
    exit(1)


def action1(text: str, at: int) -> tuple[int, int]:
    length = 1
    if is_spacelike(text[at]):
        while at + length < len(text) and is_spacelike(text[at + length]):
            length += 1
        token = Token(kind=TokenKind.SPACE, text=text[at:at + length])
        return (STATE_0, at + length, token)
    elif is_numberlike(text[at]) or is_wordlike(text[at]) or is_quotation(text[at]):
        print('Panic!')
        exit(1)
    elif is_punctuation(text[at]):
        token = Token(kind=TokenKind.PUNCTUATION, text=text[at:at + length])
        return (STATE_0, at + length, token)
    print('Panic!')
    exit(1)


ACTIONS = (action0, action1)


def is_numberlike(c: str) -> bool:
    return c.isnumeric()


def is_wordlike(c: str) -> bool:
    return c.isalnum()


def is_punctuation(c: str) -> bool:
    return True


def is_spacelike(c: str) -> bool:
    return c.isspace()


def is_quotation(c: str) -> bool:
    return c in {'"', "'", '`'}


def is_escape(c: str) -> bool:
    return c == '\\'


def parse_tokens(text: str) -> list[Token]:
    tokens = []
    state = STATE_0
    at = 0
    while at < len(text):
        state, at, token = ACTIONS[state](text, at)
        tokens.append(token)

    return tokens


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')

    args = parser.parse_args(sys.argv[1:])
    with open(args.inputfile, 'r') as f:
        text = f.read()

    parse_tokens(text)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
