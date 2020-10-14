from neat.genome import Genome
from neat.innovation_tracker import InnovationTracker
from neat.enums.node_types import NodeType
from unittest.mock import Mock


def test_initialisation(standard_config):
    tracker = InnovationTracker(standard_config)
    assert tracker.node_innovations == {}
    assert tracker.link_innovations == {}
    assert tracker.next_link_id == 1
    assert tracker.next_node_id == 2


def test_single_node_innovation(genome, standard_config):
    tracker = InnovationTracker(standard_config)
    genome.mutate_add_node(tracker=tracker)

    assert len(tracker.node_innovations) == 1, "one node innovation"
    assert len(tracker.link_innovations) == 2, "two link innovations"
    assert genome.nodes[2].id == tracker.next_node_id - 1, "correct node id assigned"
    assert genome.links[1].id == tracker.next_link_id - 2, "correct id assigned to in link"
    assert genome.links[2].id == tracker.next_link_id - 1, "correct id assigned to out link"

    node_key = (genome.nodes[0].id, genome.nodes[1].id, type(genome.nodes[0]))
    assert tracker.node_innovations[node_key] == tracker.next_node_id - 1, "correct node id stored"

    in_key = (genome.nodes[0].id, genome.nodes[2].id, type(genome.links[0]))
    assert tracker.link_innovations[in_key] == tracker.next_link_id - 2, "correct in link id stored"

    out_key = (genome.nodes[2].id, genome.nodes[1].id, type(genome.links[0]))
    assert tracker.link_innovations[out_key] == tracker.next_link_id - 1, "correct out link id stored"


def test_multiple_node_innovations(genome, standard_config):
    tracker = InnovationTracker(standard_config)
    genome.mutate_add_node(tracker=tracker)
    genome.mutate_add_node(tracker=tracker)

    assert len(tracker.node_innovations) == 2, "two node innovations added"
    assert len(tracker.link_innovations) == 4, "four link innovations added"


def test_single_link_innovation(connectable_genome, standard_config):
    tracker = InnovationTracker(standard_config)
    connectable_genome.add_non_loop_link(tracker=tracker)
    assert len(tracker.link_innovations) == 1


def test_existing_node_innovation(standard_config):
    tracker = InnovationTracker(standard_config)
    genome_1 = Genome(1, standard_config)
    genome_2 = Genome(2, standard_config)

    genome_1.mutate_add_node(tracker=tracker)
    genome_2.mutate_add_node(tracker=tracker)

    assert len(genome_1.nodes) == len(genome_2.nodes)
    assert genome_1.nodes[-1].id == genome_2.nodes[-1].id, "node received existing innovation id"
    assert genome_1.links[-2].id == genome_2.links[-2].id, "in link received existing innovation id"
    assert genome_1.links[-1].id == genome_2.links[-1].id, "out link received existing innovation id"


def test_existing_non_consecutive_node_innovation(standard_config):
    tracker = InnovationTracker(standard_config)
    genome_1 = Genome(1, standard_config)
    genome_2 = Genome(2, standard_config)

    genome_1.mutate_add_node(tracker=tracker)
    genome_1.mutate_add_node(tracker=tracker)
    genome_2.mutate_add_node(tracker=tracker)

    assert genome_1.nodes[-2].id == genome_2.nodes[-1].id, "node received existing innovation id"
    assert genome_1.links[-4].id == genome_2.links[-2].id, "in link received existing innovation id"
    assert genome_1.links[-3].id == genome_2.links[-1].id, "out link received existing innovation id"


def test_existing_link_innovation(standard_config):
    genome_1 = Genome(id=1, config=standard_config)
    genome_1.links = []

    genome_2 = Genome(id=1, config=standard_config)
    genome_2.links = []

    tracker = InnovationTracker(config=standard_config)
    genome_1.add_non_loop_link(tracker=tracker)
    genome_2.add_non_loop_link(tracker=tracker)

    assert genome_1.links[-1].id == genome_2.links[-1].id
