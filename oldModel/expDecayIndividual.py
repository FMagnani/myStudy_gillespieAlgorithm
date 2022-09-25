import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, individualGillespieModel
from scipy.integrate import solve_ivp

class indState:
    def __init__(self, exist, group=0):
        self.exist = exist
        self.group = group

def indDecayPropensity(state, t):
    return 0.6*int(state.exist)

def main():
    rate = 0.6

    # define model
    decayReaction = Reaction(
        name = "decay",
        propensity = indDecayPropensity,
        apply = lambda s: indState(False)
    )

    model = individualGillespieModel([decayReaction], 1)

    # define Simulation
    maxTime = 12
    N0 = 1000

    fig, ax = plt.subplots(1,1)

    # run some stochastic simluations
    for _ in range(5):
        initState = [indState(True) for _ in range(N0)]

        times, nIndividuals = model.simulate(initState, maxTime, initTime=0)
        times = np.array(times)

        ax.plot(times, nIndividuals, 'k', alpha=0.5)
        ax.set_title("Number of particles vs time")

    # Deterministic
    tEval = np.linspace(0,maxTime, len(times))
    tInt = [0,maxTime]
    n0 = np.array([N0])
    def expDecay(t, y):
        return -rate*y
    sol = solve_ivp(expDecay, tInt, n0, t_eval=tEval)
    ax.plot(tEval, sol.y[0], 'r', alpha=0.8)

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
