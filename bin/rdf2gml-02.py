#!/usr/bin/env python

# configure
FORMAT = 'xml'

# require
import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <rdf/xml>" )
rdf = sys.argv[ 1 ]

# initialize
graph = rdflib.Graph()

# fill the graph and tranform it into a... graph
graph = graph.parse( rdf, format=FORMAT )
graph = rdflib_to_networkx_multidigraph( graph )

# output and done
nx.write_gml( graph, sys.stdout.buffer )
exit()
