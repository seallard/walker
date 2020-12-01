

class Link:
    __slots__ = ['from_node', 'to_node', 'weight', 'id']
    def __init__(self, from_node, to_node, weight, id):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.id = id
