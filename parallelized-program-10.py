# coding: utf-8

# In[ ]:
#Import necessary modules
import csv, time, random, math
from mpi4py import MPI
import numpy
import matplotlib.pyplot as plt

#Setting colours for plots of clusters
color = ['red', 'green', 'blue','yellow','black','purple','pink']

#Data Assignment Step (Each data point is assigned to a cluster to its nearest centroid based on the squared Euclidean distance)
def eucl_distance(point_one, point_two):
    if(len(point_one) != len(point_two)):
        raise Exception("Error: non comparable points")

    sum_diff = 0.0
    for i in range(len(point_one)):
        diff = pow((float(point_one[i]) - float(point_two[i])), 2)
        sum_diff += diff
    final = math.sqrt(sum_diff)
    return final

#Centroid update step by taking the full mean of all data points assigned to that centroid's cluster
def compare_center(initial_center, derived_center, dimensions, num_clusters, cutoff):
    if(len(initial_center) != len(derived_center)):
        raise Exception("Error: non comparable points")

    flag = 0
    for i in xrange(num_clusters):
        diff = eucl_distance(initial_center[i], derived_center[i])
        if(diff < cutoff):
            flag += 1
    return flag


def main():
    #MPI Parallelization strategy initialization
    comm = MPI.COMM_WORLD #All processes together and a communicator object
    rank = comm.Get_rank() #Rank of a process in a communicator
    size = comm.Get_size() #Number of processes in a communicator
    print("Size is: ",size)
    global cutoff, dimensions, num_clusters, data, initial, min_dist
    cutoff = 0.2
    compare_val = 0
    with open('data/pcap_parallelshortfile.csv','rb') as f:
        reader = csv.reader(f)
        data = list(reader)
    data.pop(0)
    num_points = len(data)
    dimensions = len(data[0])
    initial = []
    for i in xrange(size):
        initial.append(data[i])
    start_time = time.time()
    #This will run until no data points change the clusters
    while True:
        # print "initial points",initial, rank
        # print ""
        dist = []
        min_dist = numpy.zeros(num_points)
        for point in data:
            dist.append(eucl_distance(initial[rank], point))

        temp_dist = numpy.array(dist)
        #Takes array of input data and outputs to the root process (Outputs contain the reduced element) with reduction operation as minimum value of the array of elements
        comm.Reduce(temp_dist, min_dist, op = MPI.MIN)
        #Blocks until all processes in the communicator have reached this routine
        comm.Barrier()
        if rank == 0:
            min_dist = min_dist.tolist()
       
        #Broadcast copying the same data from root process to all other processes in a communicator
        recv_min_dist = comm.bcast(min_dist, root = 0)
        comm.Barrier()
        cluster = []
        for i in xrange(len(recv_min_dist)):
            if recv_min_dist[i] == dist[i]:
                cluster.append(data[i])
        center = []
        center_val = [0] * dimensions
        for i in cluster:
            for j in xrange(dimensions):
                center_val[j] += float(i[j])

        for j in xrange(dimensions):
            if(len(cluster) != 0):
                center_val[j] = center_val[j] / len(cluster)
        #Gather data from all processes to the root process
        center = comm.gather(center_val, root = 0)
        comm.Barrier()
        if rank == 0:
            compare_val = compare_center(initial, center, dimensions,size, cutoff)
            if(compare_val == size):
                '''
                curX, curY = [], []
                for points in cluster:
                    curX.append(points[2])
                    curY.append(points[42])
                    plt.scatter(curX,curY,c=color[0])
                plt.xlabel("Protocol Type")
                plt.ylabel("Attack Type")
                plt.title("Clustering output")
                plt.show()
                '''
                print ("Final center: ", center)
                print ("Execution time %s seconds" % (time.time() - start_time))
        break_val = comm.bcast(compare_val, root = 0)

        initial = comm.bcast(center, root = 0)
        comm.Barrier()

        if break_val == size:
            break
            
    MPI.Finalize()



if __name__ == "__main__":
    main()

