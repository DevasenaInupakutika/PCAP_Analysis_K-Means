
# coding: utf-8

# In[ ]:

#Timing plots for sequential and parallel implementations
import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 40s intervals
n = [100,1000,10000,20000,50000,100000,5000000]

#Sequential timing
seq = [3.487,5.108,33.243,84.131,91.697,394.502,45650.588]

#Parallel timing
parallel = [0.168,1.167,13.811,29.267,46.197,168.076,15184.473]

# red dashes, blue squares
fig, ax = plt.subplots()
ax.plot(n,seq,"rs--", label="Sequential")
ax.plot(n,parallel,"bs--", label="Parallel MPI")
plt.axis([100,5000000,0,50000])

# Now add the legend with some customizations.
legend = ax.legend(loc='upper center', shadow=True)
plt.xlabel("Number of clusters/ processes for Parallel MPI")
plt.ylabel("Execution time (in seconds)")

plt.title("Performance plot:With Clusters Fixed to 3")
plt.show()
