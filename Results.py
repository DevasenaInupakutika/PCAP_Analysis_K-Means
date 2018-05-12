
# coding: utf-8

# In[ ]:

#Timing plots for sequential and parallel implementations
import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 40s intervals
t = np.arange(10., 210.,40)
print(t)
n = [2,3,4,5,6]

#Sequential timing
seq = [28.598, 35.767, 46.377, 81.865, 179.324]

#Parallel timing
parallel = [13.143, 14.639, 13.162, 26.927, 50.118]

#Speedup 
su = [2,2,3,3,3]
# red dashes, blue squares, green triangles
fig, ax = plt.subplots()
ax.plot(n,seq,"rs--", label="Sequential")
ax.plot(n,parallel,"bs--", label="Parallel MPI")
ax.plot(n, su, "g^--", label="Speedup")
plt.axis([2,6,0,210])

# Now add the legend with some customizations.
legend = ax.legend(loc='upper center', shadow=True)
plt.xlabel("Number of clusters/ processes for Parallel MPI")
plt.ylabel("Execution time (in seconds)")

plt.title("Performance plot:Sequential and Parallel Implementation of k-means")
plt.show()
