#!/usr/bin/env python

# configure
RDF = './rdf/emerson-works.rdf'

# require
from   pathlib import Path
from   rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import rdflib
import sys

# initialize
g = rdflib.Graph()
g = g.parse( RDF, format='xml' )

# convert to networkx graph, output, and done
G = rdflib_to_networkx_multidigraph( g )
nx.write_gml( G, sys.stdout.buffer )

