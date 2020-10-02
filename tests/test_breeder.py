from neat.genome import Genome
from neat.breeder import Breeder
from unittest.mock import Mock

def test_smaller_genome_more_fit():
    breeder = Breeder()
    mother = Genome(1, 10, 10)
    father = Genome(2, 5, 5)

    better, worse = breeder.fitness_order(mother, father)

    assert better == father
    assert worse == mother

def test_higher_score_more_fit():
    breeder = Breeder()
    mother = Genome(1, 10, 10)
    father = Genome(2, 5, 5)

    mother.fitness = 100 

    better, worse = breeder.fitness_order(mother, father)

    assert better == mother
    assert worse == father

def test_crossover_identical():
    breeder = Breeder()
    mother = Genome(1, 1, 1)
    father = Genome(2, 1, 1)

    offspring = breeder.crossover(mother, father)

    assert len(offspring.nodes) == len(mother.nodes)
    assert len(offspring.links) == len(father.links)
    assert len([node for node in mother.nodes if node in offspring.nodes]) == 0
    assert len([node for node in father.nodes if node in offspring.nodes]) == 0

def test_crossover_longer_less_fit():
    breeder = Breeder()
    mother = Genome(1, 1, 1)
    father = Genome(2, 1, 1)

    mother.mutate_add_node(tries=50, tracker=Mock())
    mother.mutate_add_node(tries=50, tracker=Mock())

    offspring = breeder.crossover(mother, father)
    father.fitness = 100

    assert len(offspring.nodes) == len(father.nodes)
    assert len(offspring.links) == len(father.links)
    assert None not in offspring.nodes
    assert None not in offspring.links

def test_crossover_looped():
    pass