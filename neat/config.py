import json


class Config():

    def __init__(self, file):

        with open(file, 'r') as f:
            config = json.load(f)

        self.population_size = config['population_size']

        self.weight_mutation_range = config['weight_mutation_range']

        self.node_add_rate = config['add_node_probability']
        self.link_add_rate = config['add_link_probability']

        self.node_add_tries = config['node_addition_attempts']
        self.link_add_tries = config['link_addition_attempts']
        self.loop_back_tries = config['link_loop_attempts']

        self.recurrent_rate = config['link_recurrent_probability']
        self.reactivation_rate = config['link_reactivation_probability']

        self.mutate_only = config['mutate_only_probability']
        self.mate_only = config['mate_only_probability']
        self.interspecies_mating_rate = config['interspecies_mating_rate']
        self.mate_by_choosing = config['mate_by_choosing_probability']
        self.mate_by_averaging = config['mate_by_averaging_probability']

        self.compatibility_threshold = config['compatibility_threshold']
        self.excess_c = config['excess_coefficient']
        self.disjoint_c = config['disjoint_coefficient']
        self.weight_c = config['weight_coefficient']
        self.survival_threshold = config['survival_threshold']
        self.maximum_stagnation = config['maximum_stagnation']
        self.species_target_number = config['target_number_of_species']
