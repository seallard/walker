from neat.species import Species
from neat.genome import Genome


def test_single_young_adjustment(genome, standard_config):
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config)
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness*standard_config.young_boost


def test_single_middle_age_adjustment(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config)
    species.age = 10
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness


def test_single_old_adjustment(genome, standard_config):
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config)
    species.age = standard_config.old_threshold + 1
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness * standard_config.old_penalty


def test_add_identical_member(standard_config):
    genome_1 = Genome(id=1, config=standard_config)
    genome_2 = Genome(id=2, config=standard_config)
    species = Species(id=1, first_genome=genome_1, config=standard_config)
    species.add_member(genome_2)

    assert len(species.members) == 2


def test_add_worse_member(standard_config):
    better = Genome(id=1, config=standard_config)
    worse = Genome(id=2, config=standard_config)
    better.fitness = 10
    species = Species(id=1, first_genome=better, config=standard_config)
    species.add_member(worse)

    assert species.leader == better
    assert species.max_fitness == better.fitness

def test_add_better_member(standard_config):
    better = Genome(id=1, config=standard_config)
    worse = Genome(id=2, config=standard_config)
    better.fitness = 10
    species = Species(id=1, first_genome=worse, config=standard_config)
    species.add_member(better)

    assert species.leader == better
    assert species.max_fitness == better.fitness
