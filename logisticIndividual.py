from numpy.random import uniform
import numpy as np

class CFG:
    def __init__(self):
        self.r = 1
        self.K = 100
        self.nReactions = 2
        self.maxIndividuals = 10000
        self.maxReactions = self.maxIndividuals*self.nReactions
        self.N0 = 10

class globalState:
    def __init__(self, cfg):

        # Initialize populatoin array - with initial states
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
        self.updatePropensities(cfg)

        self.t = 0
        self.dt = 0
        self.reactionIdx = 0
        self.rType = ""


    def print(self, complete=False, csv=False):

        if complete:
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

            print("\nN: ",self.N, " totP: ", self.totProp)
            print(log)

        elif csv:
            print(str(self.t)+','+str(self.N))

#        else:
#            print("t: "+str(self.t)[:7]+" N: ", self.N)


    def updateIndividualPropensities(self, cfg):
        # Each individual computes its own propensities
        # Stop when all the living individual have been found
        aliveCount = 0
        for i in self.populationArray:
            i.iBasedReaction(cfg, self.N)
            if i.isAlive:
                aliveCount += 1
                if aliveCount==self.N:
                    break

    def updateReactionArray(self, cfg):
        # The global array of reactions is updated by the propensities computed by the individuals
        # It's better if the indivuals directly update this array on their own
        for i in range(self.N):
            for j in range(cfg.nReactions):
                self.reactionArray[cfg.nReactions*i+j].propIncrement = self.populationArray[i].reactionProps[j]

    def updateCumulativeProp(self, cfg):
        # Here we fill the cumulative propensity array
        # Actually, also this could be done directly by the indivduals
        totProp = 0
        aliveCount = 0
        self.cumPropArray = [0 for _ in self.reactionArray]
        for i in range(cfg.maxIndividuals):

            for j in range(cfg.nReactions):
                totProp += self.reactionArray[cfg.nReactions*i + j].propIncrement
                self.cumPropArray[cfg.nReactions*i + j] = totProp

            if self.populationArray[i].isAlive:
                aliveCount += 1
                if aliveCount==self.N:
                    break

        self.totProp = totProp

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


#    def updatePropensities(self, cfg):
#        self.updateIndividualPropensities(cfg)
#        self.updateReactionArray(cfg)
#        self.updateCumulativeProp(cfg)

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

        # Draw time & reaction
        r1 = uniform()
        r2 = uniform()
        self.selectTime(r1)
        self.selectReaction(r2)

        if self.N==1 and self.rType=="Death":
            raise ValueError("x_x Extinction x_x")

        # Apply reaction
        self.applyReaction()

        # Update propensities
        self.updatePropensities(cfg)

        self.print(csv=True)

class Individual:
    def __init__(self, id, isAlive=True):
        self.id = id
        self.isAlive = isAlive
#        self.reactionProps = [0,0]

#    def iBasedReaction(self, cfg, N):
#        if self.isAlive:
#            self.reactionProps[0] = cfg.r          # birth
#            self.reactionProps[1] = cfg.r*N/cfg.K  # death
#        else:
#            self.reactionProps[0] = 0
#            self.reactionProps[1] = 0

    def reactionRates(self, cfg, N):
        reactionProps = [0, 0]
        if self.isAlive:
            reactionProps[0] = cfg.r          # birth
            reactionProps[1] = cfg.r*N/cfg.K  # death

        return reactionProps



# better a struct - it has no methods
class Reaction:
    def __init__(self, indivId, type, propIncrement):
        self.indivId = indivId
        self.type = type
        self.propIncrement = propIncrement

cfg = CFG()
gState = globalState(cfg)

gState.print()
for _ in range(1000):
    gState.step(cfg)
