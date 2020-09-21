from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest


@pytest.fixture(name='genome')
def initialised_genome():
    """Fully connected, no hidden layers. """
    num_inputs = 10
    num_outputs = 10
    genome_id = 1
    genome = Genome(genome_id, num_inputs, num_outputs)
    return genome


@pytest.fixture
def loopable_genome(genome):
    """Unrealistic genome in which each node is loopable. """
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome


@pytest.fixture
def unconnectable_genome(genome):
    """Unrealistic genome in which no node is loopable. """
    for node in genome.nodes:
        node.node_type = NodeType.BIAS
    return genome


@pytest.fixture
def connectable_genome(genome):
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome


def test_node_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"
    assert [x.innovation_number for x in genome.nodes] == [x for x in range(inputs + outputs)], "correct node innovation ids"
    assert [x.node_type for x in genome.nodes[:inputs]] == [NodeType.INPUT for x in range(inputs)], "correct type for inputs"
    assert [x.node_type for x in genome.nodes[inputs:]] == [NodeType.OUTPUT for x in range(outputs)], "correct type for outputs"


def test_link_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.links) == inputs * outputs, "correct number of links"

    ids = [x.innovation_number for x in genome.links]
    expected_ids = [x for x in range(inputs + outputs, inputs * outputs + inputs + outputs)]
    assert ids == expected_ids, "correct link innovation ids"

    assert True not in [x.recurrent for x in genome.links], "no initial link is recurrent"
    assert False not in [x.enabled for x in genome.links], "all initial links are enabled"

    assert genome.nodes[0].depth == 0, "depth of input node is 0"
    assert genome.nodes[-1].depth == 1, "depth of output node is 1"


def test_possible_loop(loopable_genome):
    original_number_of_links = len(loopable_genome.links)
    innovation = loopable_genome.add_loop(tries=1)
    loop_gene = innovation.gene

    assert len(loopable_genome.links) == original_number_of_links + 1, "one link gene has been added"
    assert loop_gene.from_node.recurrent is True, "the node has been marked as recurrent"
    assert loop_gene.recurrent is True, "the link has been marked as recurrent"
    assert loop_gene.from_node == loop_gene.to_node, "link is a loop"


def test_impossible_loop(unconnectable_genome):
    original_number_of_links = len(unconnectable_genome.links)
    result = unconnectable_genome.add_loop(tries=10)
    new_number_of_links = len(unconnectable_genome.links)
    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"


def test_add_non_loop_link(connectable_genome):
    original_number_of_links = len(connectable_genome.links)
    tries = 50  # Ensure that it won't fail due to picking the same node.
    innovation = connectable_genome.add_non_loop_link(tries)
    new_gene = innovation.gene
    new_number_of_links = len(connectable_genome.links)

    assert new_gene, "new gene is not None"
    assert new_number_of_links == original_number_of_links + 1, "one new link added"
    assert new_gene.from_node != new_gene.to_node, "from and to nodes are not the same"


def test_impossible_add_non_loop_link(unconnectable_genome):
    original_number_of_links = len(unconnectable_genome.links)
    result = unconnectable_genome.add_non_loop_link(tries=10)
    new_number_of_links = len(unconnectable_genome.links)

    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"


def test_add_node():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    original_number_of_nodes = len(genome.nodes)
    original_number_of_links = len(genome.links)
    innovations = genome.mutate_add_node(tries=1)
    new_node = innovations[0].gene
    new_in = innovations[1].gene
    new_out = innovations[2].gene

    assert len(genome.nodes) == original_number_of_nodes + 1, "one node added"
    assert len(genome.links) == original_number_of_links + 2, "two links added"
    assert False in [x.enabled for x in genome.links], "one link disabled"
    assert new_in.to_node == new_node, "new link into new node"
    assert new_out.from_node == new_node, "new link out of new node"
    assert new_in.weight == 1, "weight of new in link is 1"
    assert new_node.depth == 0.5, "depth of new single hidden node is 0.5"


def test_add_recurrent_link():
    # Create minimal genome which can have a recurrent link
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    node_innovations = genome.mutate_add_node(tries=1)
    genome.nodes[1].node_type = NodeType.BIAS  # Disable forward links
    link_innovation = genome.add_non_loop_link(tries=50)
    new_link = link_innovation.gene

    assert len(genome.links) == 4, "link added to genome"
    assert new_link.from_node == genome.nodes[1], "link goes from output"
    assert new_link.to_node == node_innovations[0].gene, "link goes to hidden"
    assert new_link.recurrent, "link is recurrent"


def test_connecting_two_output_nodes():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.mutate_add_node(tries=1)
    for node in genome.nodes:
        node.node_type = NodeType.OUTPUT
    link = genome.add_non_loop_link(tries=10)

    assert link is None, "no link is returned"
    assert len(genome.links) == 3, "no link was added to the genome"
