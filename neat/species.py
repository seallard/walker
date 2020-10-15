

class Species:

    def __init__(self, id, first_genome, config):
        self.id = id
        self.leader = first_genome
        self.members = [first_genome]
        self.age_since_improvement = 0
        self.age = 0
        self.expected_offspring = 0
        self.config = config
        self.adjusted_sum = 0

    def adjust_fitness(self):

        for genome in self.members:

            fitness = genome.fitness

            if self.age < self.config.young_boost:
                fitness *= self.config.young_boost

            if self.age > self.config.old_threshold:
                fitness *= self.config.old_penalty

            adjusted = fitness/len(self.members)
            genome.adjusted_fitness = adjusted
            self.adjusted_sum += adjusted

    def add_member(self, genome):
        self.members.append(genome)

        if genome.fitness > self.leader.fitness:
            self.leader = genome
            self.age_since_improvement = 0

    def epoch_reset(self):
        self.members = []
        self.age += 1
        self.age_since_improvement += 1
        self.expected_offspring = 0
        self.adjusted_sum = 0

    def should_go_extinct(self, no_improvement_threshold):
        return self.age_since_improvement > no_improvement_threshold

    def reproduce(self):

        offspring = [self.leader] # Always include the species leader as is.

        for i in range(self.expected_offspring):
            # TODO: crossover
            pass

        return offspring
