import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, individualGillespieModel
from scipy.integrate import solve_ivp

class State:
    def __init__(self, exist, t0, group=0):
        self.exist = exist
        self.t0 = t0
        self.group = 0

def mu(age):
    # pdf Weibull / 1- cdf Weibull
    d = 0.03
    m = 2
    return (m*d)*pow((age*d), m-1)

def decayPropensity(state, t):
    return mu(state.t0+t)

def cdfWeibull(t):
    # Actually 1 - cdf
    d = 0.03
    m = 2
    return pow(np.e, -pow(-d*t, m))


def main():

    # define model
    decayReaction = Reaction(
        name = "decay",
        propensity = decayPropensity,
        apply = lambda s: State(False, s.t0)
    )

    model = individualGillespieModel([decayReaction], 1)

    # define Simulation
    maxTime = 100
    N0 = 5000
    initState = [State(True, 0) for _ in range(N0)]

    fig, ax = plt.subplots(1,1)

    # run some stochastic simluations
    for _ in range(4):

        times, population = model.simulate(initState, maxTime, initTime=1)
        population = np.array(population)[:,0]
        times = np.array(times)

        ax.plot(times, population, 'k', alpha=0.7)
        ax.set_title("Number of particles vs time")

    # deterministic
    ax.plot(times, N0*cdfWeibull(times), 'r', label="N0*Weibull cdf")
    ax.legend()

    plt.show()

if(__name__ == '__main__'):
    main()
