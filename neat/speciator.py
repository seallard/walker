from neat.genome import Genome


class Speciator:

    def __init__(self, c_disjoint, c_excess, c_weight):
        self.species = []
        self.c_disjoint = c_disjoint
        self.c_excess = c_excess
        self.c_weight = c_weight


    def speciate_genome():
        """Place genome into a species. """
        pass

    def compatibility(self, species, genome):
        """Compatibility of genomes. """

        weight_diff = 0
        matched = 0
        disjoint = 0
        excess = 0

        species_index = 0
        genome_index = 0

        while species_index <= species.size():

            # Reached end of genome.
            if genome_index == genome.size():
                excess += len(species.links) - species_index
                break

            # Reached end of species genome.
            if species_index == species.size():
                excess += len(genome.links) - genome_index
                break

            species_gene = species.links[species_index]
            genome_gene = genome.links[genome_index]

            if genome_gene.id == species_gene.id:
                matched += 1
                weight_diff += abs(genome_gene.weight - species_gene.weight)
                genome_index += 1
                species_index += 1

            elif genome_gene.id > species_gene.id:
                disjoint += 1
                species_index += 1
            
            else:
                disjoint += 1
                genome_index += 1
        
        if species.size() > genome.size():
            n = species.size()

        else:
            n = genome.size()

        disjoint = self.c_disjoint * disjoint/n
        excess = self.c_excess * excess/n
        weight = self.c_weight * weight_diff/matched

        return disjoint + excess + weight
