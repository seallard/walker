import os
import time
import copy
import concurrent
import concurrent.futures
import multiprocessing

from neat.config import Config
from neat.population import Population

from . import maze_environment as maze
from . import agent


class MazeSimulationTrial:
    def __init__(self, maze_env, population):
        """
        Holds maze simulator and results.
        Arguments:
            maze_env:   The maze environment as loaded from configuration file.
            population: The population for this trial run
        """
        self.orig_maze_environment = maze_env
        self.record_store = agent.AgentRecordStore()
        self.population = population

def store_records(genomes):
    """Store results from each genome. """

    for genome in genomes:

        record = {}
        record['coordinates'] = (genome.x, genome.y)
        record['genome_id'] = genome.id
        record['generation'] = trialSim.population.generation
        record['solution'] = int(genome.hit)
        record['species_id'] = genome.species_id
        record['species_age'] = genome.species_age
        record['fitness'] = genome.original_fitness

        network = genome.network()
        record['nodes'] = len(network.nodes)
        record['links'] = len(network.links)

        # add record to the store
        trialSim.record_store.add_record(record)

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
    return (fitness, maze_env.agent.location.x, maze_env.agent.location.y, maze_env.exit_found)

def eval_genomes(genomes):
    """
    Evaluate the fitness of each genome.
    Arguments:
        genomes: The list of genomes from population in the
                 current generation
    """

    cores_available = multiprocessing.cpu_count()
    executor = concurrent.futures.ProcessPoolExecutor(cores_available)
    start_time = time.time()
    futures = [executor.submit(eval_fitness, genome) for genome in genomes]

    found_solution = False

    for i, future in enumerate(futures):

        fitness, x, y, hit = future.result()

        genomes[i].original_fitness = fitness
        genomes[i].adjusted_fitness = fitness
        genomes[i].x = x
        genomes[i].y = y
        genomes[i].hit = hit

        if hit:
            found_solution = True

    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return found_solution

def run_experiment(config_file, maze_env, trial_out_dir, n_generations, experiment_id):
    """
    The function to run the experiment against hyper-parameters
    defined in the provided configuration file.
    Arguments:
        config_file:    The path to the file with experiment configuration
        maze_env:       The maze environment to use in simulation.
        trial_out_dir:  The directory to store outputs for this trial
        n_generations:  The number of generations to execute.
    Returns:
        True if experiment finished with successful solver found.
    """

    # Load NEAT configuration.
    config = Config(config_file)

    # Create population.
    p = Population(config)

    # Create the trial simulation.
    global trialSim
    trialSim = MazeSimulationTrial(maze_env=maze_env, population=p)

    # Run for N generations.
    start_time = time.time()
    solution_found = p.run(eval_genomes, store_records, n=n_generations)
    elapsed_time = time.time() - start_time

    print(f"Performed {n_generations*config.population_size} evaluations in {elapsed_time} seconds")

    if solution_found:
        print(f"Solved in generation {trialSim.population.generation}")

    # Save record store data for entire run to file.
    result_path = os.path.join(trial_out_dir, f"run_{experiment_id}.json")
    trialSim.record_store.dump(result_path)

if __name__ == '__main__':

    maze_difficulty = "hard"
    metric = "pure_fitness"
    generations = 500
    runs = 30

    # Directory to store outputs.
    local_dir = os.path.dirname(__file__)
    out_dir = os.path.join(local_dir, "out", f"{metric}", f"{maze_difficulty}")
    os.makedirs(out_dir)

    # Configs
    config_path = "configs/maze.json"
    maze_env_config = os.path.join(local_dir, f"{maze_difficulty}_maze.txt")

    for run in range(runs):

        print(f"Run {run}")

        # Run the experiment
        maze_env = maze.read_environment(maze_env_config)

        run_experiment( config_file=config_path,
                        maze_env=maze_env,
                        trial_out_dir=out_dir,
                        n_generations=generations,
                        experiment_id = run
                        )