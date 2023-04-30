#!/usr/bin/env python

# configure
DIRECTORY = './subset'
PATTERN   = '*.rdf'
QUERY     = 'PREFIX crl:<https://distantreader.org/carrel#> SELECT * WHERE { ?s a crl:item . ?s crl:keyword ?o }'

# require
from   pathlib import Path
import networkx as nx
import rdflib
import sys

# initialize
graph     = rdflib.Graph()
directory = Path( DIRECTORY )

# process each file; merge rdf files into single graph
for file in directory.glob( PATTERN ) : graph = graph.parse( file, format='xml' )

# search the graph and process each result; create lists of nodes and edges
results = graph.query( QUERY )
nodes   = []
edges   = []
for result in results :
	
	# parse; very specific to the given query
	source = result[ 's' ].split( '/')[ -1 ].split( '#' )[ 1 ]
	target = result[ 'o' ]
	
	# update lists of nodes and edges
	nodes.append( ( source, { "type" : "item" } ) )
	nodes.append( ( target, { "type" : "keyword" } ) )
	edges.append( ( source, target ) )

# build the graph; very smart
graph = nx.Graph()
graph.add_nodes_from( nodes )
graph.add_edges_from( edges )

# output and done
nx.write_gml( graph, sys.stdout.buffer )
exit()

