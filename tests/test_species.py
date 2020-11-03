from neat.species import Species
from neat.genome import Genome
from unittest.mock import Mock


def test_add_identical_genome(standard_config, tracker):
    genome_1 = Genome(id=1, config=standard_config, tracker=tracker)
    genome_2 = Genome(id=2, config=standard_config, tracker=tracker)
    species = Species(id=1, first_genome=genome_1, config=standard_config, breeder=Mock())
    species.add_genome(genome_2)

    assert len(species.genomes) == 2


def test_add_worse_genome(standard_config, tracker):
    better = Genome(id=1, config=standard_config, tracker=tracker)
    better.original_fitness = 10
    worse = Genome(id=2, config=standard_config, tracker=tracker)
    worse.original_fitness = 0

    species = Species(id=1, first_genome=better, config=standard_config, breeder=Mock())
    species.add_genome(worse)

    assert species.leader == better
    assert species.genomes[0] == better
    assert species.genomes[1] == worse

def test_add_better_genome(standard_config, tracker):
    better = Genome(id=1, config=standard_config, tracker=tracker)
    worse = Genome(id=2, config=standard_config, tracker=tracker)
    better.original_fitness = 10
    species = Species(id=1, first_genome=worse, config=standard_config, breeder=Mock())
    species.add_genome(better)

    assert species.leader == better
