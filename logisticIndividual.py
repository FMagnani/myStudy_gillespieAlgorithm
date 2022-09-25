from numpy.random import uniform
import numpy as np

class CFG:
    # Configuration
    # It holds model parameters, initial conditions, etc.
    def __init__(self):
        self.r = 1
        self.K = 100
        self.nReactions = 2
        self.maxIndividuals = 500
        self.N0 = 10
        self.maxTime = 2

class globalState:
    # The global state common to all the groups and individuals. All the algorithm is
    # managed by a single instance of this class.
    def __init__(self, cfg):

        # Initialize population array - with initial states
        self.N = cfg.N0
        self.populationArray = [Individual(i) for i in range(self.N)] + [Individual(i, isAlive=False) for i in range(cfg.maxIndividuals)[self.N:]]

        # Initialize reaction array - empty
        self.reactionArray = []
        for i in self.populationArray:
            reactionProps = i.reactionRates(cfg, self.N)
            self.reactionArray += [Reaction(i.id, "Birth", reactionProps[0]), Reaction(i.id, "Death", reactionProps[1])]

        # Initialize propensities array - empty
        self.cumPropArray = [0 for _ in self.reactionArray]
        self.totProp = 0

        # Update reaction and propensities
#        self.updatePropensities(cfg)

        self.t = 0
        self.dt = 0
        self.reactionIdx = 0
        self.rType = ""

        self.isTerminalState = False
        self.terminalLog = "End of simulation: max time"

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
                    log += "*"
                    if aliveCount==self.N:
                        break
                else:
                    log += "_"
        if self.isTerminalState:
            log = self.terminalLog

        print("t: "+str(self.t)[:6]+" N: "+str(self.N)+" "+log)

    def printCsvLine(self):
        # prints in csv format, so you can run simply:
        # "python script.py >> output.csv" from command line
        print(str(self.t)+','+str(self.N))

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
                if aliveCount==self.N:
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
                self.N += 1
                break

    def death(self):
        indivId = self.reactionArray[self.reactionIdx].indivId
        if not self.populationArray[indivId].isAlive:
            raise ValueError("Trying to kill an already dead individual.")
        self.populationArray[indivId].isAlive = False
        self.N += -1

    def applyReaction(self):
        if self.rType == "Birth":
            self.birth()
        elif self.rType == "Death":
            self.death()

    def step(self, cfg):

        # Update propensities
        self.updatePropensities(cfg)

        # Draw time & reaction
        r1 = uniform()
        r2 = uniform()
        self.selectTime(r1)
        self.selectReaction(r2)

        if self.t > cfg.maxTime:
            self.isTerminalState = True

        if self.N==1 and self.rType=="Death":
            self.isTerminalState = True
            self.terminalLog = "End of simulation: Extinction"

        if self.N==cfg.maxIndividuals-1:
            self.isTerminalState = True
            self.terminalLog = "End of simulation: Max population"

        # Apply reaction
        self.applyReaction()

    def simulate(self, cfg, debugLog=False):

        while not self.isTerminalState:

            self.step(cfg)

            if debugLog:
                self.printDebug()
            else:
                self.printCsvLine()

class Individual:
    def __init__(self, id, isAlive=True):
        self.id = id
        self.isAlive = isAlive

    def reactionRates(self, cfg, N):
        reactionProps = [0, 0]
        if self.isAlive:
            reactionProps[0] = cfg.r          # birth
            reactionProps[1] = cfg.r*N/cfg.K  # death

        return reactionProps

class Reaction:
    def __init__(self, indivId, type, propIncrement):
        self.indivId = indivId
        self.type = type
        self.propIncrement = propIncrement

cfg = CFG()
gState = globalState(cfg)
gState.simulate(cfg, debugLog = True)
