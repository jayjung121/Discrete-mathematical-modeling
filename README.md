# Discrete-mathematical-modeling
This repository contains materials that create different classes, algorithm and equations that can be used to solve minisum location problem, specifically finding Optimum place to start donut shop in Seattle.

  The goal of this project is to determine the optimal location to open up a donut shop in Seattle. Our approach is to interpret easily obtained public data through the lens of a minisum location problem with some steps to reduce the computation cost via area restriction and simpliﬁed product demand. We extract an undirected node graph of Seattle from publicly available data and interpolate population in ZIP Code demarcated regions into node weights of intersections in the city. Once this is done we apply our minisum optimization to ﬁnd ideally situated locations built with the assumptions of our model. As a test of our model’s predictions of real world results we compare prediction vs actual location of donut shops in Seattle.

#### road.py
road.py is a python script that creates road.py class.

#### intersection.py
intersection.py is a python script that creates intersection class.

#### map.py
- map.py is python script which creates map class which contains both intersection and road classes.
- map class has real representation of intersection and road data.
- map.py extracts street data from Openstreetmap.

#### solution.py
- solution.py uses real map data from map.py to computes the optimal place to start donut shop in a given area. The default location is Seattle, but it can be modified to be used for other locations.
