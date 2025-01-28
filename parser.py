# Backus-Naur
# Start ::= Expression | EPSILON
# Expression ::= Term Expression | Term
# Term ::= Item Modifier | Item
# Modifier ::= '*' | '+'
# Item ::= Character | Group
# Character ::= 'A' | 'B'...
# Group ::= '(' Expression ')'

# Recursive Descent Parser

from dataclasses import dataclass
from __future__ import annotations 

@dataclass
class Start:
    content: Expression | None

def start(seq: list[str]) -> None | tuple[Start, list[str]]:
    exp_result = expression(seq)
    if exp_result:
        parsed_exp, after_exp = exp_result
        return Start(parsed_exp), after_exp
    return Start(None), seq

@dataclass
class Character:
    content: str

LITERAL_CHARS = "abcdefghijklmnopqrstuvwxyz"

def character(seq: list[str]) -> None | tuple[Character, list[str]]:
    if seq[0] in LITERAL_CHARS:
        char = seq[0]
        after_char = seq[1:]
        return Character(char), after_char
    return None

@dataclass
class Modifier:
    content: str

MOD_CHARS = "+*"

def modifier(seq: list[str]) -> None | tuple[Modifier, list[str]]:
    if seq[0] in MOD_CHARS:
        mod = seq[0]
        after_mod = seq[1:]
        return Modifier(mod), after_mod
    return None

@dataclass
class Item:
    content: Character | Group

def item(seq: list[str]) -> None | tuple[Item, list[str]]:
    char_result = character(seq)
    if char_result:
        parsed_char, after_char = char_result
        return Item(parsed_char), after_char
    group_result = group(seq)
    if group_result:
        parsed_group, after_group = group_result
        return Item(parsed_group), after_group
    return None

@dataclass
class Term:
    item: Item
    modifier: Modifier | None

def term(seq: list[str]) -> None | tuple[Term, list[str]]:
    item_result = item(seq)
    if item_result:
        parsed_item, after_item = item_result
        mod_result = modifier(after_item)
        if mod_result:
            parsed_mod, after_mod = mod_result
            return Term(parsed_item, parsed_mod), after_mod
        return Term(parsed_item), after_item
    return None


@dataclass
class Expression:
    term: Term
    next: Expression | None

def expression(seq: list[str]) -> None | tuple[Expression, list[str]]:
    term_result = term(seq)
    if term_result:
        parse_term, after_term = term_result
        exp_result = expression(after_term)
        if exp_result:
            parsed_exp, after_exp = exp_result
            return Expression(parse_term, parsed_exp), after_exp
        return Expression(parse_term), after_term
    return None

@dataclass
class Group:
    content: Expression

def group(seq: list[str]) -> None | tuple[Group, list[str]]:
    if seq[0] == '(':
        exp_result = expression(seq[1:])
        if exp_result:
            parsed_exp, after_exp = exp_result
            if after_exp[0] == ')':
                return Group(parsed_exp), after_exp[1:]
    return None

def parse(seq: str[]) -> Start | None:
    result = start(seq)
    if result:
        parsed, rest = result
        if len(rest) > 0:
            raise ValueError("Failed to parse whole input.")
        return parsed

ast = parse("(ha+)+")