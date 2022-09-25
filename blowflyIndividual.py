import numpy as np
import matplotlib.pyplot as plt
from numpy.random import uniform, choice

class State:
    # GLOBAL state - population
    def __init__(self, nJ, nA):
        self.nJ = nJ
        self.nA = nA

class Reaction:
    def __init__(self, name, prop):
        self.name = name
        self.prop = prop

class blowflyModel:
    def __init__(self, n0J, n0A, maturationAge, dJ, beta, c, dA):

        self.dJ = dJ
        self.beta = beta
        self.c = c
        self.dA = dA
        self.maturationAge = maturationAge

        self.state = State(n0J, n0A)
        self.agesJ = [0 for _ in range(n0J)] # All juveniles have initial age = 0
        self.agesA = [maturationAge for _ in range(n0A)] # All adults have initial age = maturationAge

        self.currentTime = 0
        self.timeInterval = 0

        jDeath = Reaction(
            "juvenileDeath",
            lambda state: self.dJ*state.nJ
        )
        jBirth = Reaction(
            "juvenileBirth",
#            lambda state: self.beta*pow(np.e, -state.nA/self.c)
            lambda state: self.beta*self.state.nA
        )
        aDeath = Reaction(
            "adultDeath",
            lambda state: self.dA*state.nA
        )

        self.reactions = [jDeath, jBirth, aDeath]
        self.nReactions = len(self.reactions)

        self.propensities = [r.prop(self.state) for r in self.reactions]
        self.totProp = np.sum(self.propensities)
        self.probabilities = self.propensities /self.totProp

        self.timeHistory = [self.currentTime]

        self.jHistory = [n0J]
        self.aHistory = [n0A]

    def step(self):
        self.updatePropensities()
        self.updateTime()
        self.updateAges()
        self.updateReaction()

    def updatePropensities(self):
        self.propensities = [r.prop(self.state) for r in self.reactions]
        self.totProp = np.sum(self.propensities)
        self.probabilities = self.propensities /self.totProp

    def updateTime(self):
        rand = uniform()
        invPropSum = 1/self.totProp
        self.timeInterval = invPropSum*np.log(1/rand)
        self.currentTime += self.timeInterval
        self.timeHistory.append(self.currentTime)

    def updateAges(self):
        self.agesA = [age+self.timeInterval for age in self.agesA]

        newAgesJ = []
        for age in self.agesJ:
            age += self.timeInterval
            if age > self.maturationAge:
                self.agesA.append(age)
                self.state.nA += 1
                self.state.nJ -= 1
            else:
                newAgesJ.append(age)

        self.agesJ = newAgesJ

    def updateReaction(self):
        reaction = choice(self.reactions, p=self.probabilities)

        # Reaction effects
        if reaction.name=="juvenileDeath":
            randomJuvenile = choice( range(len(self.agesJ)) )
            self.agesJ.pop(randomJuvenile)
            self.state.nJ = self.state.nJ - 1
        if reaction.name=="juvenileBirth":
            self.agesJ.append(0)
            self.state.nJ = self.state.nJ + 1
        if reaction.name=="adultDeath":
            randomAdult = choice( range(len(self.agesA)) )
            self.agesA.pop(randomAdult)
            self.state.nA = self.state.nA - 1

        assert(self.state.nJ == len(self.agesJ))
        assert(self.state.nA == len(self.agesA))

        self.jHistory.append(self.state.nJ)
        self.aHistory.append(self.state.nA)

    def simulate(self, maxTime):

        stepNumber = 0
        isTerminalState = False

        while(self.currentTime < maxTime and not isTerminalState):

            if(stepNumber%50 == 0):
                print("Time: "+str(self.currentTime)[:5]+"/{0}...   {1} Juveniles, {2} Adults".format(maxTime, self.state.nJ, self.state.nA))
            self.step()
            stepNumber += 1

            isTerminalState = (self.state.nJ+self.state.nA <= 1)

        if isTerminalState:
            print("End of simulation: Terminal state\n\n")
        else:
            print("End of simulation: Terminal time\n\n")

        return self.timeHistory, self.jHistory, self.aHistory


def main():

    # Simulation conditions
    maxTime = 10
    n0J = 0
    n0A = 10000

    maturationAge = 15.6
    dJ = 0.0060455567
    beta = 8.5
    c = 600.0
    dA = 0.27

    nSimulations = 2
    figSim, axSim = plt.subplots(nSimulations,1)

    # run some stochastic simluations
    for sim in range(nSimulations):

        model = blowflyModel(n0J, n0A, maturationAge, dJ, beta, c, dA)

        times, nJ, nA = model.simulate(maxTime)
        nJ = np.array(nJ)
        nA = np.array(nA)

        axSim[sim].plot(times, nJ, 'b', alpha=0.7, label="juveniles")
        axSim[sim].plot(times, nA, 'r', alpha=0.7, label="adults")
        axSim[sim].legend()
        axSim[sim].set_title("Status vs time, simulation {}".format(sim))

    plt.show()

if(__name__ == '__main__'):
    main()
