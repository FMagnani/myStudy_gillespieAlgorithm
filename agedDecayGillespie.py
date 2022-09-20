import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp


class State:
    def __init__(self, A0, D0, age0):
        self.A = A0
        self.D = D0
        self.age = age0

def mu(age):
    d = 0.03
    m = 2
    return (m*d)*pow((age*d), m-1)

def pdfWeibull(t):
    d = 0.03
    m = 2
    return (m*d)*pow((t*d), m-1)*pow(np.e, -pow(-d*t, m))

def cdfWeibull(t):
    d = 0.03
    m = 2
    return pow(np.e, -pow(-d*t, m))

def decayPropensity(state):
    return mu(state.age)*state.A

def nothingPropensity(state):
    return (1-mu(state.age))*state.A + state.D


def main():

#    t = np.linspace(0,100,50)
#    fig, ax = plt.subplots(1,1)
#    ax.plot(t, mu(t))

    # define model
    decayReaction = Reaction(
        name = "decay",
        propensity = decayPropensity,
        apply = lambda s: State(s.A-1, s.D+1, s.age+1)
    )
    nothingReaction = Reaction(
        name = "nothing",
        propensity = nothingPropensity,
        apply = lambda s: State(s.A, s.D, s.age+1)
    )

    model = GillespieModel([decayReaction, nothingReaction])

    # define Simulation
    maxTime = 4
    initState = State(1000, 0, 1)

    fig, ax = plt.subplots(1,2)

    # run some stochastic simluations
    for i in range(5):

        times, states, reactions, propensities = model.simulate(initState, maxTime, i)
        alives = np.array([s.A for s in states])
        ages = np.array([s.age for s in states])
        times = np.array(times)
        propensities = np.array(propensities)
        propensities = propensities[:,0]

        ax[0].plot(ages, alives/1000, 'k', alpha=0.5, label="Number of particles vs time")
        ax[1].plot(ages, propensities, 'r', alpha=0.5, label="Propensity of decay vs time")

        ax[0].legend()
        ax[1].legend()

    ax[0].plot(times, cdfWeibull(ages), 'r')

    plt.show()




if(__name__ == '__main__'):
    main()
