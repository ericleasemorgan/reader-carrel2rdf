#!/usr/bin/env python

# rdf2gml.py - transform a specifically shaped RDF/XML file into graph markup language (GML)

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May 2, 2023 - first cut, sort of


# configure
FORMAT  = 'xml'
TYPE    = 'type'
CARREL  = 'carrel'
SUBJECT = 'subject'
QUERY   = 'PREFIX carrel:<https://distantreader.org/carrel#> SELECT * WHERE { ?s carrel:about ?o }'

# require
import networkx
import rdflib
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <rdf/xml>" )
rdf = sys.argv[ 1 ]

# initialize
graph = rdflib.Graph()
graph = graph.parse( rdf, format=FORMAT )

# search the graph and process each result; create lists of nodes and edges
results = graph.query( QUERY )
nodes   = []
edges   = []
for result in results :
	
	# parse; very specific to the given rdf and query
	source = result[ 's' ].split( '/')[ -1 ]
	target = result[ 'o' ]
	
	# update lists of nodes and edges
	nodes.append( ( source, { TYPE : CARREL } ) )
	nodes.append( ( target, { TYPE : SUBJECT } ) )
	edges.append( ( source, target ) )

# build the graph; very smart
graph = networkx.Graph()
graph.add_nodes_from( nodes )
graph.add_edges_from( edges )

# output and done
nx.write_gml( graph, sys.stdout.buffer )
exit()

