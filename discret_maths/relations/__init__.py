# Standar import
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Set,
    Tuple,
)

# Third imports
import oyaml as yaml
from networkx import DiGraph

# Local import
from discret_maths.utils import get_set_combination
from discret_maths.relations.transform import to_hasse
from discret_maths.relations.extract import (
    get_all_ci,
    get_all_cs,
    get_all_mci,
    get_all_mcs,
    get_bounded,
    get_complements,
    get_inverse,
    get_mci,
    get_mcs,
    get_not_symmetric,
    get_not_transitive,
    get_reflexive,
    get_relations,
    get_symmetric,
    get_transitive,
)
from discret_maths.relations.check import (
    is_anti_reflexive,
    is_anti_symmetric,
    is_bounded,
    is_booblean_algebra,
    is_complemented,
    is_distributed,
    is_equivalent,
    is_not_reflexive,
    is_not_symmetric,
    is_not_transitive,
    is_partial_order,
    is_reflexive,
    is_strict_order,
    is_symmetric,
    is_total_order,
    is_transitive,
)

STRICT: bool = True


def draw_graph(
    graph: DiGraph,
    domain: Set[Any],
    images: Optional[Set[Any]] = None,
) -> None:
    for node in domain.union(images or set()):
        graph.add_node(node, label=node)


def draw_relation(
    graph: DiGraph,
    relations: Set[Tuple[Any, Any]],
    inverse: bool = False,
) -> None:
    for node_x, node_y in relations:
        if inverse:
            graph.add_edge(node_y, node_x, color='blue')
            continue
        graph.add_edge(node_x, node_y, color='blue')


def relations_to_str(relations: Tuple[Tuple[Any, Any], ...]) -> str:
    result = str()
    for node_x, node_y in relations:
        result += f'({node_x}, {node_y}), '
    return result


def generate_relations(
    nodes: Set[int],
    condition: Callable[[int, int], bool],
    inverse: bool = False,
) -> Iterator[Tuple[int, int]]:
    for node_x, node_y in get_set_combination(nodes):
        if condition(node_x, node_y):
            if inverse:
                yield (node_y, node_x)
                continue
            yield (node_x, node_y)


def is_lattice(graph: DiGraph) -> bool:
    nodes = graph.nodes

    return all(
        get_mcs(graph, x, y) and get_mci(graph, x, y)
        for x, y in get_set_combination(nodes) if x != y)


def generate_report(graph: DiGraph) -> None:
    hasse_graph = to_hasse(graph)
    lattice = is_lattice(hasse_graph)

    report = {
        'relations_type': {
            'reflexive': is_reflexive(graph),
            'anti_reflexive': is_anti_reflexive(graph),
            'not_reflexive': is_not_reflexive(graph),
            'symmetric': is_symmetric(graph),
            'anti_symmetric': is_anti_symmetric(graph),
            'not_symmetric': is_not_symmetric(graph),
            'transitive': is_transitive(graph),
            'not_transitive': is_not_transitive(graph),
            'equivalent': is_equivalent(graph),
            'strict_order': is_strict_order(graph),
            'partial_order': is_partial_order(graph),
            'total_order': is_total_order(graph),
        },
        'relented_nodes': {
            'relations':
            list(f'({x}, {y})' for x, y in get_relations(graph)),
            'inverse':
            list(f'({x}, {y})' for x, y in get_inverse(graph)),
            'reflexive': [f'({x}, {y})' for x, y in get_reflexive(graph)],
            'symmetry': [
                f'({a[0]}, {a[1]}), ({b[0]}, {b[1]})'
                for a, b in get_symmetric(graph)
            ],
            'not_symmetric': [
                f'({a[0]}, {a[1]}), ({b[0]}, {b[1]})'
                for a, b in get_not_symmetric(graph)
            ],
            'transitive': [
                f'({x[0]}, {x[1]}), ({y[0]}, {y[1]}), ({z[0]}, {z[1]})'
                for x, y, z in get_transitive(graph)
            ],
            'not_transitive': [
                f'({x[0]}, {x[1]}), ({y[0]}, {y[1]}), ({z[0]}, {z[1]})'
                for x, y, z in get_not_transitive(graph)
            ],
        },
        'is_lattice':
        lattice,
        'lattice_is_bounded':
        is_bounded(hasse_graph),
        'maximum':
        get_bounded(hasse_graph)[1],
        'minimum':
        get_bounded(hasse_graph)[0],
        'lattice_is_complemented':
        is_complemented(hasse_graph),
        'complements':
        get_complements(hasse_graph),
        'is_boolean_algebra':
        is_booblean_algebra(hasse_graph),
        'is_distributed': is_distributed(hasse_graph),
        'lower_bounds':
        list(
            set(f'{nodes}, {bounds}'
                for nodes, bounds in get_all_ci(hasse_graph))),
        'upper_bounds':
        list(
            set(f'{nodes}, {bounds}'
                for nodes, bounds in get_all_cs(hasse_graph))),
        'maximun_lower_bounds':
        list(
            set(f'{nodes}, {bounds}'
                for nodes, bounds in get_all_mci(hasse_graph))),
        'minimum_upper_bounds':
        list(
            set(f'{nodes}, {bounds}'
                for nodes, bounds in get_all_mcs(hasse_graph))),
    }

    with open('report.yaml', 'w') as streamer:
        yaml.dump(report, streamer)
