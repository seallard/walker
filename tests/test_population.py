from neat.population import Population
from neat.genome import Genome
from unittest.mock import Mock


def test_initialisation():
    population = Population(size=10, num_inputs=1, num_outputs=1, c_disjoint=1, c_excess=1, c_weight=1)
    assert len(population.genomes) == 10


def test_compat_identical():
    population = Population(size=10, num_inputs=1, num_outputs=1, c_disjoint=1, c_excess=1, c_weight=0)
    genome_1 = Genome(id=10, num_inputs=1, num_outputs=1)
    genome_2 = Genome(id=11, num_inputs=1, num_outputs=1)
    compatibility = population.compatibility(genome_1, genome_2)
    assert compatibility == 0


def test_compat_extra_link():
    population = Population(size=10, num_inputs=1, num_outputs=1, c_disjoint=1, c_excess=1, c_weight=0)
    genome_1 = Genome(id=10, num_inputs=2, num_outputs=1)
    genome_2 = Genome(id=11, num_inputs=1, num_outputs=1)

    compatibility = population.compatibility(genome_1, genome_2)
    assert compatibility == 0.5

    compatibility = population.compatibility(genome_2, genome_1)
    assert compatibility == 0.5


def test_speciate_single_genome():
    population = Population(size=1, num_inputs=1, num_outputs=1, c_disjoint=1, c_excess=1, c_weight=0)
    population.speciate_genomes()

    assert len(population.species) == 1, "genome placed into species"


def test_speciate_identical_genomes():
    population = Population(size=3, num_inputs=1, num_outputs=1, c_disjoint=1, c_excess=1, c_weight=0)
    population.speciate_genomes()

    assert len(population.genomes) == 3, "three genomes added"
    assert len(population.species) == 1, "one species created"
    assert len(population.species[0].members) == 3, "all genomes added to the same species"


def test_speciate_distinct_genomes():
    population = Population(size=0, num_inputs=1, num_outputs=1, c_disjoint=10, c_excess=10, c_weight=10)
    genome_1 = Genome(id=0, num_inputs=1, num_outputs=1)
    genome_2 = Genome(id=1, num_inputs=1, num_outputs=1)

    genome_1.mutate_add_node(tries=1, tracker=Mock())
    genome_1.nodes[-1].id = 2 # Mock tracker did not assign a valid id.
    population.genomes = [genome_1, genome_2]

    population.speciate_genomes()

    assert len(population.species) == 2, "two species created"
    assert len(population.species[0].members) == 1, "first species contains one genome"
    assert len(population.species[1].members) == 1, "second species contains one genome"
