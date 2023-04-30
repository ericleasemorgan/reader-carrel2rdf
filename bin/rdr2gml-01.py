#!/usr/bin/env python

import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
import sys

url = 'results.rdf'

g = rdflib.Graph()
result = g.parse(url, format='xml')

G = rdflib_to_networkx_multidigraph(result)

# output and done
nx.write_gml( G, sys.stdout.buffer )
exit()
