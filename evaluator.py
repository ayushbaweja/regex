from dataclasses import dataclass

from thompson_construction import Graph


@dataclass
class Evaluator:
    graph: Graph
