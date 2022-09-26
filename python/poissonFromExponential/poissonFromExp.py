from scipy.stats import expon
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np
import random

# given the events and the time window, return the count of events in each window
# len(counts) == number of time windows
def countEvents(times, timeWindow):

    # Build the event line from the time intervals
    timeEvent = np.zeros(len(times))
    cumulativeTime = 0
    for i in range(len(times)):
        timeEvent[i] = cumulativeTime
        cumulativeTime += times[i]

    # Compute how many events happened in disjoint time windows
    nGroups = int(cumulativeTime/timeWindow)+1
    counts = np.zeros(nGroups)
    for i in range(nGroups):
        minTime = i*timeWindow
        maxTime = (i+1)*timeWindow

        mask = np.array([ int(minTime <= t <= maxTime) for t in timeEvent])
        counts[i] = np.sum(mask)

    return counts

# time window in which the counts are made
timeWindow = 1
# number of time windows to employ
drawsCount = 2000

# average interval of time between events
avgTime = 2
# the number of events needed to fill drawsCount windows of time
drawsTime = int(1.2* drawsCount*timeWindow/avgTime)
print("Generating "+str(drawsTime)+" events...")

# average events that will fall in each window
avgCounts = timeWindow/avgTime

# scale is the mean
times = expon(scale=avgTime).rvs(size=drawsTime)

counts = countEvents(times, timeWindow)

print("Window /avgTime: ", avgCounts)
print("Sample mean:", np.mean(counts))

# let's see if the distribution coincides with the poisson (we use same number of draws)
poissonDraws = poisson(avgCounts).rvs(drawsCount)

annotation = "Time window for counts: "+str(timeWindow)+"\n" +\
             "Average time interval: "+str(avgTime)+"\n" +\
             "Poisson parameter: "+str(avgCounts)[:5]+"\n" +\
             "Counts used for the histogram: "+str(drawsCount)

fig2, ax = plt.subplots(1,1)
ax.hist([counts, poissonDraws], density=True,
        color=['blue','red'], alpha=0.8,
        label=["Histogram of counts in each time window", "Poisson draws"])
ax.annotate(annotation, (0.6,0.6), xycoords="axes fraction")
ax.legend()

plt.show()
