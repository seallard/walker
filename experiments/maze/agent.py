#
# This is the definition of a maze navigating agent.
#
import json

class Agent:
    """
    This is the maze navigating agent
    """
    def __init__(self, location, heading=0, speed=0, angular_vel=0, radius=8.0, range_finder_range=100.0):
        """
        Creates new Agent with specified parameters.
        Arguments:
            location:               The agent initial position within maze
            heading:                The heading direction in degrees.
            speed:                  The linear velocity of the agent.
            angular_vel:            The angular velocity of the agent.
            radius:                 The agent's body radius.
            range_finder_range:     The maximal detection range for range finder sensors.
        """
        self.heading = heading
        self.speed = speed
        self.angular_vel = angular_vel
        self.radius = radius
        self.range_finder_range = range_finder_range
        self.location = location

        # defining the range finder sensors
        self.range_finder_angles = [-90.0, -45.0, 0.0, 45.0, 90.0, -180.0]

        # defining the radar sensors
        self.radar_angles = [(315.0, 405.0), (45.0, 135.0), (135.0, 225.0), (225.0, 315.0)]

        # the list to hold range finders activations
        self.range_finders = [None] * len(self.range_finder_angles)
        # the list to hold pie-slice radar activations
        self.radar = [None] * len(self.radar_angles)


class AgentRecordStore:
    """
    The class to control agents record store.
    """
    def __init__(self):
        """
        Creates new instance.
        """
        self.records = []

    def add_record(self, record):
        """
        The function to add specified record to this store.
        Arguments:
            record: The record to be added.
        """
        self.records.append(record)

    def load(self, file):
        """
        The function to load records list from the specied file into this class.
        Arguments:
            file: The path to the file to read agents records from.
        """
        with open(file, 'r') as f:
            self.records = json.load(f)

    def dump(self, file):
        """
        The function to dump records list to the specified file from this class.
        Arguments:
            file: The path to the file to hold data dump.
        """
        with open(file, 'w') as fp:
            json.dump(self.records, fp)
