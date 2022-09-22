from numpy.random import choice
from numpy.random import uniform
import numpy as np

class Reaction:
    def __init__(self, name, propensity, apply):
        """
        name: str
        propensity: callable (State, Time --> Propensity)
        apply: callable (State --> State)
        [State is a user-defined class]
        """
        self.name = name
        self.propensity = propensity
        self.apply = apply

class GillespieModel:
    def __init__(self, reactions, isTerminalState = lambda x: False):
        self.nReactions = len(reactions)

        self.propensities = []
        self.probabilities = []
        self.totPropensity = 0
        self.propensityHistory = []

        self.currentTime = 0
        self.timeHistory = [0]

        self.state = 0
        self.stateHistory = []
        self.maxTime = 0

        self.reactions = reactions
        self.reactionHistory = ["initialState"]

        self.isTerminalState = isTerminalState

    def step(self):
        self.updatePropensities()
        self.updateTime()
        self.updateReaction()

    def updatePropensities(self):
        newPropensities = [j.propensity(self.state, self.currentTime) for j in self.reactions]
        self.propensities = newPropensities
        self.totPropensity = np.sum(newPropensities)
        self.probabilities = newPropensities /np.sum(newPropensities)
        self.propensityHistory.append(newPropensities)

    def updateTime(self):
        rand = uniform()
        invPropSum = 1/self.totPropensity
        timeInterval = invPropSum*np.log(1/rand)
        self.currentTime += timeInterval
        self.timeHistory.append(self.currentTime)

    def updateReaction(self):
        reaction = choice(self.reactions, p=self.probabilities)
        self.state = reaction.apply(self.state)
        self.stateHistory.append(self.state)
        self.reactionHistory.append(reaction.name)

    def simulate(self, initState, maxTime, initTime=0):

        # reset Simulation
        self.currentTime = initTime
        self.state = initState

        # clear histories
        self.stateHistory = [initState]
        self.timeHistory = [initTime]
        self.propensityHistory = []
        self.reactionHistory = ["initialState"]

        stepNumber = 0

        while(self.currentTime < maxTime and not self.isTerminalState(self.state)):
            if(stepNumber%50 == 0):
                print("Time: "+str(self.currentTime)[:5]+"/"+str(maxTime)[:5]+"...")
            self.step()
            stepNumber += 1
        print("End of simulation\n\n")

        # we update a last time the propensities in order to have their history the same length of the others
        self.updatePropensities()

        return self.timeHistory, self.stateHistory, self.reactionHistory, self.propensityHistory


class individualGillespieModel:
    def __init__(self, reactions, nGroups):
        self.nReactions = len(reactions)
        self.reactions = reactions

        self.propensities = [[]]
        self.probabilities = [[]]
        self.totPropensity = 0

        self.currentTime = 0
        self.timeHistory = [0]
        self.maxTime = 0

        self.state = []
        self.populationHistory = [0]

        self.nGroups = nGroups
        self.population = [0]

    def step(self):
        self.updatePropensities()
        self.updateTime()
        self.updateReaction()
        self.updateGroups()

    def updatePropensities(self):
        # axis=0: reactions
        # axis=1: individuals
        newPropensities = [[ j.propensity(s, self.currentTime) for s in self.state ] for j in self.reactions]
        self.propensities = newPropensities
        self.totPropensity = np.sum(newPropensities)
        self.probabilities = newPropensities /self.totPropensity

    def updateTime(self):
        rand = uniform()
        invPropSum = 1/self.totPropensity
        timeInterval = invPropSum*np.log(1/rand)
        self.currentTime += timeInterval
        self.timeHistory.append(self.currentTime)

    def updateReaction(self):
        # Draw row = reaction
        reactionProb = np.sum(self.probabilities, axis=1)
        idxReaction = choice(np.arange(self.nReactions), p=reactionProb)

        # Draw column = individual
        nIndividuals = len(self.state)

        individualProb = self.probabilities[idxReaction, :] /reactionProb[idxReaction]
        idxIndividual = choice(np.arange(nIndividuals), p=individualProb)

        reaction = self.reactions[idxReaction]
        individual = self.state[idxIndividual]

        # Update state of the individual
        self.state[idxIndividual] = reaction.apply(individual)

    def updateGroups(self):
        population = np.zeros(self.nGroups)
        newState = []
        for i in self.state:
            if i.exist:
                population[i.group] += 1
                newState.append(i)
        self.state = newState
        self.population = population
        self.populationHistory.append(population)

    def simulate(self, initState, maxTime, initTime=0):

        # reset Simulation
        self.currentTime = initTime
        self.state = initState

        # clear histories
        self.populationHistory = []
        self.timeHistory = [initTime]

        self.updateGroups()

        stepNumber = 0

        isTerminalState = False

        while(self.currentTime < maxTime and not isTerminalState):

            for n in self.population:
                isTerminalState = isTerminalState or (n==1)

            if(stepNumber%50 == 0):
                print("Time: "+str(self.currentTime)[:5]+"/"+str(maxTime)[:5]+"...")
            self.step()
            stepNumber += 1

        if isTerminalState:
            print("End of simulation: Terminal state\n\n")
        else:
            print("End of simulation: Terminal time\n\n")

        return self.timeHistory, self.populationHistory
