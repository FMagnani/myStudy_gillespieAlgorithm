import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State:
    def __init__(self, Pred, Prey):
        self.Pred = Pred
        self.Prey = Prey

def isTerminalState(state):
    return (state.Pred == 1 or state.Prey == 1)

def main():

    birth = Reaction(
        "preyBirth",
        lambda s,t: 1*s.Prey,
        lambda s: State(s.Pred, s.Prey+1)
    )
    eat = Reaction(
        "preyEaten",
        lambda s,t: 0.001*s.Prey*s.Pred,
        lambda s: State(s.Pred+1, s.Prey-1)
    )
    deathPred = Reaction(
        "predDeath",
        lambda s,t: 1*s.Pred,
        lambda s: State(s.Pred-1, s.Prey)
    )
    deathPrey = Reaction(
        "preyDeath",
        lambda s,t: 0.5*s.Prey,
        lambda s: State(s.Pred, s.Prey-1)
    )

    # Define simulation conditions
    maxTime = 30
    initState = State(1000, 1000)

#    nSimulations = 1
#    figArray = []

    # run some stochastic simluations
    for _ in range(2):

        fig, ax = plt.subplots(2,1)
        model = GillespieModel([birth, eat, deathPred, deathPrey], isTerminalState)

        times, states, reactions, propensities = model.simulate(initState, maxTime)
        preys = [s.Prey for s in states]
        preds = [s.Pred for s in states]
        propensities = np.array(propensities)

        ax[0].plot(times, preys, 'b', markersize=1.5, alpha=0.7, label="Preys")
        ax[0].plot(times, preds, 'r', alpha=0.7, label="Predators")
        ax[1].plot(times, propensities[:,0], 'b', alpha=0.7, label="Prey birth")
        ax[1].plot(times, propensities[:,1], 'r', alpha=0.7, label="Prey eaten")
        ax[1].plot(times, propensities[:,2], 'k', alpha=0.7, label="Predator death")
        ax[1].plot(times, propensities[:,3], 'g', alpha=0.7, label="Prey death")

        ax[0].legend()
        ax[1].legend()

#    preys = np.array(preys)
#    print(preys[1:]-preys[:-1])
#    preds = np.array(preys)
#    print(preds[1:]-preds[:-1])

#    ax[0,0].set_title("Number of particles vs time")
#    ax[0,1].set_title("Number of particles vs time")
#    ax[1,0].set_title("Propensity of decay vs time")
#    ax[1,1].set_title("Propensity of decay vs time")

    fig2, ax = plt.subplots(2,1)

    times = np.array(times)
    timeIntervals = times[1:] - times[:-1]
    ax[0].plot(timeIntervals, 'k')
    ax[1].plot(times, 'k', linewidth=2)
    ax[0].set_title("Time intervals along iterations")
    ax[1].set_title("(Flow of) Time along iterations")

    plt.show()

if(__name__ == '__main__'):
    main()
