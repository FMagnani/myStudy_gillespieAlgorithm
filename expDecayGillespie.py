import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State:
    "Number of Alive and Decayed particles define the state"
    def __init__(self, A0, D0):
        self.A = A0
        self.D = D0

def main():
    # Define reactions
    rate = 0.5

    decayReaction = Reaction(
        "decay",
        lambda s: s.A*rate,
        lambda s: State(s.A-1, s.D+1)
    )
    nothingReaction = Reaction(
        "nothing",
        lambda s: s.A*(1-rate) + s.D,
        lambda s: s
    )

    # Define simulation conditions
    maxTime = 10
    initState = State(1000, 0)

    fig, ax = plt.subplots(2,2)

    # run some stochastic simluations
    for i in range(5):
        model = GillespieModel([decayReaction, nothingReaction])

        times, states, reactions, propensities = model.simulate(initState, maxTime, i)
        states = [s.A for s in states]
        propensities = np.array(propensities)

        ax[0,0].scatter(times, states, color='black', alpha=0.7, s=1.5, label="Number of particles vs time")
        ax[0,1].plot(times, states, 'k', alpha=0.5, label="Number of particles vs time")
        ax[1,1].plot(times, propensities[:,0], 'b', alpha=0.5, label="Propensity of decay vs time")
        ax[1,0].scatter(times, propensities[:,0], color='blue', alpha=0.7, s=1.5, label="Propensity of decay vs time")

    ax[0,0].legend()
    ax[0,1].legend()
    ax[1,0].legend()
    ax[1,1].legend()

    # deterministic solution
    tEval = np.linspace(0,maxTime, len(times))
    tInt = [0,maxTime]
    n0 = np.array([initState.A])
    def expDecay(t, y):
        return -rate*y
    sol = solve_ivp(expDecay, tInt, n0, t_eval=tEval)
    ax[0,0].scatter(tEval, sol.y[0], color='r', s=1)
    ax[0,1].plot(tEval, sol.y[0], 'r')

    plt.show()

if(__name__ == '__main__'):
    main()
