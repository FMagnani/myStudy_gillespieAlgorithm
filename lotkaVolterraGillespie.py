import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel

class State:
    def __init__(self, Pred, Prey):
        self.Pred = Pred
        self.Prey = Prey

def isTerminalState(state):
    return (state.Pred == 1 or state.Prey == 1)

def main():

    birth = Reaction(
        "preyBirth",
        lambda s,t: 10*1*s.Prey,
        lambda s: State(s.Pred, s.Prey+1)
    )
    eat = Reaction(
        "preyEaten",
        lambda s,t: 10*0.001*s.Prey*s.Pred,
        lambda s: State(s.Pred+1, s.Prey-1)
    )
    deathPred = Reaction(
        "predDeath",
        lambda s,t: 0.5*1*s.Pred,
        lambda s: State(s.Pred-1, s.Prey)
    )
    deathPrey = Reaction(
        "preyDeath",
        lambda s,t: 0*0.5*s.Prey,
        lambda s: State(s.Pred, s.Prey-1)
    )

    # Define simulation conditions
    maxTime = 5
    initState = State(50, 50)

    nSimulations = 2
    figSim, axSim = plt.subplots(nSimulations,1)
    figProp, axProp = plt.subplots(nSimulations,1)


    model = GillespieModel([birth, eat, deathPred, deathPrey], isTerminalState)

    # run some stochastic simluations
    for sim in range(nSimulations):

        times, states, reactions, propensities = model.simulate(initState, maxTime)
        preys = [s.Prey for s in states]
        preds = [s.Pred for s in states]
        propensities = np.array(propensities)

        axSim[sim].plot(times, preys, 'b', markersize=1.5, alpha=0.7, label="Preys")
        axSim[sim].plot(times, preds, 'r', alpha=0.7, label="Predators")
        axProp[sim].plot(times, propensities[:,0], 'b', alpha=0.7, label="Prey birth")
        axProp[sim].plot(times, propensities[:,1], 'r', alpha=0.7, label="Prey eaten")
        axProp[sim].plot(times, propensities[:,2], 'k', alpha=0.7, label="Predator death")
        axProp[sim].plot(times, propensities[:,3], 'g', alpha=0.7, label="Prey death")

        axSim[sim].legend()
        axProp[sim].legend()

        axSim[sim].set_title("Status vs time, simulation {}".format(sim))
        axProp[sim].set_title("Propensities vs time, simulation {}".format(sim))

    fig2, ax = plt.subplots(3,1)

    times = np.array(times)
    timeIntervals = times[1:] - times[:-1]
    ax[0].plot(timeIntervals, 'k')
    ax[1].plot(times, 'k', linewidth=2)
    ax[2].plot(np.sum(propensities, axis=1))
    ax[0].set_title("Time intervals along iterations")
    ax[1].set_title("(Flow of) Time along iterations")
    ax[2].set_title("Total propensity along iterations")
    ax[0].set_xticks([])
    ax[1].set_xticks([])
    fig2.suptitle("From last simulation")

    plt.show()

if(__name__ == '__main__'):
    main()
