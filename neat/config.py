import json


class Config():

    def __init__(self, file):

        with open(file, 'r') as f:
            config = json.load(f)

        self.population_size = config['population_size']

        self.weight_mutation_range = config['weight_mutation_range']
        self.weight_mutation_rate = config['weight_mutation_rate']
        self.weight_replacement_rate = config['weight_replacement_rate']

        self.node_add_rate = config['add_node_probability']
        self.link_add_rate = config['add_link_probability']

        self.node_add_tries = config['node_addition_attempts']
        self.link_add_tries = config['link_addition_attempts']
        self.loop_add_tries = config['link_loop_attempts']

        self.loop_rate = config['loop_rate']

        self.recurrent_rate = config['link_recurrent_probability']
        self.reactivation_rate = config['link_reactivation_probability']

        self.mutate_only = config['mutate_only_probability']
        self.mate_only = config['mate_only_probability']
        self.interspecies_mating_rate = config['interspecies_mating_rate']
        self.mate_by_choosing = config['mate_by_choosing_probability']
        self.mate_by_averaging = config['mate_by_averaging_probability']

        self.compatibility_threshold = config['compatibility_threshold']
        self.c_excess = config['excess_coefficient']
        self.c_disjoint = config['disjoint_coefficient']
        self.c_weight = config['weight_coefficient']
        self.survival_threshold = config['survival_threshold']
        self.maximum_stagnation = config['maximum_stagnation']
        self.species_target_number = config['target_number_of_species']

        self.environment = config['environment']
        self.num_inputs = config['input_dimension']
        self.num_outputs = config['output_dimension']

        self.young_threshold = config['young_threshold']
        self.young_boost = config['young_boost']
        self.old_threshold = config['old_threshold']
        self.old_penalty = config['old_penalty']