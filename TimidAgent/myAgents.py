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

        # Your code
        pac_pos = pacman.getPacmanPosition()
        ghosts_pos= ghost.getGhostPositions()
        pac_row, pac_col = pac_pos
        for ghost_pos in ghosts_pos:
            ghost_row, ghost_col = ghost_pos
            if not ghost.scared():
                if abs(pac_row - ghost_row) <= dist or abs(pac_col - ghost_col) <= dist:
                    return ghost.direction()
        else:
            return Directions.STOP


    def getAction(self, state):
        """
        state - GameState

        Fill in appropriate documentation
        """
        # List of directions the agent can choose from
        legal = state.getLegalPacmanActions()

        # Get the agent's state from the game state and find agent heading
        agentState = state.getPacmanState()
        heading = agentState.getDirection()

        if heading == Directions.STOP:
            # Pacman is stopped, assume North (true at beginning of game)
            heading = self.inDanger(agentState, state.getGhostState(1))

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
