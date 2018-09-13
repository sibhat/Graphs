#!/usr/bin/python

"""
Demonstration of Graph and BokehGraph functionality.
"""

from draw import BokehGraph
from graph import Graph
from random import randint
from sys import argv
import random


def main(**kwargs):
    number_vertices = kwargs['num_verts']
    connected = kwargs['connected']
    number_edges = kwargs['num_edges']
    style = kwargs['style']
    if style == 'default':
        graph = default_graph()
    else:
        if number_vertices < 0 or number_edges < 0:
            raise ValueError("number must be greater than zero")
        elif number_edges > number_vertices * (number_vertices-1)/2:
            raise ValueError("max number of edges exceeded")
        graph = Graph()
        g = [graph.add_vertex(x) for x in range(number_vertices)]

        unique_edges = set()

        while(len(unique_edges) < number_edges):
            v1 = randint(0, number_vertices - 1)
            v2 = randint(0, number_vertices - 1)
            if v1 == v2:
                continue
            if (v2, v1) not in unique_edges:
                unique_edges.add((v1, v2))
                graph.add_edge(v1, v2)
        print('number of unique edges', len(unique_edges))

    # graph.bft(3)
    boka = BokehGraph(graph)
    if connected:
        color_connected(graph)
    boka.show()


def random_color():
    hexValues = ['0', '1', '2', '3', '4', '5', '6',
                 '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    colorString = "#A"
    for i in range(0, 3):
        colorString += hexValues[random.randint(0, len(hexValues) - 1)]
    return colorString


def color_connected(graph):
    for vertx in graph.vertices:
        color = random_color()
        # print(color)
        if graph.vertices[vertx].color == 'white':
            graph.vertices[vertx].color == color
            graph.bft(vertx, color)


def default_graph():
    graph = Graph()

    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)

    graph.add_vertex(7)
    graph.add_vertex(8)
    graph.add_vertex(9)

    graph.add_vertex(10)
    graph.add_vertex(11)

    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(2, 5)
    graph.add_edge(5, 6)
    graph.add_edge(3, 6)
    graph.add_edge(6, 1)
    # # graph.add_edge('0', '9')  # checking wrong index

    graph.add_edge(7, 8)
    graph.add_edge(7, 9)
    graph.add_edge(9, 8)

    graph.add_edge(10, 7)

    # print(graph.bft(1))
    print(graph.bft_path(3, 5))
    return graph


if __name__ == '__main__':

    style = "default"
    num_verts = 5
    num_edges = 6
    connected = False

    for arg in argv[1:]:
        arg_split = arg.split("=")
        if len(arg_split) == 2:
            if arg_split[0] == "style":
                style = arg_split[1].lower()
            elif arg_split[0] == "verts":
                num_verts = int(arg_split[1])
            elif arg_split[0] == "edges":
                num_edges = int(arg_split[1])
            elif arg_split[0] == "connected":
                connected = True

    main(style=style, num_verts=num_verts,
         num_edges=num_edges, connected=connected)
