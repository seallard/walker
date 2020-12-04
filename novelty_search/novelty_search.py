from rtree import index


class Archive:


    def __init__(self):
        self.archive = index.Index()
        self.points = []
        self.point_index = 0

    def get_novelty_score(self, point, k=15):
        """Get mean distance to the k nearest neighbours. """
        neighbour_indices = self.archive.nearest(2*point, k)

        total_distance = 0
        hits = 0

        for i in neighbour_indices:
            neighbour = self.points[i]
            total_distance += self.distance(point, neighbour)
            hits += 1

        mean_distance = total_distance/hits
        return mean_distance

    def add_point(self, point):
        """Add point to archive. """
        self.archive.insert(self.point_index, 2*point) # Use minimum bounding rectangle.
        self.points.append(point)
        self.point_index += 1

    def distance(self, a, b):
        """Return euclidean distance between point a and b. """
        total = (a[0] - b[0])**2 + (a[1] - b[1])**2
        return total ** 0.5

    def reset(self):
        self.points = []
        self.archive = index.Index()
        self.point_index = 0
