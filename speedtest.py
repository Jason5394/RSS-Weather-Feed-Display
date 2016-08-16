from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput

import weather_controller as wc

graphviz = GraphvizOutput(output_file='speed_test.png')

with PyCallGraph(output=graphviz):
    wc.main()