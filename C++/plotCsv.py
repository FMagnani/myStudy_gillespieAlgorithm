import matplotlib.pyplot as plt
import numpy as np
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

t, n = pandasParseCsv("output.csv")

fig, ax = plt.subplots(1,1)
ax.plot(t, n, 'b', alpha=0.8)

def logistic(t):
    return N0*K/(N0+(K-N0)*pow(np.e, -r*t))

t = np.array(t)
ax.plot(t, logistic(t), 'r')

plt.show()
