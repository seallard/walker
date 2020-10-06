

class Species:

    def __init__(self, id, first_genome):
        self.id = id
        self.leader = first_genome
        self.members = [first_genome]
        self.max_fitness = first_genome.fitness
        self.age_since_improvement = 0
        self.age = 0
        self.expected_offspring = 0


    def adjust_fitness(self, young_bonus, old_penalty, young_threshold, old_threshold):

        for genome in self.members:

            fitness = genome.fitness

            if self.age < young_threshold:
                fitness *= young_bonus
            
            if self.age > old_threshold:
                fitness *= old_penalty

            genome.adjusted_fitness = fitness/len(self.members)

    def add_member(self, genome):
        self.members.append(genome)
        
        if genome.fitness > self.leader.fitness:
            self.leader = genome
            self.max_fitness = genome.fitness
            self.age_since_improvement = 0

    def epoch_reset(self):
        self.members = []
        self.age += 1
        self.age_since_improvement += 1
        self.expected_offspring = 0

    def average_adjusted_fitness(self):
        total_fitness = 0
        for genome in self.members:
            total_fitness += genome.adjusted_fitness

        return total_fitness/len(self.members)

    def should_go_extinct(self, no_improvement_threshold):
        return self.age_since_improvement > no_improvement_threshold
