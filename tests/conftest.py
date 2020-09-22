from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest

@pytest.fixture()
def genome():
    return Genome(id=1, num_inputs=10, num_outputs=10)

@pytest.fixture
def loopable_genome(genome):
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome


@pytest.fixture
def unloopable_genome(genome):
    for node in genome.nodes:
        node.node_type = NodeType.BIAS
    return genome


@pytest.fixture
def connectable_genome(genome):
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome
