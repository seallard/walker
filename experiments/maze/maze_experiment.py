import os
import time
import copy
import concurrent
import concurrent.futures
import multiprocessing
import random

from neat.config import Config
from neat.population import Population
from novelty_search.novelty_search import Archive

from . import maze_environment as maze
from . import agent

archive = Archive() # Used in novelty search to store points for novelty score calculation.

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
    return (fitness, maze_env.agent.location.x, maze_env.agent.location.y, maze_env.exit_found, control_net)

def only_novelty():
    return 1

def eval_genomes(genomes, use_novelty, weighting):
    """
    Evaluate the fitness of each genome.
    Arguments:
        genomes: The list of genomes from population in the
                 current generation
        use_novelty: Bool indicating whether to use novelty score.
        weighting: Function returning novelty weight [0,1].
    """

    cores_available = multiprocessing.cpu_count()
    executor = concurrent.futures.ProcessPoolExecutor(cores_available)
    futures = [executor.submit(eval_fitness, genome) for genome in genomes]

    found_solution = False

    archive_updates = 0
    novelty_score = 0
    points = []

    for i, future in enumerate(futures):

        fitness, x, y, hit, net = future.result()

        if use_novelty:
            novelty_score = archive.get_novelty_score((x,y))
            p = weighting()

            # TODO: normalising?
            genomes[i].original_fitness = p*novelty_score + (1-p)*fitness

            # Randomly add 6 solutions to archive per generation.
            if random.random() < 6/200 and archive_updates < 6:
                archive.add_point((x, y))
                archive_updates += 1

            # Save coordinates if any points need to be added after loop.
            points.append((x,y))

        else:
            genomes[i].original_fitness = fitness

        record = {}
        record['genome_id'] = genomes[i].id
        record['generation'] = trialSim.population.generation
        record['coordinates'] = (x, y)
        record['solution'] = int(hit)
        record['fitness'] = fitness
        record['novelty_score'] = novelty_score
        record['nodes'] = len(net.nodes)
        record['links'] = len(net.links)

        # add record to the store
        trialSim.record_store.add_record(record)

        if hit:
            found_solution = True

    # Add remaining points to archive.
    if use_novelty:
        for i in range(6-archive_updates):
            point = random.choice(points)
            archive.add_point(point)

    return found_solution

def run_experiment(config_file, maze_env, trial_out_dir, n_generations, use_novelty, weighting, experiment_id):
    """
    The function to run the experiment against hyper-parameters
    defined in the provided configuration file.
    Arguments:
        config_file:    The path to the file with experiment configuration
        maze_env:       The maze environment to use in simulation.
        trial_out_dir:  The directory to store outputs for this trial
        n_generations:  The number of generations to execute.
        use_novelty:    Whether evaluation should use novelty search.
        weighting:      How the novelty and fitness score should be combined.
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
    solution_found = p.run(eval_genomes, use_novelty, weighting, n=n_generations, run=experiment_id)
    elapsed_time = time.time() - start_time

    print(f"Time to complete run {experiment_id} out of 30: {elapsed_time}")

    if solution_found:
        print(f"Solved maze in generation {trialSim.population.generation}")

    # Write record store to file.
    result_path = os.path.join(trial_out_dir, f"run_{experiment_id}.json")
    trialSim.record_store.dump(result_path)

if __name__ == '__main__':

    config_path = "configs/maze.json"

    runs = 30
    generations = 500
    experiments = [("hard", "novelty", True, only_novelty)]
    # ("medium", "novelty", True, only_novelty),("medium", "fit", False, None), ("hard", "fit", False, None)

    for experiment in experiments:
        maze_difficulty, metric, use_novelty, weighting = experiment

        # Directory to store outputs.
        local_dir = os.path.dirname(__file__)
        out_dir = os.path.join(local_dir, "out", f"{metric}", f"{maze_difficulty}")
        os.makedirs(out_dir)

        # Config for building maze.
        maze_env_config = os.path.join(local_dir, f"{maze_difficulty}_maze.txt")

        for run in range(runs):

            print(f"Run {run} of {runs} on {maze_difficulty} maze with {metric} metric.")

            # Run the experiment
            maze_env = maze.read_environment(maze_env_config)

            # Add initial starting point to novelty search archive.
            archive.add_point((maze_env.agent.location.x, maze_env.agent.location.y))

            run_experiment( config_file=config_path,
                            maze_env=maze_env,
                            trial_out_dir=out_dir,
                            n_generations=generations,
                            use_novelty=use_novelty,
                            weighting=weighting,
                            experiment_id = run
                            )
            archive.reset()
