from neat.genome import Genome
from neat.breeder import Breeder


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
