#
# The script to run maze navigation experiment for both medium and hard
# maze configurations.
#

# The Python standard library import
import os
import shutil
import math
import random
import time
import copy
import argparse

from neat.config import Config
from neat.population import Population
from neat.statistics import StatisticsReporter

# The helper used to visualize experiment results
from . import visualize
from . import utils

# The maze environment
from . import maze_environment as maze
from . import agent

# The current working directory
local_dir = os.path.dirname(__file__)
# The directory to store outputs
out_dir = os.path.join(local_dir, 'out')
out_dir = os.path.join(out_dir, 'maze_objective')

class MazeSimulationTrial:
    """
    The class to hold maze simulator execution parameters and results.
    """
    def __init__(self, maze_env, population):
        """
        Creates new instance and initialize fileds.
        Arguments:
            maze_env:   The maze environment as loaded from configuration file.
            population: The population for this trial run
        """
        # The initial maze simulation environment
        self.orig_maze_environment = maze_env
        # The record store for evaluated maze solver agents
        self.record_store = agent.AgentRecordStore()
        # The NEAT population object
        self.population = population

# The simulation results holder for a one trial.
# It must be initialized before start of each trial.
trialSim = None

def eval_fitness(genome, time_steps=400):
    """
    Evaluates fitness of the provided genome.
    Arguments:
        genome:     The genome to evaluate.
        time_steps: The number of time steps to execute for maze solver simulation.
    Returns:
        The phenotype fitness score in range (0, 1]
    """
    # run the simulation
    maze_env = copy.deepcopy(trialSim.orig_maze_environment)
    control_net = genome.network()
    fitness = maze.maze_simulation_evaluate(
                                        env=maze_env,
                                        net=control_net,
                                        time_steps=time_steps)
    return fitness

def update_records(genomes):

    for genome in genomes:

        # Store simulation results into the agent record
        record = agent.AgentRecord(
            generation=trialSim.population.generation,
            agent_id=genome.id)

        record.fitness = genome.fitness
        record.x = maze_env.agent.location.x
        record.y = maze_env.agent.location.y
        record.hit_exit = maze_env.exit_found
        species = trialSim.population.get_species(genome.id)
        record.species_id = species.id
        record.species_age = species.age

        # add record to the store
        trialSim.record_store.add_record(record)

def eval_genomes(genomes):
    """
    The function to evaluate the fitness of each genome in
    the genomes list.
    Arguments:
        genomes: The list of genomes from population in the
                 current generation
    """
    for genome in genomes:
        fitness = eval_fitness(genome)
        genome.fitness = fitness
        genome.original_fitness = fitness

def run_experiment(config_file, maze_env, trial_out_dir, args=None, n_generations=100, silent=False):
    """
    The function to run the experiment against hyper-parameters
    defined in the provided configuration file.
    The winner genome will be rendered as a graph as well as the
    important statistics of neuroevolution process execution.
    Arguments:
        config_file:    The path to the file with experiment configuration
        maze_env:       The maze environment to use in simulation.
        trial_out_dir:  The directory to store outputs for this trial
        n_generations:  The number of generations to execute.
        silent:         If True than no intermediary outputs will be
                        presented until solution is found.
        args:           The command line arguments holder.
    Returns:
        True if experiment finished with successful solver found.
    """

    # Load configuration.
    config = Config(config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = Population(config)

    # Create the trial simulation
    global trialSim
    trialSim = MazeSimulationTrial(maze_env=maze_env, population=p)

    # TODO: add stats object which is updated in population.
    stats = StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to N generations.
    start_time = time.time()
    best_genome = p.run(eval_genomes, update_records, n=n_generations)

    elapsed_time = time.time() - start_time

    # Display the best genome among generations.
    print('\nBest genome:\n%s' % (best_genome))

    solution_found = (best_genome.fitness >= config.fitness_threshold)
    if solution_found:
        print("SUCCESS: The stable maze solver controller was found!!!")
    else:
        print("FAILURE: Failed to find the stable maze solver controller!!!")

    # write the record store data
    rs_file = os.path.join(trial_out_dir, "data.pickle")
    trialSim.record_store.dump(rs_file)

    print("Record store file: %s" % rs_file)
    print("Trial elapsed time: %.3f sec" % (elapsed_time))

    # Visualize the experiment results
    if not silent or solution_found:

        # Draw best network.
        best_genome.network().draw()

        if args is None:
            visualize.draw_maze_records(maze_env, trialSim.record_store.records, view=True)
        else:
            visualize.draw_maze_records(maze_env, trialSim.record_store.records,
                                        view=True,
                                        width=args.width,
                                        height=args.height,
                                        filename=os.path.join(trial_out_dir, 'maze_records.svg'))
        visualize.plot_stats(stats, ylog=False, view=True, filename=os.path.join(trial_out_dir, 'avg_fitness.svg'))
        visualize.plot_species(stats, view=True, filename=os.path.join(trial_out_dir, 'speciation.svg'))

    return solution_found

if __name__ == '__main__':
    # read command line parameters
    parser = argparse.ArgumentParser(description="The maze experiment runner.")
    parser.add_argument('-m', '--maze', default='medium',
                        help='The maze configuration to use.')
    parser.add_argument('-g', '--generations', default=500, type=int,
                        help='The number of generations for the evolutionary process.')
    parser.add_argument('--width', type=int, default=400, help='The width of the records subplot')
    parser.add_argument('--height', type=int, default=400, help='The height of the records subplot')
    args = parser.parse_args()

    if not (args.maze == 'medium' or args.maze == 'hard'):
        print('Unsupported maze configuration: %s' % args.maze)
        exit(1)

    # Determine path to configuration file.
    config_path = "configs/maze.json"

    trial_out_dir = os.path.join(out_dir, args.maze)

    # Clean results of previous run if any or init the ouput directory
    utils.clear_output(trial_out_dir)

    # Run the experiment
    maze_env_config = os.path.join(local_dir, '%s_maze.txt' % args.maze)
    maze_env = maze.read_environment(maze_env_config)

    # visualize.draw_maze_records(maze_env, None, view=True)

    print("Starting the %s maze experiment" % args.maze)
    run_experiment( config_file=config_path,
                    maze_env=maze_env,
                    trial_out_dir=trial_out_dir,
                    n_generations=args.generations,
                    args=args)