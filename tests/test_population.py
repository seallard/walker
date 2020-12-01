from neat.population import Population
from neat.genome import Genome


def test_initialisation(standard_config):
    population = Population(standard_config)
    assert len(population.genomes) == 10


def test_speciate_single_genome(standard_config):
    population = Population(standard_config)
    population.speciate_genomes()

    assert len(population.species) == 1, "genome placed into species"


def test_speciate_identical_genomes(standard_config):
    population = Population(standard_config)
    population.speciate_genomes()

    assert len(population.species) == 1, "one species created"
    assert len(population.species[0].genomes) == standard_config.population_size, "all genomes added to the same species"


def test_speciate_distinct_genomes(standard_config):
    standard_config.compatibility_threshold = 0.1 # Make sure any difference in topology creates a new species.
    standard_config.c_weight = 0 # Ignore differences in weights.
    population = Population(standard_config)
    population.genomes[0].mutate_add_node()

    population.speciate_genomes()

    assert len(population.species) == 2, "two species created"
    assert len(population.species[0].genomes) == 1, "first species contains one genome"
    assert len(population.species[1].genomes) == standard_config.population_size-1, "second species contains all but one genome"