import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State:
    def __init__(self, A0, D0):
        self.A = A0
        self.D = D0

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
    return mu(t)*state.A

def nothingPropensity(state, t):
    return (1-mu(t))*state.A + state.D


def main():

    # define model
    decayReaction = Reaction(
        name = "decay",
        propensity = decayPropensity,
        apply = lambda s: State(s.A-1, s.D+1)
    )
    nothingReaction = Reaction(
        name = "nothing",
        propensity = nothingPropensity,
        apply = lambda s: State(s.A, s.D)
    )

    model = GillespieModel([decayReaction, nothingReaction])

    # define Simulation
    maxTime = 50
    A0 = 1000
    initState = State(A0, 0)

    fig, ax = plt.subplots(1,2)

    # run some stochastic simluations
    for i in range(3):

        times, states, reactions, propensities = model.simulate(initState, maxTime, i)
        alives = np.array([s.A for s in states])
        times = np.array(times)
        propensities = np.array(propensities)
        propensities = propensities[:,0]

        ax[0].plot(times, alives, 'k', alpha=0.5, label="Number of particles vs time")
        ax[1].plot(times, propensities, 'k', alpha=0.5, label="Propensity of decay vs time")

        ax[0].legend()
        ax[1].legend()

    # deterministic
    ax[0].plot(times, A0*cdfWeibull(times), 'r', label="Weibull cdf * A0")
    ax[1].plot(times, A0*pdfWeibull(times), 'r', label="Weibull pdf * A0")

    plt.show()

if(__name__ == '__main__'):
    main()
