from neat.genome import Genome
from neat.innovation_tracker import InnovationTracker
from neat.enums.node_types import NodeType
from unittest.mock import Mock


def test_initialisation(standard_config):
    tracker = InnovationTracker(standard_config)
    assert tracker.node_innovations == {}
    assert tracker.link_innovations == {}
    assert tracker.next_link_id == 1
    assert tracker.next_node_id == 3


def test_single_node_innovation(genome):
    tracker = genome.tracker
    genome.mutate_add_node()

    assert len(tracker.node_innovations) == 1, "one node innovation"
    assert len(tracker.link_innovations) == 2, "two link innovations"

    assert genome.nodes[-1].id == tracker.next_node_id - 1, "correct node id assigned"
    assert genome.links[-2].id == tracker.next_link_id - 2, "correct id assigned to in link"
    assert genome.links[-1].id == tracker.next_link_id - 1, "correct id assigned to out link"


def test_multiple_node_innovations(genome):
    tracker = genome.tracker
    genome.mutate_add_node()
    genome.mutate_add_node()

    assert len(tracker.node_innovations) == 2, "two node innovations added"
    assert len(tracker.link_innovations) == 4, "four link innovations added"


def test_single_link_innovation(connectable_genome):
    connectable_genome.add_forward_link()
    assert len(connectable_genome.tracker.link_innovations) == 1


def test_existing_node_innovation(standard_config):
    tracker = InnovationTracker(standard_config)
    genome_1 = Genome(id=1, config=standard_config, tracker=tracker)
    genome_2 = Genome(id=2, config=standard_config, tracker=tracker)

    genome_1.mutate_add_node()
    genome_2.mutate_add_node()

    assert len(genome_1.nodes) == len(genome_2.nodes)
    assert genome_1.nodes[-1].id == genome_2.nodes[-1].id, "node received existing innovation id"
    assert genome_1.links[-2].id == genome_2.links[-2].id, "in link received existing innovation id"
    assert genome_1.links[-1].id == genome_2.links[-1].id, "out link received existing innovation id"


def test_existing_non_consecutive_node_innovation(standard_config):
    tracker = InnovationTracker(standard_config)
    genome_1 = Genome(1, standard_config, tracker=tracker)
    genome_2 = Genome(2, standard_config, tracker=tracker)

    genome_1.mutate_add_node()
    genome_1.mutate_add_node()
    genome_2.mutate_add_node()

    assert genome_1.nodes[-2].id == genome_2.nodes[-1].id, "node received existing innovation id"
    assert genome_1.links[-4].id == genome_2.links[-2].id, "in link received existing innovation id"
    assert genome_1.links[-3].id == genome_2.links[-1].id, "out link received existing innovation id"
