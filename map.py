# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 18:30:34 2018
Desc : This file creates Map class to be used for 
@author: ByungsuJung
"""
from intersection import Intersection
from road import Road
import requests
import osmnx as ox
import pandas as pd
import numpy as np
import random


class Map:
    
    # center_lat=47.608013, center_long=-122.335167, dist=1000
    
    def __init__(self,  center_lat=47.608013, center_long=-122.335167, dist=1000):
        center_pt = (center_lat, center_long)
        G = ox.graph_from_point(center_pt, distance=dist, network_type='drive')
        #G = ox.graph_from_place(place)
        self.G = G
        self.node_map = self.set_intersections(G) #dictionary of nodes
        self.edge_map = self.set_roads(G, self.node_map) #dictionary of edges
        
        
    def set_intersections(self, G):
        """
        Method: set_intersections

        Method Arguments:
        * G - The graph of a real section of the world that will be produced
              from using the osmnx package and the lat and lon provided by the
              user input.

        Output:
        * A dictionary of the nodes created will be returned, where each node id
          is their key.
        """ 
        node_dict = {}
        g_nodes = G.nodes()
        for n in g_nodes.keys():
            name = g_nodes[n]['osmid']
            x = g_nodes[n]['x'] # -122
            y = g_nodes[n]['y'] # 42
            zipcode = get_zip(y,x) #Insert point for zipcode data

            weight = get_pop(zipcode)
                
            node_to_insert = Intersection(name, x, y, weight, zipcode, self)
            if name in node_dict: #If the name's not in the dictionary, put the node in the dictionary
                #print("duplicate")
                pass
            else:
                node_dict[name] = node_to_insert #Insert Node
        return node_dict #Return full dictionary with data added. 
    
    def set_roads(self, G, node_dict):
        
        """
        Method: set_roads

        Method Arguments:
        * G - The graph of a real section of the world that will be produced
              from using the osmnx package and the lat and lon provided by the
              user input.

        * node_dict - The node dictionary that will be used to show which roads
                        are connected to each other.

        Output:
        * A dictionary of the edges created will be returned, where each edge id
          is their key.
        """ 
        
        edge_dict = {}
        id = 0
        for e in G.edges(data=True):
            start = node_dict[e[0]]
            destination = node_dict[e[1]]
            length = int(e[2]['length']) 
            #name = e[2]['name']
            edge_to_insert = Road(id, start, destination, length)
            if id in edge_dict: 
                print("duplicate edge")
            edge_dict[id] = edge_to_insert
            id+=1
        #removed bad edge
        return edge_dict
    
#########################################################################3
# This function takes zipcode as a parameter and return matching population in given zipcode.

def get_pop(zipcode):
    df = pd.read_csv("C:\\Users\\jbsoo\\Desktop\\JayJung\\UW\\Math 381\\Math381_final_project\\pop_by_zip.csv")
    x = df[df["Zip Code ZCTA"] == zipcode]['2010 Census Population']
    mean = np.mean(df['2010 Census Population'])
    # if failed to find zipcode from lat and long
    if zipcode == 99999:
        return(mean)
    # successfully received zipcode from lat and long
    if len(x) >= 1:
        x = int(x.values[0])
    # if no pop data for zipcode
    else:
        x = mean
    return(x)


def get_zip(lat, long):
    #latitude = 47.608013#lat
    #longitude = -122.335167#long
    # Did the geocoding request comes from a device with a
    # location sensor? Must be either true or false.
    sensor = 'true'

    # Hit Google's reverse geocoder directly
    # NOTE: I *think* their terms state that you're supposed to
    # use google maps if you use their api for anything.
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=lat,
        lon=long,
        sen=sensor
    )
    #print("Debug Format get_zip",base,params)
    url = "{base}{params}".format(base=base, params=params)
    #url = url + "&Key=AIzaSyCirOJRPBGCQ_UrF_r49FkPf14anlxRtTk"
    result = 99999
    while True:
        response = requests.get(url).json()
        if(response['status'] == 'OK'):
            street_data = response['results'][0]['address_components']
            for i in street_data:
                if i['types'] == ['postal_code']:
                    result = int(i['long_name'])
                    break
        break
            #length = len(street_data) - 1
            #result = street_data[length]['long_name']
            
    return(result)   




        