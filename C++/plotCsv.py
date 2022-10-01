import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pandasParseCsv(filename):
    # to parse data saved as csv

    df = pd.read_csv(filename, names=["t", "S", "G", "N"])

    df.t.apply(float)
    df.S.apply(int)
    df.G.apply(int)
    df.N.apply(int)

    t = df.t.to_numpy()
    S = df.S.to_numpy()
    G = df.G.to_numpy()
    N = df.N.to_numpy()

    return t, S, G, N

t, S, G, N = pandasParseCsv("epidermalOutput.csv")

fig, ax = plt.subplots(2,1)
ax[0].plot(t, S, 'r', alpha=0.8)
ax[0].plot(t, G, 'g', alpha=0.8)
ax[0].plot(t, N, 'b', alpha=0.8)
ax[1].plot(t, N, 'b', alpha=1)

plt.show()
