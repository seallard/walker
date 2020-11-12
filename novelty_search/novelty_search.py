from rtree import index


class NoveltySearch:


    def __init__(self):
        self.archive = index.Index()
        self.points = []
        self.point_id = 0

    def get_novelty_score(self, point, k=15):
        """Get mean distance to the k nearest neighbours. """
        neighbour_indices = self.archive.nearest(4*point, k)

        total_distance = 0
        hits = 0

        for i in neighbour_indices:
            neighbour = self.points[i]
            total_distance += self.distance(point, neighbour)
            hits += 1

        mean_distance = total_distance/hits
        return mean_distance

    def add_to_archive(self, point):
        """Add point to archive. """
        self.archive.insert(self.point_id, 4*point) # Use minimum bounding rectangle.
        self.points.append(point)
        self.point_id += 1

    def distance(self, a, b):
        """Return euclidean distance between point a and b. """
        total = 0
        dim = len(a)

        for i in range(dim):
            total += (a[i]-b[i]) ** 2
        return total ** 0.5
