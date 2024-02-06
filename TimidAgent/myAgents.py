from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent

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

        # Ghost is scared so who cares!
        if ghost.scaredTimer > 0:
            return Directions.STOP
        else:
            #pacman is within the dangerous distance (dist)
            if abs(pac_row == ghost_row) <= dist and abs(pac_col - ghost_col) <= dist:
                # pacman and ghost are in the same row
                if pac_row == ghost_row:
                    # ghost is located at west from pacman
                    if pac_col > ghost_col:
                        return Directions.WEST
                    # ghost is located at east from pacman
                    else:
                        return Directions.EAST
                # pacman and ghost are in the same column
                elif pac_col == ghost_col:
                    # ghost is located at south from pacman
                    if pac_row > ghost_row:
                        return Directions.SOUTH
                    # ghost is located at north from pacman
                    else:
                        return Directions.NORTH
        # pacman is not in danger, return stop
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
        heading = pacmanState.getDirection()
        # Get the ghosts' state from the game
        ghostStates = state.getGhostStates()

        # Fetch each ghost's state every loop
        for ghostState in ghostStates:
            # inDanger returns ghost's location from pacman. (if not in danger, then it returns STOP)
            danger = self.inDanger(pacmanState, ghostState)
            # check if pacman is in danger
            if danger != Directions.STOP:
                # Check if reverse direction is legal action
                if Directions.REVERSE[danger] in legal:
                    return Directions.REVERSE[danger]
                # Check if going left is legal action
                elif Directions.LEFT[danger] in legal:
                    return Directions.LEFT[danger]
                # Check if going right is legal action
                elif Directions.RIGHT[danger] in legal:
                    return Directions.RIGHT[danger]
                # No change in direction
                elif heading in legal:
                    return heading
                # nowhere to go..
                else:
                    return Directions.STOP


        # If pacman is not in danger, act like the LeftTurnAgent
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
