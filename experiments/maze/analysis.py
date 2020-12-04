import json
import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

runs = 30
local_dir = os.path.dirname(__file__)


def load_experiment_data(metric, maze):
    all_runs = []
    for run in range(runs):
        data = json.load(open(f"{local_dir}/out/{metric}/{maze}/run_{run}.json", "r" ))
        all_runs.append(data)
    return all_runs


def get_solutions(runs):
    solutions = []
    for run_data in runs:
        for i, evaluation in enumerate(run_data):
            if evaluation['solution'] == 1:
                evaluation['eval'] = i
                solutions.append(evaluation)
                break
    return solutions


def print_stats(solutions, experiment):
    metric, maze = experiment

    print("-------------------------------------------------------------------------")
    print(f"Statistics for solutions in experiment with {metric} on the {maze} maze.")
    print("-------------------------------------------------------------------------")

    evals = [solution['eval'] for solution in solutions]

    print(f"Successful runs: {len(solutions)}")
    print(f"Worst successful run: {max(evals)}")

    print(f"Mean evaluations until solved: {statistics.mean(evals)}")
    print(f"Stdev evaluations until solved: {statistics.stdev(evals)}")

    links = [solution['links'] - 21 for solution in solutions]
    hidden_nodes = [solution['nodes'] - 13 for solution in solutions]

    print(f"Mean hidden_nodes: {statistics.mean(hidden_nodes)}")
    print(f"Stdev hidden_nodes: {statistics.stdev(hidden_nodes)}")

    print(f"Mean links: {statistics.mean(links)}")
    print(f"Stdev links: {statistics.stdev(links)}")


def format_data_for_plot(data):
    filtered_runs = []

    for run in data:
        fitness_values = []

        for evaluation in run:
            fitness_values.append(evaluation['fitness'])

            if evaluation['solution'] == 1:
                break

        filtered_runs.append(fitness_values)

    # Pad to the same length.
    for run in filtered_runs:
        remainder = 500*200 - len(run) # Total evals - actual.
        run += remainder*[run[-1]]

    return filtered_runs


def plot_average_fitness(experiments_data, labels, export):

    for data in experiments_data:
        filtered_data = format_data_for_plot(data)

        data = np.array(filtered_data)
        raw_average = np.average(data, axis=0)

        y = np.mean(raw_average.reshape(-1, 200), axis=1) # Average of generation.
        x = np.arange(start=0, stop=500)

        plt.plot(x, y)

    plt.xlabel("Generations")
    plt.ylabel("Average fitness")
    plt.legend(labels, loc=4)

    if export:
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
        plt.savefig("fitness.pgf")

    else:
        plt.show()


experiments = [("pure_fitness", "hard")]
experiments_data = []

for experiment in experiments:
    metric, maze = experiment

    data = load_experiment_data(metric, maze)
    experiments_data.append(data)

    solutions = get_solutions(data)
    print_stats(solutions, experiment)

labels = ["Fitness"]
plot_average_fitness(experiments_data, labels, False)
