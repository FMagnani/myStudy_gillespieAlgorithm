import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State:
    def __init__(self, N0):
        self.N = N0

def isTerminalState(state):
    return state.N == 1

def mu(t):
    # pdf Weibull / 1- cdf Weibull
    d = 0.03
    m = 2
    return (m*d)*pow((t*d), m-1)

def pdfWeibull(t):
    d = 0.03
    m = 2
    return (m*d)*pow((t*d), m-1)*pow(np.e, -pow(-d*t, m))

def cdfWeibull(t):
    # Actually 1 - cdf
    d = 0.03
    m = 2
    return pow(np.e, -pow(-d*t, m))

def decayPropensity(state, t):
    return mu(t)*state.N


def main():

    # define model
    decayReaction = Reaction(
        name = "decay",
        propensity = decayPropensity,
        apply = lambda s: State(s.N-1)
    )

    model = GillespieModel([decayReaction], isTerminalState)

    # define Simulation
    maxTime = 100
    N0 = 10000
    initState = State(N0)

    fig, ax = plt.subplots(1,2)

    # run some stochastic simluations
    for _ in range(6):

        times, states, reactions, propensities = model.simulate(initState, maxTime, initTime=1)
        alives = np.array([s.N for s in states])
        times = np.array(times)
        propensities = np.array(propensities)
        propensities = propensities[:,0]

        ax[0].plot(times, alives, 'k', alpha=0.5)
        ax[1].plot(times, propensities, 'k', alpha=0.5)

        ax[0].set_title("Number of particles vs time")
        ax[1].set_title("Propensity of decay vs time")


    # deterministic
    ax[0].plot(times, N0*cdfWeibull(times), 'r', label="N0*Weibull cdf")
    ax[1].plot(times, N0*pdfWeibull(times), 'r', label="N0*Weibull pdf")
    ax[0].legend()
    ax[1].legend()

    plt.show()

if(__name__ == '__main__'):
    main()
