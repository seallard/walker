from neat.genome import Genome
from neat.network import Network
from neat.enums.node_types import NodeType
from unittest.mock import Mock
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

def test_create_nework(standard_config):
    genome = Genome(id=1, config=standard_config)
    network = genome.network()

    assert len(network.nodes) == len(genome.nodes)
    assert len(network.links) == len(genome.links)


def test_create_network_with_disabled_links(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.links[0].enabled = False
    network = genome.network()

    assert len(network.links) == len(genome.links) - 1
    assert len(network.nodes) == len(genome.nodes)


def test_create_network_with_loops(genome):
    genome.mutate_add_node()
    genome.add_loop_link()
    network = genome.network()
    assert len(network.links) == len(genome.links) - 1


def test_activate_without_hidden_nodes(genome):
    network = genome.network()
    output = network.activate(inputs=[0])[0]

    assert output == sigmoid(0)

    #output = network.activate(inputs=[1])
    #assert output == [sigmoid(network.links[0].weight)]


def test_activate_with_hidden_nodes(genome):
    genome.mutate_add_node()

    network = genome.network()
    output = network.activate(inputs=[1])[0]
    output_of_hidden_node = network.nodes[-1].output

    assert output_of_hidden_node == sigmoid(network.links[0].weight)
    assert output == sigmoid(sigmoid(network.links[0].weight) * network.links[1].weight)


def test_activate_with_multiple_inputs(multiple_inputs_config):
    genome = Genome(id=1, config=multiple_inputs_config)
    network = genome.network()

    output = network.activate(inputs=[0,0])
    assert output == [sigmoid(0)]

    output = network.activate(inputs=[1,1])
    assert output == [sigmoid(network.links[0].weight + network.links[1].weight)]


def test_activate_with_multiple_outputs(multiple_input_output_config):
    genome = Genome(id=1, config=multiple_input_output_config)
    network = genome.network()

    outputs = network.activate(inputs=[0, 0])
    assert outputs == [sigmoid(0), sigmoid(0)]

    outputs = network.activate(inputs=[1, 1])
    w11 = network.links[0].weight
    w12 = network.links[1].weight
    w21 = network.links[2].weight
    w22 = network.links[3].weight
    assert outputs == [sigmoid(w11 + w21), sigmoid(w12 + w22)]

