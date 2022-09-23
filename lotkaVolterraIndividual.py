import numpy as np
import matplotlib.pyplot as plt
from numpy.random import uniform, choice

class State:
    def __init__(self, group):
        self.group = group

class lotkaVolterraIndividual:
    def __init__(self, preds0, preys0):

        self.state = [State("prey") for _ in range(preys0)]
        self.state += [State("pred") for _ in range(preds0)]

        self.nPreys = preys0
        self.nPreds = preds0

        self.currentTime = 0

        # propensity functions
        def preyBirthProp(state):
            if state.group == "prey":
                return 10
            else:
                return 0

        def preyEatenProp(state):
            return 10*0.001*self.nPreds

        def predEatProp(state):
            return 10*0.001*self.nPreys

        def predDeathProp(state):
            if state.group == "pred":
                return 0.5*1
            else:
                return 0

        def preyDeathProp(state):
            if state.group == "prey":
                return 0*0.5
            else:
                return 0

        self.propFuncs = [preyBirthProp, preyEatenProp, predEatProp, predDeathProp, preyDeathProp]
        self.nReactions = len(self.propFuncs)

        self.propensities = [[p(s) for s in self.state] for p in self.propFuncs]
        self.totProp = np.sum(self.propensities)
        self.probablities = self.propensities /self.totProp

        self.timeHistory = [self.currentTime]

        self.preyHistory = [preys0]
        self.predHistory = [preds0]

    def step(self):
        self.updatePropensities()
        self.updateTime()
        self.updateReaction()

    def updatePropensities(self):
        # axis=0: reactions
        # axis=1: individuals
        newPropensities = [[ p(s) for s in self.state ] for p in self.propFuncs]
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

        # Reaction effects
        if idxReaction==0:
            # prey birth
            self.state.append(State("prey"))
        if idxReaction==1:
            # prey eaten - but predator not born, that's a different event
            # or prey death
            self.state.pop(idxIndividual)
        if idxReaction==2:
            # predator eat
            self.state.append(State("pred"))
        if idxReaction==3:
            # predator death
            self.state.pop(idxIndividual)

        nPreys = 0
        nPreds = 0
        for s in self.state:
            if s.group == "prey":
                nPreys += 1
            else:
                nPreds += 1
        self.nPreys = nPreys
        self.nPreds = nPreds
        self.preyHistory.append(nPreys)
        self.predHistory.append(nPreds)

    def simulate(self, maxTime):

        stepNumber = 0
        isTerminalState = False
        maxPeople = False

        while(self.currentTime < maxTime and not isTerminalState and not maxPeople):

            if(stepNumber%50 == 0):
                print("Time: "+str(self.currentTime)[:5]+"/{0}...   {1} preys, {2} predators".format(maxTime, self.nPreys, self.nPreds))
            self.step()
            stepNumber += 1

            isTerminalState = ((self.nPreys==1) or (self.nPreds==1))
            maxPeople = self.nPreys==1000

        if isTerminalState:
            print("End of simulation: Terminal state\n\n")
        elif maxPeople:
            print("End of simulation: Max preys\n\n")
        else:
            print("End of simulation: Terminal time\n\n")

        return self.timeHistory, self.predHistory, self.preyHistory


def main():

    # Simulation conditions
    maxTime = 5
    preds0 = 50
    preys0 = 50

    nSimulations = 2
    figSim, axSim = plt.subplots(nSimulations,1)

    # run some stochastic simluations
    for sim in range(nSimulations):

        model = lotkaVolterraIndividual(preds0, preys0)

        times, preds, preys = model.simulate(maxTime)
        preds = np.array(preds)
        preys = np.array(preys)

        axSim[sim].plot(times, preds, 'r', alpha=0.7, label="Predators")
        axSim[sim].plot(times, preys, 'b', alpha=0.7, label="Preys")
        axSim[sim].legend()
        axSim[sim].set_title("Status vs time, simulation {}".format(sim))

#    fig2, ax = plt.subplots(3,1)

#    times = np.array(times)
#    timeIntervals = times[1:] - times[:-1]
#    ax[0].plot(timeIntervals, 'k')
#    ax[1].plot(times, 'k', linewidth=2)
#    ax[2].plot(np.sum(propensities, axis=1))
#    ax[0].set_title("Time intervals along iterations")
#    ax[1].set_title("(Flow of) Time along iterations")
#    ax[2].set_title("Total propensity along iterations")
#    ax[0].set_xticks([])
#    ax[1].set_xticks([])
#    fig2.suptitle("From last simulation")

    plt.show()

if(__name__ == '__main__'):
    main()
