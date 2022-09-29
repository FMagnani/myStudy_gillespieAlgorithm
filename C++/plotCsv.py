import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pandasParseCsv(filename):
    # to parse data saved as csv

    df = pd.read_csv(filename, names=["t", "nJ", "nA"])

    df.t.apply(float)
    df.nJ.apply(int)
    df.nA.apply(int)

    t = df.t.to_numpy()
    nJ = df.nJ.to_numpy()
    nA = df.nA.to_numpy()

    return t, nJ, nA

t, nJ, nA = pandasParseCsv("blowflyOutput.csv")

fig, ax = plt.subplots(2,1)
ax[0].plot(t, nJ, 'b', alpha=0.8)
ax[0].plot(t, nA, 'r', alpha=0.8)
ax[1].plot(t, nA, 'r', alpha=0.8)

plt.show()
