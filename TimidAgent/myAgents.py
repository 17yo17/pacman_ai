from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent
import numpy as np

class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor
        # Add anything else you think you need here

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """

        #Get the positions of the pacman and the ghost
        pac_pos = pacman.getPosition()
        ghost_pos = ghost.getPosition()

        #Get the row and column of the pacman and the ghost
        pac_col, pac_row = pac_pos
        ghost_col, ghost_row = ghost_pos

        if ghost.scaredTimer > 0:
            return pacman.getDirection()
        else:
            if pac_row == ghost_row:
                return ghost.getDirection()
            if pac_col == ghost_col:
                return ghost.getDirection()
            if abs(pac_row - ghost_row) <= dist:
                return ghost.getDirection()
            if abs(pac_col - ghost_col) <= dist:
                return ghost.getDirection()

        return Directions.STOP


    def getAction(self, state):
        """
        state - GameState

        Fill in appropriate documentation
        """
        # List of directions the agent can choose from
        legal = state.getLegalPacmanActions()

        # Get the agent's state from the game state and find agent heading
        pacmanState = state.getPacmanState()
        ghostStates = state.getGhostStates()
        heading = pacmanState.getDirection()

        for ghostState in ghostStates:
            heading = self.inDanger(pacmanState, ghostState)
            if heading != Directions.STOP:
                break


        if heading == Directions.STOP:
            # Pacman is stopped, assume North (true at beginning of game)
            heading = Directions.NORTH

        # Turn left if possible
        left = Directions.LEFT[heading]  # What is left based on current heading
        if left in legal:
            action = left
        else:
            # No left turn
            if heading in legal:
                action = heading  # continue in current direction
            elif Directions.RIGHT[heading] in legal:
                action = Directions.RIGHT[heading]  # Turn right
            elif Directions.REVERSE[heading] in legal:
                action = Directions.REVERSE[heading]  # Turn around
            else:
                action = Directions.STOP  # Can't move!

        return action
