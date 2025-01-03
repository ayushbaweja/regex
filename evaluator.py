from dataclasses import dataclass
from typing import Set

from thompson_construction import Graph, State


@dataclass
class Evaluator:
    graph: Graph

    def match(self, string: str) -> bool:
        states = self.follow_epsilons(
            self.graph.start
        )  # states is all states reachable by epsilons
        for char in string:
            next_states = set()
            for rule in self.matching_rules(states, char):
                next_states.update(
                    self.follow_epsilons(rule.end)
                )  # follow epsilon transitions from each rules end state
            states = next_states
        return self.graph.end in states  # check end state in list of active states

    # all possible states reachable using epsilon transitions
    def follow_epsilons(self, state: State) -> Set[State]:
        possible = {state}
        for rule in self.graph.rules:
            if rule.is_epsilon() and state == rule.start:
                possible.update(self.follow_epsilons(rule.end))
        return possible

    # rules that match current state
    def matching_rules(self, states: Set[State], char: str):
        matching_rules = []
        for rule in self.graph.rules:
            if rule.start in states and rule.match(char):
                matching_rules.append(rule)
        return matching_rules
