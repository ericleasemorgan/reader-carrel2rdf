#!/usr/bin/env python

# configure
DIRECTORY = './subset'
PATTERN   = '*.rdf'
OUTPUT    = 'gml'

# require
from   pathlib import Path
from   rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import rdflib
import sys

# initialize
g         = rdflib.Graph()
directory = Path( DIRECTORY )

# process each file; merge all into a graph
for file in directory.glob( PATTERN ) : g = g.parse( file, format='xml' )

if OUTPUT == 'gml' : 

	# convert to networkx graph, output, and done
	G = rdflib_to_networkx_multidigraph( g )
	nx.write_gml( G, sys.stdout.buffer )

elif OUTPUT == 'xml' : print( g.serialize( format="xml" ) )

else : sys.stderr.write( 'Unknown value for OUTPUT; call Eric.\n' )

