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
def loopable_genome():
    pass

@pytest.fixture
def unloopable_genome():
    pass

@pytest.fixture
def connectable_genome():
    pass


def test_node_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"
    assert [x.id for x in genome.nodes] == [x for x in range(inputs + outputs)], "correct node innovation ids"
    assert [x.node_type for x in genome.nodes[:inputs]] == [NodeType.INPUT for x in range(inputs)], "correct type for inputs"
    assert [x.node_type for x in genome.nodes[inputs:]] == [NodeType.OUTPUT for x in range(outputs)], "correct type for outputs"


def test_link_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.links) == inputs * outputs, "correct number of links"

    ids = [x.innovation_id for x in genome.links]
    expected_ids = [x for x in range(inputs + outputs, inputs * outputs + inputs + outputs)]
    assert ids == expected_ids, "correct link innovation ids"

    assert True not in [x.recurrent for x in genome.links], "no initial link is recurrent"
    assert False not in [x.enabled for x in genome.links], "all initial links are enabled"