from neat.population import Population
from neat.genome import Genome


def test_compat_identical():
    population = Population(size=10,c_disjoint=1, c_excess=1, c_weight=1)
    genome_1 = Genome(id=1, num_inputs=1, num_outputs=1)
    genome_2 = Genome(id=2, num_inputs=1, num_outputs=1)
    genome_1.links[0].weight = genome_2.links[0].weight
    compatibility = population.compatibility(genome_1, genome_2)
    assert compatibility == 0


def test_compat_extra_link():
    population = Population(size=10,c_disjoint=1, c_excess=1, c_weight=0)
    genome_1 = Genome(id=1, num_inputs=2, num_outputs=1)
    genome_2 = Genome(id=2, num_inputs=1, num_outputs=1)

    compatibility = population.compatibility(genome_1, genome_2)
    assert compatibility == 0.5

    compatibility = population.compatibility(genome_2, genome_1)
    assert compatibility == 0.5
