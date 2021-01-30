import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
import seaborn as sns
import geometry
import json
import os
import numpy as np


runs = 30
local_dir = os.path.dirname(__file__)

def get_endpoints(run):
    end_points = []
    for evaluation in run:
        end_points.append(evaluation['coordinates'])
        if evaluation['solution']:
            break
    return end_points

def load_experiment_data(metric, maze):
    all_runs = []
    for run in range(runs):
        data = json.load(open(f"{local_dir}/{metric}/{maze}/run_{run}.json", "r" ))
        all_runs.append(data)
        break
    return all_runs

def get_walls(file_path):
    walls = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file.readlines()):
            line = line.strip()
            if i == 1:
                start = geometry.read_point(line)
            if i == 3:
                end = geometry.read_point(line)
            if i > 3:
                wall = geometry.read_line(line)
                walls.append(wall)
    return walls, start, end

def draw_maze(xs, ys):
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 140)

    walls, start, end = get_walls("medium_maze.txt")
    for wall in walls:
        line = plt.Line2D((wall.a.x, wall.b.x), (wall.a.y, wall.b.y), lw=1.5)
        ax.add_line(line)

    start = plt.Circle((start.x, start.y), radius=5, facecolor="green")
    ax.add_patch(start)

    end = plt.Circle((end.x, end.y), radius=5, facecolor="red")
    ax.add_patch(end)

    plt.scatter(xs, ys)
    plt.show()

def draw_heat_map(xs, ys):
    heatmap, xedges, yedges = np.histogram2d(xs, ys, bins=200)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()


experiments = ["pure_fitness", "pure_novelty", "fitness_novelty", "novelty_injection", "dynamic"]
maze = "open"

for experiment in experiments:
    all_runs = load_experiment_data(experiment, maze)

    all_points = []

    for run in all_runs:
        end_points = get_endpoints(run)
        all_points += end_points
    print(len(all_points))


    xs = [tup[0] for tup in all_points]
    ys = [tup[1] for tup in all_points]

    plot = sns.jointplot(x=xs, y=ys, kind='scatter')

    walls, start, end = get_walls(f"{maze}_maze.txt")

    for wall in walls:
        plot.ax_joint.plot([wall.a.x,wall.b.x], [wall.a.y, wall.b.y], 'black', linewidth = 2)

    plot.ax_marg_x.set_axis_off()
    plot.ax_marg_y.set_axis_off()
    plot.ax_joint.set_xticks([])
    plot.ax_joint.set_yticks([])


    sns.despine(ax=plot.ax_joint, bottom=True, left=True)

    # Draw start and end points.
    plot.ax_joint.plot([start.x], [start.y],'o', ms=35, mec='g', mfc='g', alpha=0.5)
    plot.ax_joint.plot([end.x], [end.y],'o', ms=35, mec='r', mfc='r', alpha=0.5)


    #plot.ax_joint.set_xlim(0,205)
    #plot.ax_joint.set_ylim(0,200)
    plt.show()
    #plt.savefig(f"{experiment}_{maze}_all_runs")
    #plt.close()
