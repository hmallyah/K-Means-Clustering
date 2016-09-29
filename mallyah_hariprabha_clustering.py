import os
import sys
import string
import math
import copy
import random
import operator

k = 0
iterations = 0
data_file = []
initial_points = []
point_len = 0
clusters = {}
temp = {}
clusternames = []
formatted_clusters = []

k = int(sys.argv[2])
iterations = int(sys.argv[3])
#print k ,iterations

with open(sys.argv[1]) as inputfile1:
    for line in inputfile1:
        line = line.strip('\n')
        if line != '':
            line = line.split(',')
            data_file.append(line)
with open(sys.argv[4]) as inputfile2:
    for line in inputfile2:
        line = line.strip('\n')
        if line != '':
            line = line.split(',')
            initial_points.append(line)
if len(initial_points) != k:
    print "Number of Initial Points are not equal to k"
else:
    point_len = len(data_file[0])
    for point in data_file:
        for i in range(0, point_len - 1):
            point[i] = float(point[i])
    for point in initial_points:
        for i in range(0, point_len - 1):
            point[i] = float(point[i])
    #print data_file, initial_points

    def euclidean_distance(point1 = [], point2 = []):
        sumsq = 0
        sumsqsqrt = 0
        for i in range(0, point_len - 1):
            sumsq += (point1[i] - point2[i]) ** 2
        sumsqsqrt = math.sqrt(sumsq)
        return sumsqsqrt

    def get_centroid(points = []):
        centroid = []
        if len(points) == 1:
            centroid = points[0]
        else:
            for i in range(0, point_len - 1):
                sum = 0
                avg = 0
                for j in range(0, len(points)):
                    sum += points[j][i]
                avg = float(sum/len(points))
                centroid.append(avg)
            centroid.append('')
        return centroid

    def k_means(k, iterations, data_file = [], initial_points = []):
        clusters = {}
        centroids = copy.deepcopy(initial_points)

        for iteration in range(0, iterations):
            for i in range(0, k):
                clusters[i] = []
                clusters[i].append(centroids[i])

            for d in range(0, len(data_file)):
                min_dist_from_centroid = 100000000
                nearest_centroid_cluster_id = 0
                for j in range(0, k):
                    dist_from_centroid = euclidean_distance(data_file[d], centroids[j])
                    if dist_from_centroid < min_dist_from_centroid:
                        min_dist_from_centroid = dist_from_centroid
                        nearest_centroid_cluster_id = j
                clusters[nearest_centroid_cluster_id].append(data_file[d])

            centroids = []
            for cid in clusters:
                centroids.append(get_centroid(clusters[cid]))

        for c in clusters:
            for point in clusters[c]:
                if point not in initial_points:
                    if point not in data_file:
                        clusters[c].remove(point)

        return clusters

    clusters = k_means(k, iterations, data_file, initial_points)

    for c in clusters:
        clusters[c].sort(key = lambda x: x[point_len-1])

    def get_clusternames(clusters = {}):
        global clusternames
        for cluster in clusters:
            for point in clusters[cluster]:
                if point[point_len-1] not in clusternames:
                    temp[point[point_len-1]] = 0
        for c in range(0, len(clusters)):
            hashtable = copy.deepcopy(temp)
            for point in clusters[c]:
                key = point[point_len-1]
                hashtable[key] += 1
            formatted_clusters.append(max(hashtable.iteritems(), key = operator.itemgetter(1))[0])  ##### converted fc to list from dict
        #clusternames = formatted_clusters.keys()
        #clusternames.sort()

    get_clusternames(clusters)

    def erroneous_assignment(formatted_clusters = [], clusters = {}):
        errors = 0
        for fc in range(len(clusters)):
            for point in clusters[fc]:
                if point[point_len-1] != formatted_clusters[fc]:
                    errors += 1
        return errors

    def print_output(clusters = {}, formatted_clusters = []):
        for i in range(len(formatted_clusters)):
            print "Cluster " + str(formatted_clusters[i])
            for point in clusters[i]:
                print point
            print '\n'
        print "Number of points assigned to wrong cluster:"
        print erroneous_assignment(formatted_clusters, clusters)

    print_output(clusters, formatted_clusters)
