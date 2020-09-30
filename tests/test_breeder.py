from neat.genome import Genome
from neat.breeder import Breeder


def test_ordering_equal_fitness():
    breeder = Breeder()
    mother = Genome(1, 10, 10)
    father = Genome(2, 5, 5)

    better, worse = breeder.fitness_order(mother, father)

    assert better == father
    assert worse == mother

