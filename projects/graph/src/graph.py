"""
Simple graph implementation compatible with BokehGraph class.
"""

import queue


class Vertices:
    def __init__(self, vertices_id, x=None, y=None, value=None, color="white"):
        self.id = int(vertices_id)
        self.x = x
        self.y = x
        self.value = value
        self.color = color
        self.edges = set()
        if self.x == None:
            self.x = 2 * (self.id // 3) + self.id / 10 * (self.id % 3)
        if self.y == None:
            self.y = 2 * (self.id % 3) + self.id / 10 * (self.id // 3)
        if self.value == None:
            self.value = self.id


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, node):
        self.vertices[node] = Vertices(node)
        return

    def add_edge(self, from_node, to_node):
        if self.vertices[from_node] != None and self.vertices[to_node] != None:
            self.vertices[from_node].edges.add(to_node)
            self.vertices[to_node].edges.add(from_node)
        else:
            raise IndexError("That vertex doesnt exist")
        return

    def add_directed_edge(self, from_node, to_node):
        if self.vertices[from_node] != None and self.vertices[to_node] != None:
            self.vertices[from_node].edges.add(to_node)
        else:
            raise IndexError("That vertex doesnt exist")
        return

    def dft(self, start):
        self.vertices[start].color = 'red'
        for child_node in self.vertices[start].edges:
            if self.vertices[child_node].color != 'red':
                self.dft(child_node)
        return [self.vertices[x].value for x in self.vertices]

    def bft(self, start, color="green"):
        # print('search initiated', color)
        q = queue.Queue()
        q.put(start)
        while(not q.empty()):
            node = q.get()
            if self.vertices[node].color != color:
                self.vertices[node].color = color
                for next_node in self.vertices[node].edges:
                    # if self.vertices[next_node].color != color:
                    q.put(next_node)

        # print('search finished')
        return [self.vertices[x].value for x in self.vertices]

    def dft_path(self, start, target, color="red", path=[]):
        self.vertices[start].color = color
        path = path + [start]
        if self.vertices[start].value == target:
            return path
        for child_vert in self.vertices[start].edges:
            if self.vertices[child_vert].color != color:
                new_path = self.dft_path(child_vert, target, color, path)
                if new_path:
                    return new_path
        return None

    def bft_path(self, start, target, color='blue'):
        q = queue.Queue()
        q.put([start])
        while(not q.empty()):
            path = q.get()
            node = path[-1]
            if self.vertices[node].color != color:
                if self.vertices[node].value == target:
                    return path
                self.vertices[node].color = color
                for next_node in self.vertices[node].edges:
                    if self.vertices[next_node].color != color:
                        new_path = list(path)
                        new_path.append(next_node)
                        q.put(new_path)

        return None

    def __str__(self):
        return f"Graph {self.vertices}"


# graph = Graph()

# graph.add_vertex('1')
# graph.add_vertex('2')
# graph.add_vertex('3')
# graph.add_vertex('4')
# graph.add_vertex('5')
# graph.add_vertex('6')

# graph.add_vertex('7')
# graph.add_vertex('8')
# graph.add_vertex('9')

# graph.add_vertex('10')
# graph.add_vertex('11')

# graph.add_directed_edge('1', '2')
# graph.add_directed_edge('1', '3')
# graph.add_directed_edge('2', '4')
# graph.add_directed_edge('2', '5')
# graph.add_directed_edge('5', '6')
# graph.add_directed_edge('3', '6')
# graph.add_directed_edge('6', '1')
# # # graph.add_edge('0', '9')  # checking wrong index

# graph.add_directed_edge('7', '8')
# graph.add_directed_edge('7', '9')
# graph.add_directed_edge('9', '8')

# graph.add_directed_edge('10', '7')

# print(graph.dft('1'))
