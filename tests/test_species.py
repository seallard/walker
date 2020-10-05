from neat.species import Species
from neat.genome import Genome


def test_single_young_adjustment():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.fitness = 10
    species = Species(id=1, first_genome=genome)
    species.adjust_fitness(young_bonus=1.05, old_penalty=0.95, young_threshold=10, old_threshold=20)

    assert genome.adjusted_fitness == genome.fitness*1.05


def test_single_middle_age_adjustment():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.fitness = 10
    species = Species(id=1, first_genome=genome)
    species.age = 10
    species.adjust_fitness(young_bonus=1.05, old_penalty=0.95, young_threshold=10, old_threshold=20)

    assert genome.adjusted_fitness == genome.fitness


def test_single_old_adjustment():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    genome.fitness = 10
    species = Species(id=1, first_genome=genome)
    species.age = 21
    species.adjust_fitness(young_bonus=1.05, old_penalty=0.95, young_threshold=10, old_threshold=20)

    assert genome.adjusted_fitness == genome.fitness * 0.95


def test_add_identical_member():
    genome_1 = Genome(id=1, num_inputs=1, num_outputs=1)
    genome_2 = Genome(id=2, num_inputs=1, num_outputs=1)
    species = Species(id=1, first_genome=genome_1)
    species.add_member(genome_2)

    assert len(species.members) == 2


def test_add_worse_member():
    better = Genome(id=1, num_inputs=1, num_outputs=1)
    worse = Genome(id=2, num_inputs=1, num_outputs=1)
    better.fitness = 10
    species = Species(id=1, first_genome=better)
    species.add_member(worse)

    assert species.leader == better
    assert species.max_fitness == better.fitness

def test_add_better_member():
    better = Genome(id=1, num_inputs=1, num_outputs=1)
    worse = Genome(id=2, num_inputs=1, num_outputs=1)
    better.fitness = 10
    species = Species(id=1, first_genome=worse)
    species.add_member(better)

    assert species.leader == better
    assert species.max_fitness == better.fitness
