from neat.genome import Genome
from neat.enums.node_types import NodeType
from unittest.mock import Mock


def test_link_initialisation(genome):
    inputs = genome.config.num_inputs
    outputs = genome.config.num_outputs
    assert len(genome.links) == inputs * outputs, "correct number of links"

    ids = [x.id for x in genome.links]
    expected_ids = [x for x in range(0, inputs * outputs)]
    assert ids == expected_ids, "correct link innovation ids"

    assert True not in [x.recurrent for x in genome.links], "no initial link is recurrent"
    assert False not in [x.enabled for x in genome.links], "all initial links are enabled"

    assert genome.nodes[0].depth == 0, "depth of input node is 0"
    assert genome.nodes[-1].depth == 1, "depth of output node is 1"


def test_possible_loop(loopable_genome):
    original_number_of_links = len(loopable_genome.links)
    loopable_genome.add_loop(tracker=Mock())
    loop_gene = loopable_genome.links[-1]

    assert len(loopable_genome.links) == original_number_of_links + 1, "one link gene has been added"
    assert loop_gene.from_node.recurrent is True, "the node has been marked as recurrent"
    assert loop_gene.recurrent is True, "the link has been marked as recurrent"
    assert loop_gene.from_node == loop_gene.to_node, "link is a loop"


def test_impossible_loop(unloopable_genome):
    original_number_of_links = len(unloopable_genome.links)
    result = unloopable_genome.add_loop(tracker=Mock())
    new_number_of_links = len(unloopable_genome.links)
    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"


def test_add_non_loop_link(connectable_genome):
    original_number_of_links = len(connectable_genome.links)
    connectable_genome.add_non_loop_link(tracker=Mock())
    link = connectable_genome.links[-1]

    assert len(connectable_genome.links) == original_number_of_links + 1, "one new link added"
    assert link.from_node != link.to_node, "new link is not a loop"


def test_impossible_add_non_loop_link(unloopable_genome):
    original_number_of_links = len(unloopable_genome.links)
    result = unloopable_genome.add_non_loop_link(tracker=Mock())
    new_number_of_links = len(unloopable_genome.links)

    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"


def test_add_recurrent_link(make_recurrent_genome, standard_config):
    make_recurrent_genome.add_non_loop_link(tracker=Mock())
    new_link = make_recurrent_genome.links[-1]

    assert new_link.from_node == make_recurrent_genome.nodes[1], "link goes from output"
    assert new_link.to_node == make_recurrent_genome.nodes[-1], "link goes to input"
    assert new_link.recurrent, "link is recurrent"


def test_connecting_two_output_nodes(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.mutate_add_node(tracker=Mock())
    for node in genome.nodes:
        node.type = NodeType.OUTPUT
    genome.add_non_loop_link(tracker=Mock())

    assert len(genome.links) == 3, "no link was added to the genome"


def test_perturbing_single_link(standard_config):
    genome = Genome(id=1, config=standard_config)
    initial_weight = genome.links[0].weight
    genome.mutate_weights()
    new_weight = genome.links[0].weight

    assert new_weight != initial_weight, "weight perturbed"
    assert new_weight >= initial_weight - 0.5, "weight is not below min allowed"
    assert new_weight <= initial_weight + 0.5, "weight is not above max allowed"


def test_perturbing_multiple_links(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.mutate_add_node(tracker=Mock())

    initial_weights = [link.weight for link in genome.links]
    genome.mutate_weights()
    perturbed_weigths = [link.weight for link in genome.links]

    assert initial_weights[0] != perturbed_weigths[0]
    assert initial_weights[1] != perturbed_weigths[1]

    for i, weight in enumerate(perturbed_weigths):
        assert weight <= initial_weights[i] + 0.5
        assert weight >= initial_weights[i] - 0.5


def test_replacing_link(genome):
    genome.config.weight_mutation_rate = 1
    genome.config.weight_replacement_rate = 1
    genome.config.weight_mutation_range =  0

    initial_weight = genome.links[0].weight
    genome.mutate_weights()
    new_weight = genome.links[0].weight

    assert new_weight != initial_weight, "weight perturbed"
    assert new_weight >= -1
    assert new_weight <= 1
