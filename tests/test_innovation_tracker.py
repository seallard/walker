from neat.genome import Genome
from neat.innovation_tracker import InnovationTracker


def test_initialisation():
    tracker = InnovationTracker(num_inputs=1, num_outputs=1)
    assert tracker.innovations == {}
    assert tracker.next_innovation_number == 3


def test_single_node_innovation():
    genome = Genome(1, num_inputs=1, num_outputs=1)
    tracker = InnovationTracker(num_inputs=1, num_outputs=1)

    innovations = genome.mutate_add_node(tries=1)

    for innovation in innovations:
        tracker.assign_innovation_number(innovation)

    assert len(tracker.innovations) == 3, "three innovations added"
    assert innovations[0].gene.innovation_number == 3, "correct number assigned to node gene"
    assert innovations[1].gene.innovation_number == 4, "correct number assigned to in link gene"
    assert innovations[2].gene.innovation_number == 5, "correct number assigned to out link gene"
    assert tracker.innovations[innovations[0].get_key()] == 3, "correct number stored for node innovation"
    assert tracker.innovations[innovations[1].get_key()] == 4, "correct number stored for in link innovation"
    assert tracker.innovations[innovations[2].get_key()] == 5, "correct number stored for out link innovation"


def test_multiple_node_innovations():
    pass


def test_single_link_innovation():
    pass


def test_multiple_link_innovations():
    pass

def test_reset():
    pass