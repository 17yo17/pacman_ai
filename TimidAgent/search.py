
# Ryo Taono
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


import util
import explored

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    print(problem._visitedlist)
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def genericSearch(problem, g, h):
    state = problem.getStartState()
    goal = problem.goal

# Generic graph search
def graph_search(problem, g, h):
    # declare frontier as PriorityQueue and push initial state
    frontier = util.PriorityQueue()
    frontier.push(SearchNode(problem.getStartState()), 0)
    # declare a explored set that keeps track of all the states that are explored
    explored_set = explored.Explored()
    # loop until frontier becomes empty
    while frontier:
        # node is set to state with the highest priority (lowest in priority queue)
        # added to the  explored set
        node = frontier.pop()
        explored_set.add(node.state)
        # check if node is the goal
        if problem.isGoalState(node.state):
            # trace back from goal state to initial state
            # the sequence of actions is the reverse order of the trace
            path_back = []
            while node:
                path_back.append(node)
                node = node.parent
            return [node.action for node in list(reversed(path_back))[1:]]
        # get child nodes of the current node
        for child in node.expand(problem):
            # check if state of the child is not explored nor in the frontier
            if not explored_set.exists(child.state) and child.state not in [n[2].state for n in frontier.heap]:
                frontier.push(child, g(child) + h(child, problem))
    return None

class DepthFirstSearch:
    @classmethod
    def g(cls,node):
        # DepthFirstSearch doesn't care about cost to the current state
        return 0
    @classmethod
    def h(cls,node, problem):
        # the highest priority is the deepest node (highest depth * (-1))
        return -node.depth
    @classmethod
    def search(cls,problem):
        return graph_search(problem, cls.g, cls.h)
class BreadthFirstSearch:
    @classmethod
    def g(cls,node):
        # the highest priority is the lowest depth
        return node.depth
    @classmethod
    def h(cls,node, problem):
        # BreadthFirstSearch doesn't care about cost to the goal
        return 0
    @classmethod
    def search(cls, problem):
        return graph_search(problem, cls.g, cls.h)

class UniformCostSearch:
    @classmethod
    def g(cls,node):
        return 0
    @classmethod
    def h(cls,node, problem):
        return 0
    @classmethod
    def search(cls,problem):
        return graph_search(problem, cls.g, cls.h)

class AStarSearch:
    @classmethod
    def g(cls,node):
        # cost is the depth of the node
        return node.depth
    @classmethod
    def h(cls, node, problem):
        # nullHeuristic calculates the length of the straight line between the current node and goal
        return nullHeuristic(node.state, problem)
    @classmethod
    def search(cls, problem):
        return graph_search(problem, cls.g, cls.h)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # search function returns the list of actions from the initial to goal
    return DepthFirstSearch.search(problem)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # search function returns the list of actions from the initial to goal
    return BreadthFirstSearch.search(problem)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    # calculate the length of the line between the current node and goal
    goal = problem.goal
    dx = goal[0] - state[0]
    dy = goal[1] - state[1]
    cost = dx * dx + dy * dy
    return cost ** (1/2)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # search function returns the list of actions from the initial to goal
    return AStarSearch.search(problem)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

class SearchNode:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        # get successors of the current node
        child_nodes = problem.getSuccessors(self.state)
        # return list of SearchNode child nodes
        return [self.child_node(child_node)
                for child_node in child_nodes]
    def child_node(self, child_node):
        """[Figure 3.10]"""
        # create SearchNode next node
        child_state, action, _ = child_node
        next_node = SearchNode(child_state, self, action)
        return next_node