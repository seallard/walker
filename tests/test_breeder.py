from neat.genome import Genome
from neat.breeder import Breeder
from neat.link_gene import LinkGene
from unittest.mock import Mock
from neat.enums.node_types import NodeType


def test_smaller_genome_more_fit(standard_config, tracker):
    breeder = Breeder(standard_config)
    mother = Genome(1, standard_config, tracker=tracker)
    father = Genome(2, standard_config, tracker=tracker)

    better, worse = breeder.fitness_order(mother, father)

    assert better == father
    assert worse == mother


def test_higher_score_more_fit(standard_config, tracker):
    breeder = Breeder(standard_config)
    mother = Genome(1, standard_config, tracker=tracker)
    father = Genome(2, standard_config, tracker=tracker)

    mother.original_fitness = 100

    better, worse = breeder.fitness_order(mother, father)

    assert better == mother
    assert worse == father


def test_crossover_identical(standard_config, tracker):
    breeder = Breeder(standard_config)
    mother = Genome(1, standard_config, tracker=tracker)
    father = Genome(2, standard_config, tracker=tracker)

    offspring = breeder.crossover(mother, father, False)

    assert len(offspring.nodes) == len(mother.nodes)
    assert len(offspring.links) == len(father.links)
    assert len([node for node in mother.nodes if node in offspring.nodes]) == 0
    assert len([node for node in father.nodes if node in offspring.nodes]) == 0


def test_crossover_longer_less_fit(standard_config, tracker):
    breeder = Breeder(standard_config)
    mother = Genome(id=1, config=standard_config, tracker=tracker)
    father = Genome(id=2, config=standard_config, tracker=tracker)

    mother.mutate_add_node()
    mother.mutate_add_node()

    offspring = breeder.crossover(mother, father, False)
    father.original_fitness = 100

    assert len(offspring.nodes) == len(father.nodes)
    assert len(offspring.links) == len(father.links)
    assert None not in offspring.nodes
    assert None not in offspring.links


def test_create_genome_parent_unchanged(genome, standard_config):
    breeder = Breeder(standard_config)

    old_link_weights = [x.weight for x in genome.links]
    new_genome = breeder.create_genome(genome.links, None)

    assert old_link_weights == [x.weight for x in genome.links]
    assert old_link_weights == [x.weight for x in new_genome.links]


def test_crossover_averaging_unchanged(standard_config, tracker):
    breeder = Breeder(standard_config)

    mother = Genome(id=1, config=standard_config, tracker=tracker)
    mother_original_weights = [x.weight for x in mother.links]

    father = Genome(id=2, config=standard_config, tracker=tracker)
    father_original_weigjts = [x.weight for x in father.links]

    breeder.crossover(mother, father, averaging=True)

    assert mother_original_weights == [x.weight for x in mother.links], "weights of mother not mutated"
    assert father_original_weigjts == [x.weight for x in father.links], "weights of father not mutated"
