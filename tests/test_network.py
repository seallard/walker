from neat.genome import Genome
from neat.network import Network
from neat.enums.node_types import NodeType
from unittest.mock import Mock
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

def test_create_nework():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    network = genome.network()

    assert len(network.nodes) == len(genome.nodes)
    assert len(network.links) == len(genome.links)


def test_create_network_with_disabled_links():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.links[0].enabled = False
    network = genome.network()

    assert len(network.links) == len(genome.links) - 1
    assert len(network.nodes) == len(genome.nodes)


def test_create_network_with_loops():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.mutate_add_node(tries=10, tracker=Mock())
    genome.add_loop(tries=50, tracker=Mock())
    network = genome.network()
    assert len(network.links) == len(genome.links) - 1


def test_updates_without_hidden_nodes():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    network = genome.network()

    output = network.update(inputs=[0])
    assert network.nodes[0].output == 0
    assert network.nodes[1].output == 0.5
    assert output == [0.5], "0 -> sigmoid -> 0.5"

    output = network.update(inputs=[1])
    assert output == [sigmoid(network.links[0].weight)]


def test_updates_with_hidden_nodes():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.mutate_add_node(tries=1, tracker=Mock())

    network = genome.network()
    final_output = network.update(inputs=[1])
    first_output = network.nodes[2].output

    assert first_output == sigmoid(network.links[-2].weight)
    assert final_output == [sigmoid(first_output * network.links[-1].weight)]
    for node in network.nodes:
        assert node.sum == 0, "net input signal to each node reset"


def test_update_with_multiple_inputs():
    genome = Genome(id=1, num_inputs=2, num_outputs=1)
    network = genome.network()

    output = network.update(inputs=[0,0])
    assert output == [sigmoid(0)]

    output = network.update(inputs=[1,1])
    assert output == [sigmoid(network.links[0].weight + network.links[1].weight)]


def test_update_with_multiple_outputs():
    genome = Genome(id=1, num_inputs=2, num_outputs=2)
    network = genome.network()

    outputs = network.update(inputs=[0, 0])
    assert outputs == [sigmoid(0), sigmoid(0)]

    outputs = network.update(inputs=[1, 1])
    w11 = network.links[0].weight
    w12 = network.links[1].weight
    w21 = network.links[2].weight
    w22 = network.links[3].weight
    assert outputs == [sigmoid(w11 + w21), sigmoid(w12 + w22)]


def test_update_with_loop():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.add_loop(tries=50, tracker=Mock())
    network = genome.network()

    output = network.update(inputs=[0])
    assert output == [sigmoid(0)], "correct output"

    output = network.update(inputs=[0])
    loop_weight = network.links[1].weight
    assert output == [sigmoid(sigmoid(0)*loop_weight)]
