

class InnovationTracker:
    """Keeps track of the innovations (hidden nodes and links).

    The innovations are stored in a dictionary. The innovations are specified by
    two nodes. The innovation occurs between them, as a new node or link.
    """

    def __init__(self, num_inputs, num_outputs):
        self.innovations = {}
        self.next_innovation_number = num_inputs + num_outputs + num_inputs * num_outputs

    def assign_innovation_number(self, innovation):
        """Assigns an innovation number to gene in innovation.

        Checks whether the structure the innovation represents is new and assigns
        an innovation number accordingly. If the structure is new, it receives a
        new innovation number. Otherwise, the previous innovation number is
        retrieved and assigned to the gene in the innovation.

        Args:
            innovation: An innovation.Innovation instance.

        Side effects:
            self.innovation_number: incremented by 1 if the gene is new.
            gene.innovation_number: set to innovation number.
        """

        try:
            key = innovation.get_key()
            innovation.gene.innovation_number = self.innovations[key]

        except:
            innovation.gene.innovation_number = self.next_innovation_number
            self.innovations[innovation.get_key()] = self.next_innovation_number
            self.next_innovation_number += 1


    def reset(self):
        self.innovations = {}
