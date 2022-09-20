import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

def main():
    # Define reactions
    rate = 0.5

    decayReaction = Reaction("decay", [-1,+1], lambda s: s[0]*rate)
    nothingReaction = Reaction("nothing", [0,0], lambda s: s[0]*(1-rate) + s[1])
    groupNames = ["Alive", "Decayed"]

    # Define simulation conditions
    maxTime = 10
    n0 = 1000

    fig, ax = plt.subplots(2,2)

    # run some stochastic simluations
    for i in range(5):
        model = GillespieModel([decayReaction, nothingReaction], groupNames)

        times, states, reactions, propensities = model.simulate([n0,0], maxTime, i)
        states = np.array(states)
        propensities = np.array(propensities)

        ax[0,0].scatter(times, states[:,0], color='black', alpha=0.7, s=1.5, label="Number of particles vs time")
        ax[0,1].plot(times, states[:,0], 'k', alpha=0.5, label="Number of particles vs time")
        ax[1,1].plot(times, propensities[:,0], 'b', alpha=0.5, label="Propensity of decay vs time")
        ax[1,0].scatter(times, propensities[:,0], color='blue', alpha=0.7, s=1.5, label="Propensity of decay vs time")

    ax[0,0].legend()
    ax[0,1].legend()
    ax[1,0].legend()
    ax[1,1].legend()

    # deterministic solution
    tEval = np.linspace(0,maxTime, len(times))
    tInt = [0,maxTime]
    n0 = np.array([n0])
    def expDecay(t, y):
        return -rate*y
    sol = solve_ivp(expDecay, tInt, n0, t_eval=tEval)
    ax[0,0].scatter(tEval, sol.y[0], color='r', s=1)
    ax[0,1].plot(tEval, sol.y[0], 'r')

    plt.show()

if(__name__ == '__main__'):
    main()
