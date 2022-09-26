import matplotlib.pyplot as plt
import numpy as np
from logisticIndividual import CFG, globalState
import pandas as pd

def pandasParseCsv(filename):
    # to parse data saved as csv

    df = pd.read_csv(filename, names=["t", "N"])

    df.t.apply(float)
    df.N.apply(int)

    t = df.t.to_numpy()
    N = df.N.to_numpy()

    return t, N

r = 1
K = 30
N0 = 10
maxTime = 300
maxIndividuals = 35000

t1, n1 = pandasParseCsv("output.csv")

#cfg = CFG(r=r, K=K, N0=N0, maxTime=maxTime, maxIndividuals=maxIndividuals)

#gState = globalState(cfg, seed=0)
#t1, n1 = gState.simulate(cfg)

#gState = globalState(cfg, seed=152)
#t2, n2 = gState.simulate(cfg)

#gState = globalState(cfg, seed=53)
#t3, n3 = gState.simulate(cfg)

#gState = globalState(cfg, seed=123)
#t4, n4 = gState.simulate(cfg)

#gState = globalState(cfg, seed=78945)
#t5, n5 = gState.simulate(cfg)

fig, ax = plt.subplots(1,1)
ax.plot(t1, n1, 'b', alpha=0.8)
#ax.plot(t2, n2, 'b', alpha=0.8)
#ax.plot(t3, n3, 'b', alpha=0.8)
#ax.plot(t4, n4, 'b', alpha=0.8)
#ax.plot(t5, n5, 'b', alpha=0.8)

def logistic(t):
    return N0*K/(N0+(K-N0)*pow(np.e, -r*t))

t = np.array(t1)
ax.plot(t, logistic(t), 'r')

plt.show()
