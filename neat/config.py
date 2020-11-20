import json


class Config():

    def __init__(self, file):

        with open(file, 'r') as f:
            config = json.load(f)

        # Number of genomes in the population.
        self.population_size = config['population_settings']['size']


        #### SPECIES SETTINGS ####
        species_settings = config['species_settings']

        # Maximum number of generations a species is allowed to stay at the same max fitness before it is removed.
        self.maximum_stagnation = species_settings['maximum_stagnation']

        # Coefficients representing how important the gene differences are in measuring compatibility.
        self.c_excess = species_settings['excess_coefficient']
        self.c_disjoint = species_settings['disjoint_coefficient']
        self.c_weight = species_settings['weight_coefficient']
        self.compatibility_threshold = species_settings['compatibility_threshold']

        # Fitness adjustment parameters
        self.young_threshold = species_settings['young_threshold']
        self.old_threshold = species_settings['old_threshold']
        self.young_boost = species_settings['young_boost']
        self.old_penalty = species_settings['old_penalty']

        #### REPRODUCTION SETTINGS ####
        reproduction_settings = config['reproduction_settings']

        # Percentage of each species allowed to reproduce.
        self.survival_threshold = reproduction_settings['survival_threshold']

        # Probability an offspring will be created only through crossover without mutation.
        self.mate_only_probability = reproduction_settings['mate_only_probability']

        # Probability an offspring will be created only through mutation without crossover.
        self.mutate_only_probability = reproduction_settings['mutate_only_probability']

        # Percentage of crossovers allowed to occur between parents of different species.
        self.interspecies_mating_rate = reproduction_settings['interspecies_mating_rate']

        # Probability that matching genes will be averaged during crossover (otherwise randomly chosen).
        self.mate_by_averaging = reproduction_settings['mate_by_averaging_probability']


        #### MUTATION SETTINGS ####
        mutation_settings = config['mutation_settings']

        # Probability a new connection will be added to the genome.
        self.add_link_probability = mutation_settings['add_link_probability']
        self.link_add_tries = mutation_settings['link_addition_attempts']

        # Probability a new node gene will be added to the genome
        self.add_node_probability = mutation_settings['add_node_probability']
        self.node_add_tries = mutation_settings['node_addition_attempts']

        # The maximum magnitude of a mutation that changes the weight of a connection.
        self.weight_mutation_power = mutation_settings['weight_mutation_power']
        self.weight_mutation_probability = mutation_settings['weight_mutation_probability']
        self.weight_replacement_rate = mutation_settings['weight_replacement_rate']

        # Probability a new connection will be recurrent.
        self.link_recurrent_probability = mutation_settings['link_recurrent_probability']
        self.reenable_link_probability = mutation_settings['link_reenable_probability']
        self.toggle_probability = mutation_settings['link_toggle_enable_probability']

        #### ENVIRONMENT SETTINGS ####
        environment_settings = config['environment_settings']
        self.environment = environment_settings['environment']
        self.num_inputs = environment_settings['input_dimension']
        self.num_outputs = environment_settings['output_dimension']
        self.fitness_threshold = 1.0
