from neat.species import Species
from neat.genome import Genome
from unittest.mock import Mock


def test_single_young_adjustment(genome, standard_config):
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config, breeder=Mock())
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness*standard_config.young_boost


def test_single_middle_age_adjustment(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config, breeder=Mock())
    species.age = 10
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness


def test_single_old_adjustment(genome, standard_config):
    genome.fitness = 10
    species = Species(id=1, first_genome=genome, config=standard_config, breeder=Mock())
    species.age = standard_config.old_threshold + 1
    species.adjust_fitness()

    assert genome.adjusted_fitness == genome.fitness * standard_config.old_penalty


def test_add_identical_genome(standard_config):
    genome_1 = Genome(id=1, config=standard_config)
    genome_2 = Genome(id=2, config=standard_config)
    species = Species(id=1, first_genome=genome_1, config=standard_config, breeder=Mock())
    species.add_genome(genome_2)

    assert len(species.genomes) == 2


def test_add_worse_genome(standard_config):
    better = Genome(id=1, config=standard_config)
    better.fitness = 10
    worse = Genome(id=2, config=standard_config)
    worse.fitness = 0

    species = Species(id=1, first_genome=better, config=standard_config, breeder=Mock())
    species.add_genome(worse)

    assert species.leader == better
    assert species.genomes[0] == better
    assert species.genomes[1] == worse

def test_add_better_genome(standard_config):
    better = Genome(id=1, config=standard_config)
    worse = Genome(id=2, config=standard_config)
    better.fitness = 10
    species = Species(id=1, first_genome=worse, config=standard_config, breeder=Mock())
    species.add_genome(better)

    assert species.leader == better
