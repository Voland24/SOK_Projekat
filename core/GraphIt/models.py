from django.db import models
import json
import datetime

class Graph:
    def __init__(self, directed=False):
        self.is_directed = directed
        self.neighbors_list = {}
        self.vertices_dict = {}

    def insert_vertex(self, vertex):
        id = vertex['id']
        if id not in self.vertices_dict:
            self.vertices_dict[id] = vertex
            self.neighbors_list[id] = []
    
    def insert_edge(self, vertex1, vertex2):
        id1 = vertex1['id']
        id2 = vertex2['id']
    
        self.insert_vertex(vertex1)
        self.insert_vertex(vertex2)

        self.neighbors_list[id1].append(id2)
        if not self.is_directed:
            self.neighbors_list[id2].append(id1)
    
    def vertices(self):
        """id of the vertex is key, the value is the vertes itself"""
        return self.vertices_dict

    def vertex_count(self):
        return len(self.vertices_dict)

    def are_adjacent(self, id1, id2):
        if id1 in self.vertices_dict and id2 in self.vertices_dict:
            return id2 in self.neighbors_list[id1]
        return False
    
    def get_adjacent(self, id):
        """returns a list of ids of the vertices that are adjacent to the one passed"""
        if id in self.vertices_dict:
            return self.neighbors_list[id]
        return None
    
    def edges(self):
        """
        Return a list of tuples, two values, where each element of the tuple
        is the vertex id
        """
        all_edges = []
        for vertex_id in self.vertices_dict:
            for adjacent in self.neighbors_list[vertex_id]:
                all_edges.append((self.vertices_dict[vertex_id], self.vertices_dict[adjacent]))
        return all_edges

    def edge_count(self):
        return len(self.edges())

    def degree(self, id):
        return len(self.get_adjacent(id))

    def from_dict(self, graph_dict):
        """
        Reads a graph from the dictionary
        """
        self.is_directed = graph_dict['is_directed']
        self.neighbors_list = graph_dict['neighbors_list']
        self.vertices_dict = graph_dict['vertices_dict']
    
    def is_cyclic(self, subgraph_vertices):
        visited = {key: False for key in subgraph_vertices}
        for key in visited.keys():
            if not visited[key]:
                if self._is_cyclic(key, visited, None):
                    return True
        return False
    
    def _is_cyclic(self, key, visited, parent):
        visited[key] = True

        for vertex in self.neighbors_list[key]:
            if vertex not in visited:
                return False
            if not visited[vertex]:
                if self._is_cyclic(vertex, visited, key):
                    return True
            elif parent != vertex:
                return True

        return False
    
    def get_first(self, subgraph_vertices):
        vertex = self.vertices_dict[subgraph_vertices[0]]
        name = vertex['name']
        id = vertex['id']
        linked_nodes = self.neighbors_list[id]
        return {'name': name, 'id': id, 'linked_nodes': linked_nodes, 'clicked': 'false'}
    
    def get_root(self, subgraph_vertices):
        for vertex_key in subgraph_vertices:
            in_count = 0
            for edge in self.edges():
                if edge[1] == vertex_key:
                    in_count += 1
            if in_count == 0:
                root = self.vertices_dict[vertex_key]
                name = root['name']
                id = root['id']
                linked_nodes = self.neighbors_list[id]
                return {'name': name, 'id': id, 'linked_nodes': linked_nodes, 'clicked': 'false'}
    
    def dfs_util(self, temp, v_key, visited):
        visited[v_key] = True

        temp.append(v_key)

        for neighbor_key in self.neighbors_list[v_key]:
            if not visited[neighbor_key]:
                temp = self.dfs_util(temp, neighbor_key, visited)

        return temp
    
    def get_connected_components(self):
        visited = {key: False for key in self.vertices_dict.keys()}
        cc = []

        for key in self.vertices_dict.keys():
            if not visited[key]:
                temp = []
                cc.append(self.dfs_util(temp, key, visited))

        return cc
    
    def get_tree(self):
        """
        Returns json string used for making the tree view
        """
        dict_graph = {}
        data = []
        roots = []
        for connected_component in self.get_connected_components():
            if not self.is_cyclic(connected_component) and not self.is_directed:
                roots.append(self.get_root(connected_component))
            else:
                roots.append(self.get_first(connected_component))
        for vertex in self.vertices_dict.values():
            name = vertex['name']
            id = vertex['id']
            linked_nodes = self.neighbors_list[id]
            data.append({'name': name, 'id': id, 'linked_nodes': linked_nodes, 'clicked': 'false'})
        dict_graph['data'] = data
        dict_graph['roots'] = roots
        return json.dumps(dict_graph, indent=4)
    

    def search(self, search_string: str):
        """Accepts a string, returns a Graph composed of nodes in which at least one of the attributes
        contains the string value."""
        results_graph = Graph()
        for vertex in self.vertices_dict.values():
            for value in vertex.values():
                if search_string.lower() in str(value).lower():
                    results_graph.insert_vertex(vertex)
                    break

        for vertex_id in results_graph.vertices_dict:
            vertex_edges = self.get_adjacent(vertex_id)
            for edge_id in vertex_edges:
                if edge_id in results_graph.vertices():
                    if not results_graph.neighbors_list[vertex_id]:
                        results_graph.neighbors_list[vertex_id] = []
                    results_graph.neighbors_list[vertex_id].append(edge_id)
        return results_graph
    
    def insert_vertex_for_filter(self, filter_attribute, filter_value, operation, filtered_graph):
        for vertex in self.vertices_dict.values():

            if filter_attribute not in vertex:
                continue

            vertex_value = vertex[filter_attribute]
            vertex_value_backup = vertex_value

            if isinstance(vertex_value, str):
                if vertex_value.isnumeric():
                    vertex_value = float(vertex_value)
                    if not isinstance(filter_value, float):
                        continue
                else:
                    try:
                        vertex_value = datetime.datetime.strptime(vertex_value, '%d-%m-%Y %H:%M:%S')
                        if not isinstance(filter_value, datetime.datetime):
                            continue
                    except:
                        vertex_value = vertex_value_backup
            elif isinstance(vertex_value, int):
                vertex_value = float(vertex_value)
                if not isinstance(filter_value, float):
                    continue

            elif type(filter_value) != type(vertex_value):
                filter_value = str(filter_value)
                vertex_value = str(vertex_value)

            if operation == "==":
                if filter_value == vertex_value:
                    filtered_graph.insert_vertex(vertex)
            elif operation == ">":
                if vertex_value > filter_value:
                    filtered_graph.insert_vertex(vertex)
            elif operation == ">=":
                if vertex_value >= filter_value:
                    filtered_graph.insert_vertex(vertex)
            elif operation == "<":
                if vertex_value < filter_value:
                    filtered_graph.insert_vertex(vertex)
            elif operation == "<=":
                if vertex_value <= filter_value:
                    filtered_graph.insert_vertex(vertex)
            elif operation == "!=":
                if filter_value != vertex_value:
                    filtered_graph.insert_vertex(vertex)
    
    def filter(self, filter_string: str):
        """Accepts a string in the 'attribute*value' format, where '*' represents one of the following:
        - <
        - <=
        - ==
        - !=
        - >
        - >=
        The function then returns a Graph composed of nodes in which the chosen attribute matches the value specified in
        the string. If there are no matching nodes, the function returns an empty Graph.
        """
        filtered_graph = Graph(self.is_directed)

        operation = ""
        while True:
            if filter_string.find('==') != -1:
                operation = '=='
                break
            elif filter_string.find('>=') != -1:
                operation = '>='
                break
            elif filter_string.find('<=') != -1:
                operation = '<='
                break
            elif filter_string.find('!=') != -1:
                operation = '!='
                break
            elif filter_string.find('>') != -1:
                operation = '>'
                break
            elif filter_string.find('<') != -1:
                operation = '<'
                break
            return filtered_graph

        filter_string_split = filter_string.split(operation)

        filter_attribute = filter_string_split[0]
        filter_value = filter_string_split[1]

        filter_value_backup = filter_value

        if filter_value.isnumeric():
            filter_value = float(filter_value)
        else:
            try:
                filter_value = datetime.datetime.strptime(filter_value, '%d-%m-%Y %H:%M:%S')
            except:
                filter_value = filter_value_backup

        self.insert_vertex_for_filter(filter_attribute, filter_value, operation, filtered_graph)

        for vertex_id in filtered_graph.vertices_dict:
            vertex_edges = self.get_adjacent(vertex_id)
            for adjacent_id in vertex_edges:
                if adjacent_id in filtered_graph.vertices():
                    if not filtered_graph.neighbors_list[vertex_id]:
                        filtered_graph.neighbors_list[vertex_id] = []
                    filtered_graph.neighbors_list[vertex_id].append(adjacent_id)
        return filtered_graph