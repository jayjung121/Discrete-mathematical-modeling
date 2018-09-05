# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 15:11:33 2018
Desc: This file creates map of given location and solve minisum location problem.
      In this problem, I focused on finding best spot to open Donut shop in Seattle. 
      However, this problem can be modified to be used for ther optimal location problem.
@author: ByungsuJung
"""


import matplotlib.pyplot as plt
from intersection import Intersection
import osmnx as ox
from map import Map
import matplotlib.pyplot as plt

# Location data
CENTER_LAT=47.608013
CENTER_LONG=-122.335167
CENTER_POINT = (CENTER_LAT, CENTER_LONG)
DISTANCE_FROM_CENTER = 1000 # Meters
DISTANCE_FROM_CENTER2 = DISTANCE_FROM_CENTER + 1000
# Competitors location data
COMPETITORS = [(47.662577,-122.37484),(47.62,-122.35),(47.6057,-122.3369),(47.610087,-122.32376),(47.668668,-122.375954),(47.608631,-122.34021),(47.668914,-122.3843),(47.628471,-122.360602),(47.603269,-122.33616),(47.613096,-122.31657),(47.616912,-122.33183),(47.616359,-122.345628),(47.578712,-122.41142),(47.585711,-122.33392)]


def drawMap(nodes,edges):
    """
    Method: drawMap

    Method Arguments:
    * nodes - List of nodes that will be draw on to the graph to help
              help visualize the follow of traffic.

    * edges - List of edges that will be draw on to the graph to help
              help visualize the follow of traffic.

    Output:
    * No return values, but the graph will be created in its initial state
      using the nodes and edges.
    """ 
    for key, node in nodes.items():
        if node == best_donutshop_place:
            ax.plot(node.x,node.y, marker = 'o', color = 'r', markersize = 20)
            ax.plot(node.x,node.y, marker = '+', color = 'b', markersize = 20)
        if node == second_best_donutshop_place:
            ax.plot(node.x,node.y, marker = 'o', color = 'b', markersize = 20)
            ax.plot(node.x,node.y, marker = '+', color = 'r', markersize = 20)
        if node in C:
            ax.plot(node.x,node.y, marker = 'o', color = 'g', markersize = 20)
        else:
            ax.plot(node.x,node.y, marker = 'o', color = 'b')
    for key, edge in edges.items():
        if type(edge.u) is int:
            u = nodes[str(edge.u)]
            v = nodes[str(edge.v)]
            ax.plot([u.x,v.x],[u.y,v.y], color = 'k')
        else:
            ax.plot([edge.u.x,edge.v.x],[edge.u.y,edge.v.y], color = 'k')


# Returns a list of all pairs (F(v),v) (sorted by decreasing F(v)) and prints
# the vertex v in V that minimizes F(v)
def solve():
    X = []
    count = 0
    for v in V:
        X.append((F(v),v))
        print(count)
        count+=1
        X.sort(key = lambda x:x[0])
    return X

# Objective function
def F(v):
    result = 0
    for u in V:
        result += pi(u,v)*weight[u]/(1 + d(u,v))
    return result

# Returns the proportion of customers retained from u
# for a facility at v
def pi(u,v):
    if u == v:
        return 1
    if u in C:
        return 0
    gammas = 1/d(u,v)
    for x in C:
        gammas += 1/d(u,x)
    return 1/d(u,v)/gammas

#Jay's Dijkstra
def dijkstra(s, V, E):
    R = set([s]) # list of intersections(nodes)
    l = {} # key = destination(v), value = shortest path length from s to v
    for e in E:
        e = E[e]
        if e.u == s:
            l[e.v] = e.length
        else:
            l[e.v] = float('inf')
    l[s] = 0
    V_set = set(list(V.values()))
    count = 0
    while R != V_set:
        count += 1
        X = V_set.difference(R)
        x = minimal(X,l)
        print(count)
        for y in X:
            if (x, y) in ee.keys():
                length = ee[(x,y)]
                l[y] = min(l[y], l[x] + length)
#        for e in E:
#            e = E[e]
#            if e.u == x:
#                l[e.v] = min(l[e.v], l[x] + e.length)
        R.add(x)
    return (l)


# Returns the shortest distance between vertices u and v
# using Dijkstra's algorithm
def d(u,v):
    if (u,v) in D:
        return D[(u,v)]
    if (v,u) in D:
        return D[(v,u)]
    l = {}
    R = set([v])
    for x in V:
        if (v,x) in E:
            l[x] = cost[(v,x)]
        elif (x,v) in E:
            l[x] = cost[(x,v)]
        else:
            l[x] = float('inf')
    l[v] = 0
    while R != V:
        X = V.difference(R)
        x = minimal(X,l)
        for y in X:
            if (x,y) in E:
                l[y] = min(l[y], l[x] + cost[(x,y)])
            elif (y,x) in E:
                l[y] = min(l[y], l[x] + cost[(y,x)])
        R.add(x)
    for x in V:
        D[x,v] = l[x]
    return l[u]

# Given a set of vertices X and a length map l, returns the
# vertex v in X that minimizes l[v]
def minimal(X, l):
    result = X.pop()
    X.add(result)
    for x in X:
        if l[x] < l[result]:
            result = x
    return result

###########################################################################
 
# Create a map
a_map = Map(center_lat=CENTER_LAT, center_long=CENTER_LONG, dist=DISTANCE_FROM_CENTER)

b_map = Map(center_lat=CENTER_LAT, center_long=CENTER_LONG, dist=DISTANCE_FROM_CENTER2)
# Calculate the number of intersection in each zipcodes conatained in the map
num_intersections = {}
for i in b_map.node_map.values():
    if i.zipcode in num_intersections.keys():
        x = num_intersections[i.zipcode]
        num_intersections[i.zipcode] = x + 1
    else:
        num_intersections[i.zipcode] = 1


D = {} # Cache for distances
edges = []
edge_and_length = {}
a = a_map.edge_map.values()
for e in a:
    edge = (e.u, e.v)
    length = e.length
    edges.append(edge)
    edge_and_length[edge] = length

E = set(edges) # Edges
cost = edge_and_length # Costs for d(u,v)

# Create iterable object for vertices
V1 = list(a_map.node_map.values())
V = set(V1) # V
# Set weights
weight = {} # Weight
for v in V1:
    weight[v] = (v.weight / num_intersections[v.zipcode])

# find score of competetors
def competitorsScore():
    min_list = []
    for i in COMPETITORS:
        temp_min_p = Intersection
        temp_min = 99999999
        for v in V:
            x = abs(v.y - i[0])
            y = abs(v.x - i[1])
            z = x+y
            if z < temp_min:
                temp_min_p = v
                temp_min = z
        min_list.append(temp_min_p) 
    return(min_list)
# set competitors   
C = set(competitorsScore())  

# solve the problem
Answer = solve()
best_donutshop_place = max(Answer)[1]
second_best_donutshop_place = Answer[len(Answer)-2][1]
# Create a blank figure
fig, ax = plt.subplots()
# Draw complete graph into the figure. Best donut place is indicated as red dot
drawMap(a_map.node_map, a_map.edge_map)


# Fr calculating mean
total = 0
for i in Answer:
    total += i[0]
mean = total / len(Answer)
print('Mean : ', mean)
    


for i in a_map.node_map.values():
    x = i.x
    y= i.y
    z = get_zip(y,x)
    print(z)













