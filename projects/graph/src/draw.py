"""
General drawing methods for graphs using Bokeh.
"""
import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet, HoverTool, MultiLine, TapTool, BoxSelectTool,
                          ColumnDataSource, EdgesAndLinkedNodes, NodesAndLinkedEdges)
from bokeh.palettes import Spectral8, Spectral4
from graph import Graph


class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""

    def __init__(self, graph):
        self.graph = graph

    def show(self):

        node_indices = [
            self.graph.vertices[vertex].value for vertex in self.graph.vertices]
        # edge__start = [
        #     self.graph.vertices[vertex].value for vertex in self.graph.vertices]
        nodes__and__edges = [
            tuple((self.graph.vertices[vertex].value, self.graph.vertices[vertex].edges)) for vertex in self.graph.vertices]
        # print('\n vertes: ', edge__start)
        print('\n nodes__and__edges: ', nodes__and__edges)
        plot = figure(title="Graph Layout", x_range=(-1, 10),
                      y_range=(-1, 10))  # tools="pan,lasso_select,box_select,poly_select",

        graph = GraphRenderer()

        graph.node_renderer.data_source.add(node_indices, 'index')

        graph.node_renderer.data_source.add(
            [self.graph.vertices[vertex].color for vertex in self.graph.vertices], 'color')

        r = 30
        graph.node_renderer.glyph = Circle(
            size=r, fill_color='color')

        graph.node_renderer.selection_glyph = Circle(
            size=r, fill_color=Spectral4[2])   # make the shape of the node selectable
        graph.node_renderer.hover_glyph = Circle(
            size=r, fill_color=Spectral4[1])  # hover effect on node

        start_i = []
        end_i = []
        for vertex in self.graph.vertices:
            for end_point in self.graph.vertices[vertex].edges:
                start_i.append(vertex)
                end_i.append(end_point)

        graph.edge_renderer.data_source.data = dict(
            start=start_i, end=end_i)

        graph.edge_renderer.glyph = MultiLine(
            line_color="#CCCCCC", line_alpha=0.8, line_width=5)  # make the shape of the edge

        graph.edge_renderer.selection_glyph = MultiLine(
            line_color=Spectral4[2], line_width=5)  # make the shape of the edge selectable
        graph.edge_renderer.hover_glyph = MultiLine(
            line_color=Spectral4[1], line_width=5)  # hover effect on node

        x = [self.graph.vertices[vertex].x for vertex in self.graph.vertices]
        y = [self.graph.vertices[vertex].y for vertex in self.graph.vertices]

        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        # will cause the start and end nodes of an edge to also be inspected upon hovering an edge with the HoverTool
        graph.inspection_policy = EdgesAndLinkedNodes()
        # will cause a selected node to also select the associated edges
        graph.selection_policy = NodesAndLinkedEdges()

        plot.renderers.append(graph)

        labelSource = ColumnDataSource(data=dict(x=x, y=y, names=node_indices))
        labels = LabelSet(x='x', y='y', text='names', level='glyph',
                          text_align='center', text_baseline='middle', source=labelSource, render_mode='canvas')

        # calculate the ave distance, from starting_node (x, y) to ending node (x, y)
        w_x = [((self.graph.vertices[end_i[i]].x -
                 self.graph.vertices[start_i[i]].x) / 2) + self.graph.vertices[start_i[i]].x for (i, x) in enumerate(start_i)]
        w_y = [((self.graph.vertices[end_i[i]].y -
                 self.graph.vertices[start_i[i]].y) / 2) + self.graph.vertices[start_i[i]].y for (i, x) in enumerate(start_i)]
      # calculate wighted edge
        w_name = [abs(end_i[i] - start_i[i]) for (i, x) in enumerate(start_i)]

        weight_labelSource = ColumnDataSource(
            data=dict(x=w_x, y=w_y, names=w_name))
        weight_labels = LabelSet(x='x', y='y', text='names', text_color="red", level='glyph', text_align='center',
                                 text_baseline='middle', source=weight_labelSource, render_mode='canvas')

        plot.add_layout(labels)
        plot.add_layout(weight_labels)
        plot.add_tools(HoverTool(tooltips=None), TapTool(),
                       BoxSelectTool())  # add the hover

        output_file('graph.html')
        show(plot)
