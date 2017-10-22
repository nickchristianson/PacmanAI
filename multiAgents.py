# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        # print bestScore
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print bestIndices
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print chosenIndex

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        totalScore = 0


        #is there food left? if yes, compute shortest distance to food
        food_left = sum(int(j) for i in newFood for j in i)
        food_list = newFood.asList()
        manDistFood = []
        closestFood = 0
        if food_left > 0:
            for food in food_list:
                manDist = util.manhattanDistance(pacPos, food)
                manDistFood.append(manDist)
            closestFood = min(manDistFood)
        else:
            closestFood = 0
        #calculate distance of ghost(s)
        ghostDist = []
        for position in currentGameState.getGhostPositions():
            manDist = util.manhattanDistance(pacPos, position)
            ghostDist.append(manDist)
        if newGhostStates:
            closest_ghost = min(ghostDist)
            if closest_ghost == 0:
                closest_ghost = -2000
            else:
                closest_ghost = -20/closest_ghost
        else:
            closest_ghost = 0

        return  (-closestFood + closest_ghost) - (20 * food_left)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

def average(lst):
    lst = list(lst)
    return sum(lst) / len(lst)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        total_agents = gameState.getNumAgents()
        def new_depths(state, depth, agent):
            if agent == total_agents:
                #terminal test
                if depth == self.depth:
                    return self.evaluationFunction(state)
                #else, recurse until we hit the desired depth
                else:
                    return new_depths(state, depth+1, 0)
            else:
                legalActions = state.getLegalActions(agent)
                #if no actions available, return eval
                if(len(legalActions)==0):
                    return self.evaluationFunction(state)

                new_states = []
                for action in legalActions:
                    depths = new_depths(state.generateSuccessor(agent, action),
                    depth, agent+1)
                    new_states.append(depths)
                if(agent==0):
                    return max(new_states)
                else:
                    return sum(new_states)/len(new_states)

        return max(gameState.getLegalActions(0),
    key=lambda x: new_depths(gameState.generateSuccessor(0,x),
    1,1))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    totalScore = 0


    #######find distance to closest food#################################
    food_left = currentGameState.getNumFood()
    food_list = newFood.asList()
    manDistFood = []
    closestFood = 0
    if food_left > 0:
        for food in food_list:
            manDist = util.manhattanDistance(pacPos, food)
            manDistFood.append(manDist)


    if closestFood:
        closestFood = min(manDistFood)
        closestFood = 1.0/food_left
        closestFood = float(closestFood)

    else:
        closestFood = 1000
    ###########################################################################

    ##########################Distance to Closest Ghost########################
    ghostDist = []
    for position in currentGameState.getGhostPositions():
        manDist = util.manhattanDistance(pacPos, position)
        ghostDist.append(manDist)
    closest_ghost = min(ghostDist)

    if newGhostStates:
        if closest_ghost == 0:
            closest_ghost = 20000
        else:
            closest_ghost = 1.0/closest_ghost
            closest_ghost = float(closest_ghost)
    else:
        closest_ghost = 0
    ###########################################################################


    ###############################Power Pellets###############################
    powerDists = []
    closestPellet = 0
    pellets_left = len(capsules)
    for position in capsules:
        manDist = util.manhattanDistance(pacPos, position)
        powerDists.append(manDist)


    if capsules:
        closestPellet = min(powerDists)
        closestPellet = 1.0/closestPellet
        closestPellet = float(closestPellet)
    else:
        closestPellet = 0
    ###########################################################################


    ###########################Spooped Ghosts##################################
    spoopedDist = []
    shortestSpoop = 0
    for spoopedGhost in newScaredTimes:
        if spoopedGhost > 0:
            for position in currentGameState.getGhostPositions():
                manDist = util.manhattanDistance(pacPos, position)
                spoopedDist.append(manDist)
            if spoopedDist:
                shortestSpoop = min(spoopedDist)
                if shortestSpoop == 0:
                    shortestSpoop = 10
                else:
                    shortestSpoop = 1/shortestSpoop

    ###########################################################################


    featureWeights = [1,-10, -1, 10, -100, 10]
    features = [closestFood, food_left, closest_ghost, closestPellet, pellets_left, shortestSpoop]

    totalScore = sum(i*j for i, j in zip(featureWeights, features))


    return totalScore

# Abbreviation
better = betterEvaluationFunction
