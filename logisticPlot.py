import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1,1)

df = pd.read_csv("output1.csv", names=["t", "N"])
df.t.apply(float)
df.N.apply(int)
t = df.t.to_numpy()
N = df.N.to_numpy()
ax.plot(t, N, 'b', alpha=0.8)

df = pd.read_csv("output2.csv", names=["t", "N"])
df.t.apply(float)
df.N.apply(int)
t = df.t.to_numpy()
N = df.N.to_numpy()
ax.plot(t, N, 'b', alpha=0.8)

df = pd.read_csv("output3.csv", names=["t", "N"])
df.t.apply(float)
df.N.apply(int)
t = df.t.to_numpy()
N = df.N.to_numpy()
ax.plot(t, N, 'b', alpha=0.8)

r = 1
K = 100
N0 = 10
def logistic(t):
    return N0*K/(N0+(K-N0)*pow(np.e, -t))
ax.plot(t, logistic(t), 'r')

plt.show()
