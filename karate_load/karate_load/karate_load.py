from GraphIt.models import Graph
from GraphIt.services.services import DataSourceService
import os
import datetime
import json
import pandas as pd

class KarateLoader(DataSourceService):
    def identification(self):
        return 'karate_loader'

    def name(self):
        return 'Karate loader'


    #   C:/FAKS/MASTER/SOK/LukaExpressivnes/KarateDataset
    def load_data(self, resource: str) -> Graph:
        path_to_values = resource + 'KarateValues.json'
        path_to_neighbours = resource + 'neighbourList.pickle'

        g = Graph(directed=True)

        values_file = open(path_to_values)
        vertex_values = json.load(values_file)
        for v in vertex_values:
            v['name'] = v['First Name'] + ' ' + v['Last Name']
            v['id'] = str(v['id'])
        edges_dict = pd.read_pickle(path_to_neighbours)
        g = Graph(directed=True)
        for d in vertex_values:
            g.insert_vertex(d)

        for vertex_edge_pair in edges_dict.items():
            neighbour = vertex_edge_pair[1]
            for n in neighbour:
                g.insert_edge(vertex_values[vertex_edge_pair[0] - 1], vertex_values[n-1])

        
        print(g.edges())
                

        

        return g
    

