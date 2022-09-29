from numpy.random import uniform
import numpy as np
import pandas as pd

class Individual:
    def __init__(self, id, isAlive=True, age=0, group="J"):
        self.id = id
        self.isAlive = isAlive
        self.age = age
        self.group = group

    def reactionRates(self, cfg, N):
        reactionProps = [0, 0]
        if self.isAlive:
            if self.group=="J":
                reactionProps[0] = 0       # birth
                reactionProps[1] = cfg.dJ  # death
            if self.group=="A":
                reactionProps[0] = cfg.beta*pow(np.e, -N[1]/cfg.c)  # birth
                reactionProps[1] = cfg.dA                     # death

        return reactionProps

class Reaction:
    def __init__(self, indivId, type, propIncrement):
        self.indivId = indivId
        self.type = type
        self.propIncrement = propIncrement

class CFG:
    # Configuration
    # It holds model parameters, initial conditions, etc.
    def __init__(self, dJ=0.0060455567, dA=0.27, beta=8.5, c=600, tau=15.6,
                 nReactions=2,
                 maxIndividuals=35000, N0=[0,5000], maxTime=120):
        self.dJ = dJ
        self.dA = dA
        self.beta = beta
        self.c = c
        self.tau = tau
        self.nReactions = nReactions
        self.maxIndividuals = maxIndividuals
        self.N0 = N0
        self.maxTime = maxTime

class globalState:
    # The global state common to all the groups and individuals. All the algorithm is
    # managed by a single instance of this class.
    def __init__(self, cfg, seed=53):

        np.random.seed(seed)

        # Initialize population array - with initial states
        # N[0] = Juveniles, N[1]: Adults
        self.N = cfg.N0

        juveniles = [Individual(i, group="J") for i in range(self.N[0])]
        adults = [Individual(i, group="A") for i in range(self.N[1])]
        totN = cfg.N0[0]+cfg.N0[1]
        rest =  [Individual(i, isAlive=False) for i in range(cfg.maxIndividuals)[totN:] ]

        self.populationArray = juveniles+adults+rest

        # Initialize reaction array - empty
        self.reactionArray = []
        for i in self.populationArray:
            reactionProps = i.reactionRates(cfg, self.N)
            self.reactionArray += [Reaction(i.id, "Birth", reactionProps[0]), Reaction(i.id, "Death", reactionProps[1])]

        # Initialize propensities array - empty
        self.cumPropArray = [0 for _ in self.reactionArray]
        self.totProp = 0

        self.t = 0
        self.dt = 0
        self.reactionIdx = 0
        self.rType = ""

        self.isTerminalState = False
        self.terminalLog = "End of simulation: max time"

        self.jHistory = []
        self.aHistory = []
        self.tHistory = []

    def printDebug(self):
        # mainly for debugging
        if not self.isTerminalState:
            aliveCount = 0
            n = 0
            log = ""
            for i in self.populationArray:
                n += 1
                if i.isAlive:
                    aliveCount += 1
                    log += i.group
                    if aliveCount==(self.N[0]+self.N[1]):
                        break
                else:
                    log += "_"
        if self.isTerminalState:
            log = self.terminalLog

        print("t: "+str(self.t)[:6]+" N: "+str(self.N)+" "+log)

    def printCsvLine(self):
        # prints in csv format, so you can run simply:
        # "python script.py >> output.csv" from command line
        print(str(self.t)+','+str(self.N[0])+','+str(self.N[1]))

    def updatePropensities(self, cfg):

        totProp = 0
        aliveCount = 0
        self.cumPropArray = [0 for _ in self.cumPropArray]
        for i in range(cfg.maxIndividuals):

            reactionRates = self.populationArray[i].reactionRates(cfg, self.N)

            for j in range(cfg.nReactions):
                totProp += reactionRates[j]
                self.cumPropArray[cfg.nReactions*i + j] = totProp

            if self.populationArray[i].isAlive:
                aliveCount += 1
                if aliveCount==self.N:  !!! !!! !!! !!! !!! Idiota
                    break

        self.totProp = totProp
        if self.totProp == 0:
            isTerminalState = True

    def selectTime(self, r1):
        self.dt = (1/self.totProp)*np.log(1/r1)
        self.t += self.dt

    def selectReaction(self, r2):
        reactionIdx = 0
        randVar = r2*self.totProp
        threshold = self.cumPropArray[reactionIdx]
        if randVar > threshold:
            while randVar > threshold:
                reactionIdx += 1
                threshold = self.cumPropArray[reactionIdx]
        self.reactionIdx = reactionIdx
        self.rType = self.reactionArray[self.reactionIdx].type

    def birth(self):
        for i in self.populationArray:
            if not i.isAlive:
                i.isAlive = True
                i.group = "J"
                i.age = 0
                self.N[0] += 1
                break

    def death(self):

        indivId = self.reactionArray[self.reactionIdx].indivId
        indiv = self.populationArray[indivId]

        if not indiv.isAlive:
            raise ValueError("Trying to kill an already dead individual.")

        indiv.isAlive = False
        if indiv.group == "J":
            self.N[0] += -1
        if indiv.group == "A":
            self.N[1] += -1

    def applyReaction(self):
        if self.rType == "Birth":
            self.birth()
        elif self.rType == "Death":
            self.death()

    def maturationProcess(self, cfg):

        juvenilesCount = 0
        maturatedCount = 0

        for i in range(cfg.maxIndividuals):
            indiv = self.populationArray[i]
            # For every alive juvenile:
            if indiv.isAlive:
                if indiv.group=="J":

                    # increase age
                    indiv.age += self.dt

                    # change group if maturation is reached
                    if indiv.age > cfg.tau:
                        indiv.group = "A"
                        maturatedCount += 1
                        # wait for updating the population numbers

                juvenilesCount += 1
                # when you made the maturation for all the juveniles, update the population numbers and break
                if juvenilesCount==self.N[0]:
                    self.N[0] += -maturatedCount
                    self.N[1] += maturatedCount
                    break

    def step(self, cfg):

        # Update propensities
        self.updatePropensities(cfg)

        # Draw time & reaction
        r1 = uniform()
        r2 = uniform()
        self.selectTime(r1)
        self.selectReaction(r2)

        self.maturationProcess(cfg)

        # Apply reaction
        self.applyReaction()

        if self.t > cfg.maxTime:
            self.isTerminalState = True

        if self.N[0]==0 and self.N[1]==0:
            self.isTerminalState = True
            self.terminalLog = "End of simulation: Extinction"

        if (self.N[0]+self.N[1])==cfg.maxIndividuals:
            self.isTerminalState = True
            self.terminalLog = "End of simulation: Max population"

    def simulate(self, cfg, debugLog=False, csv=False):

        while not self.isTerminalState:

            self.step(cfg)

            if debugLog:
                self.printDebug()
            elif csv:
                self.printCsvLine()

#            self.jHistory.append(self.N[0])
#            self.aHistory.append(self.N[1])
#            self.tHistory.append(self.t)

#        return self.tHistory, self.jHistory, self.aHistory

# Example of usage:
cfg = CFG()
gState = globalState(cfg)
gState.simulate(cfg, csv = True)

def pandasParseCsv(filename):
    # to parse data saved as csv

    df = pd.read_csv(filename, names=["t", "N"])

    df.t.apply(float)
    df.N.apply(int)

    t = df.t.to_numpy()
    N = df.N.to_numpy()

    return t, N
