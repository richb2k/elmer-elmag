import os
from pathlib import Path

import pydot
from elmer_circuitbuilder import (Circuit, ElmerComponent, I,
                                  generate_elmer_circuits, number_of_circuits)


def create_circuit(dir_out: Path):
    """Creates circuit definition file for Elmer.

    Args:
        dir_out: Directory the circuit definition file is written to

    Returns:
        Filename of the circuit definition file.
    """
    # initialize circuits: number of circuits - do not remove
    c = number_of_circuits(1)
    # reference/ground node needed - do not remove.
    c[1].ref_node = 1

    # Components
    peak_current = 6.0
    current_0 = I("I_0", 1, 2, peak_current)
    current_1 = I("I_1", 1, 3, peak_current)
    current_2 = I("I_2", 1, 4, peak_current)
    currents = [current_0, current_1, current_2]

    phase_0 = ElmerComponent("Phase_0", 2, 1, 1, [2, 3], 1)
    phase_1 = ElmerComponent("Phase_1", 3, 1, 2, [6, 7], 1)
    phase_2 = ElmerComponent("Phase_2", 4, 1, 3, [4, 5], 1)
    phases = [phase_0, phase_1, phase_2]
    for phase in phases:
        n_turns = 35
        resistance = 0.8 / float(n_turns)
        phase.stranded(n_turns, resistance)

    components = [*currents, *phases]

    # store components in array components = [comp1, comp2,...] - do not remove
    c[1].components.append(components)

    fname_out = "circuit.definition"
    path_out = dir_out / fname_out
    if os.path.exists(path_out):
        os.remove(path_out)

    # generate elmer circuit.definitions - do not remove / do not edit
    generate_elmer_circuits(c, path_out)

    return c

def plot_circuit(c: Circuit, fname: Path):
    """Plots the circuit."""
    graph = pydot.Dot(graph_type="digraph")
    pins = []

    # Add components as graph nodes
    for comp in c[1].components[0]:
        pins.append(comp.pin1)
        pins.append(comp.pin2)
        graph.add_node(
            pydot.Node(comp.name, style="filled", fillcolor="turquoise", shape="box")
        )

    # Add nodes/pins as graph nodes
    pins = list(set(pins))
    for pin in pins:
        graph.add_node(
            pydot.Node(f"Node_{pin}", style="filled", fillcolor="red", shape="box")
        )

    # Connect components and nodes/pins
    for comp in c[1].components[0]:
        edge = pydot.Edge(f"Node_{comp.pin1}", comp.name)
        graph.add_edge(edge)
        edge = pydot.Edge(comp.name, f"Node_{comp.pin2}")
        graph.add_edge(edge)

    save = getattr(graph, f"write_{fname.suffix.replace('.', '')}")
    save(fname)


if __name__ == "__main__":
    # Change path to your case directory
    path = Path(__file__).parent
    circuit = create_circuit(Path(path))
    plot_circuit(circuit, path / "circuit.png")

   

   

