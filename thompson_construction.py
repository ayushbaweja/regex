from dataclasses import dataclass
from typing import Callable, List


def EPSILON(_):
    return False


class State:
    pass


# Transition function
@dataclass
class Rule:
    start: State
    matcher: Callable[[str], bool]
    end: State

    def match(self, char: str) -> bool:
        return self.matcher(char)

    def is_epsilon(self) -> bool:
        return self.matcher == EPSILON


@dataclass
class Graph:
    label: str
    start: State
    end: State
    rules: List[Rule]


def match_eq(c):
    return lambda x: x == c


def single_char(char: str) -> Graph:
    start, end = State(), State()
    return Graph(char, start, end, [Rule(start, match_eq(char), end)])


# example = single_char('h')
# rule = example.rules[0]
# rule.match('h') -> True
# rule.match('j') -> False


# . in regex
def match_any():
    return lambda _: True


def any_char() -> Graph:
    start, end = State(), State()
    return Graph(".", start, end, [Rule(start, match_any(), end)])


# example = single_char('h')
# rule = example.rules[0]
# rule.match('h') -> True
# rule.match('j') -> True

# * Kleene Star
# 0 or more repetitions


def zero_or_more(test: Graph) -> Graph:
    start, end = State(), State()
    label = "(" + test.label + ")*"
    return Graph(
        label,
        start,
        end,
        [
            *test.rules,
            Rule(start, EPSILON, end),  # 0 occurances
            Rule(start, EPSILON, test.start),  # empty transition to start of test
            Rule(test.end, EPSILON, end),  # empty transition to end
            Rule(test.end, EPSILON, test.start),  # looping over test
        ],
    )


# Concatentation


def concat(left: Graph, right: Graph) -> Graph:
    label = left.label + right.label
    start = left.start
    end = right.end
    return Graph(
        label,
        start,
        end,
        [*left.rules, *right.rules, Rule(left.end, EPSILON, right.start)],
    )


# One or more +
def one_or_more(test: Graph) -> Graph:
    start, end = State(), State()
    label = "(" + test.label + ")+"
    return Graph(
        label,
        start,
        end,
        [
            *test.rules,
            # no direct path from start to end
            Rule(start, EPSILON, test.start),  # empty transition to start of test
            Rule(test.end, EPSILON, end),  # empty transition to end
            Rule(test.end, EPSILON, test.start),  # looping over test
        ],
    )


# Union |
def union(left: Graph, right: Graph) -> Graph:
    label = "(" + left.label + "|" + right.label + ")"
    start, end = State(), State()
    return Graph(
        label,
        start,
        end,
        [
            *left.rules,
            *right.rules,
            Rule(start, EPSILON, left.start),
            Rule(left.end, EPSILON, end),
            Rule(start, EPSILON, right.start),
            Rule(right.end, EPSILON, end),
        ],
    )


# Optional ?
# zero or one
def optional(test: Graph) -> Graph:
    label = "(" + test.label + ")?"
    start, end = State(), State()
    return Graph(
        label,
        start,
        end,
        [
            *test.rules,
            Rule(start, EPSILON, test.start),
            Rule(test.end, EPSILON, end),
            Rule(start, EPSILON, end),
            # no looping over from test endd to test start
        ],
    )
