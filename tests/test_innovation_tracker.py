from neat.genome import Genome
from neat.innovation_tracker import InnovationTracker


def test_initialisation():
    tracker = InnovationTracker(num_inputs=1, num_outputs=1)
    assert tracker.node_innovations == {}
    assert tracker.link_innovations == {}
    assert tracker.next_link_id == 1
    assert tracker.next_node_id == 2


def test_single_node_innovation():
    genome = Genome(1, num_inputs=1, num_outputs=1)
    tracker = InnovationTracker(num_inputs=1, num_outputs=1)
    genome.mutate_add_node(tries=1, tracker=tracker)

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


def test_multiple_node_innovations():
    genome = Genome(1, num_inputs=1, num_outputs=1)
    tracker = InnovationTracker(num_inputs=1, num_outputs=1)
    genome.mutate_add_node(tries=1, tracker=tracker)
    genome.mutate_add_node(tries=50, tracker=tracker)

    assert len(tracker.node_innovations) == 2, "two node innovations added"
    assert len(tracker.link_innovations) == 4, "four link innovations added"


def test_single_link_innovation(connectable_genome):
    tracker = InnovationTracker(connectable_genome.num_inputs, connectable_genome.num_outputs)
    connectable_genome.add_non_loop_link(tries=50, tracker=tracker)

    assert len(tracker.link_innovations) == 1
    assert tracker.next_link_id == connectable_genome.num_inputs*connectable_genome.num_outputs + 1


def test_multiple_link_innovations():
    pass

def test_reset():
    pass