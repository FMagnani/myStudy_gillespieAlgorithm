import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State:
    def __init__(self, N0):
        self.N = N0

def isTerminalState(state):
    return state.N == 1

def main():

    rate = 0.5
    decayReaction = Reaction(
        "decay",
        lambda s,t: s.N*rate,
        lambda s: State(s.N-1)
    )

    # Define simulation conditions
    maxTime = 10
    initState = State(1000)

    fig, ax = plt.subplots(2,2)

    # run some stochastic simluations
    for _ in range(10):
        model = GillespieModel([decayReaction], isTerminalState)

        times, states, reactions, propensities = model.simulate(initState, maxTime)
        states = [s.N for s in states]
        propensities = np.array(propensities)

        ax[0,0].scatter(times, states, color='black', alpha=0.7, s=1.5)
        ax[0,1].plot(times, states, 'k', alpha=0.5)
        ax[1,1].plot(times, propensities[:,0], 'k', alpha=0.5)
        ax[1,0].scatter(times, propensities[:,0], color='black', alpha=0.7, s=1.5)

    ax[0,0].set_title("Number of particles vs time")
    ax[0,1].set_title("Number of particles vs time")
    ax[1,0].set_title("Propensity of decay vs time")
    ax[1,1].set_title("Propensity of decay vs time")

    # deterministic solution
    tEval = np.linspace(0,maxTime, len(times))
    tInt = [0,maxTime]
    n0 = np.array([initState.N])
    def expDecay(t, y):
        return -rate*y
    sol = solve_ivp(expDecay, tInt, n0, t_eval=tEval)
    ax[0,0].scatter(tEval, sol.y[0], color='r', s=1, label="Deterministic", alpha=0.8)
    ax[0,1].plot(tEval, sol.y[0], 'r', alpha=0.8)
    ax[1,0].scatter(tEval, rate*sol.y[0], color='r', s=1, label="Deterministic", alpha=0.8)
    ax[1,1].plot(tEval, rate*sol.y[0], 'r', alpha=0.8)
    ax[0,0].legend()
    ax[1,0].legend()

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
