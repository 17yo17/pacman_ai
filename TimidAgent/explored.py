#Ryo Taono
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class Explored:

    def __init__(self):
        self.visited_set = set()

    def add(self, state):
        # adding current state to the visited set
        self.visited_set.add(state)

    def exists(self, state):
        # checking if the state exists in the visited set
        return state in self.visited_set


