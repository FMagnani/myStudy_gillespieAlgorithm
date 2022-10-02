import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pandasParseCsv(filename):
    # to parse data saved as csv

    df = pd.read_csv(filename, names=["t", "J", "A"])

    df.t.apply(float)
    df.J.apply(int)
    df.A.apply(int)

    t = df.t.to_numpy()
    J = df.J.to_numpy()
    A = df.A.to_numpy()

    return t, J, A

t, J, A = pandasParseCsv("blowflyVariant.csv")
t1, J1, A1 = pandasParseCsv("blowflyOutput.csv")


fig, ax = plt.subplots(2,1)
ax[0].plot(t, J, 'r', alpha=0.8, label = "Variant")
ax[0].plot(t, A, 'r', alpha=0.8)
ax[0].plot(t1, J1, 'b', alpha=0.8, label = "As the paper")
ax[0].plot(t1, A1, 'b', alpha=0.8)
ax[1].plot(t, A, 'r', alpha=0.8, label = "Variant")
ax[1].plot(t1, A1, 'b', alpha=0.8, label = "As the paper")
ax[0].legend()
ax[1].legend()

plt.show()
