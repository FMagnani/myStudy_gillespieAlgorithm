import matplotlib.pyplot as plt
import numpy as np
from logisticIndividual import CFG, globalState

r = 1
K = 100
N0 = 20
maxTime = 10
maxIndividuals = 500

cfg = CFG(r=r, K=K, N0=N0, maxTime=maxTime, maxIndividuals=maxIndividuals)

gState = globalState(cfg, seed=0)
t1, n1 = gState.simulate(cfg)

gState = globalState(cfg, seed=152)
t2, n2 = gState.simulate(cfg)

gState = globalState(cfg, seed=53)
t3, n3 = gState.simulate(cfg)

gState = globalState(cfg, seed=123)
t4, n4 = gState.simulate(cfg)

gState = globalState(cfg, seed=78945)
t5, n5 = gState.simulate(cfg)

fig, ax = plt.subplots(1,1)
ax.plot(t1, n1, 'b', alpha=0.8)
ax.plot(t2, n2, 'b', alpha=0.8)
ax.plot(t3, n3, 'b', alpha=0.8)
ax.plot(t4, n4, 'b', alpha=0.8)
ax.plot(t5, n5, 'b', alpha=0.8)

def logistic(t):
    return N0*K/(N0+(K-N0)*pow(np.e, -r*t))

t = np.array(t1)
ax.plot(t, logistic(t), 'r')

plt.show()
