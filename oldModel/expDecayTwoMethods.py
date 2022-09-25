import numpy as np
import matplotlib.pyplot as plt
from gillespieModel import Reaction, GillespieModel
from scipy.integrate import solve_ivp

class State1:
    def __init__(self, N0):
        "Number of particles define the state"
        self.N = N0

class State2:
    "Number of Alive and Decayed particles define the state"
    def __init__(self, A0, D0):
        self.A = A0
        self.D = D0

def main():
    # Define reactions
    rate = 0.5

    # Only one reaction for method 1
    decayReaction1 = Reaction(
        "decay",
        lambda s,t: s.N*rate,
        lambda s: State1(s.N-1)
    )

    # 2 reactions for method 2
    decayReaction2 = Reaction(
        "decay",
        lambda s,t: s.A*rate,
        lambda s: State2(s.A-1, s.D+1)
    )
    nothingReaction = Reaction(
        "nothing",
        lambda s,t: s.A*(1-rate) + s.D,
        lambda s: s
    )

    model1 = GillespieModel([decayReaction1])
    model2 = GillespieModel([decayReaction2, nothingReaction])

    # Define simulation conditions
    maxTime = 10
    initState1 = State1(1000)
    initState2 = State2(1000, 0)

    fig, ax = plt.subplots(1,2)

    for i in range(10):

        times, states, reactions, propensities = model1.simulate(initState1, maxTime, i)
        states = [s.N for s in states]
        propensities = np.array(propensities)

        ax[0].plot(times, states, 'r', alpha=0.5, label="Model1")
        ax[1].plot(times, propensities[:,0], 'r', alpha=0.5, label="Model1 propensity")

        times, states, reactions, propensities = model2.simulate(initState2, maxTime, i)
        states = [s.A for s in states]
        propensities = np.array(propensities)

        ax[0].plot(times, states, 'b', alpha=0.5, label="Model2")
        ax[1].plot(times, propensities[:,0], 'b', alpha=0.5, label="Model2 propensity")

    plt.show()

if(__name__ == '__main__'):
    main()
