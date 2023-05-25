#!/usr/bin/env python

# graph2gml.py - given a specifically shaped RDF/XML file, output graph markup language (GML)

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May  2, 2023 - first cut, sort of; can probably be implemented sans the query
# May 17, 2023 - close to done, but software is never done; obsessive


# configure
FORMAT = 'xml'
CARREL = 'https://distantreader.org/carrel#'
WDP    = "http://www.wikidata.org/prop/direct/"

# require
from rdflib.namespace import DCTERMS, RDFS
import networkx
import rdflib
import rdr
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
studyCarrel = sys.argv[ 1 ]

# initialize
graph  = rdflib.Graph()
rdf    = ( rdr.configuration( 'localLibrary' ) )/studyCarrel/( rdr.INDEXRDF )
graph  = graph.parse( rdf, format=FORMAT )
CARREL = rdflib.Namespace( CARREL )
WDP    = rdflib.Namespace( WDP )
nodes  = []
edges  = []


# return the object of a given subject/predicate pair
def searchForObject ( suject, predicate ) :
	sparql = 'SELECT ?object WHERE { <' + str( suject ) + '> <' + predicate + '> ?object}'
	object = graph.query( sparql ).bindings[ 0 ][ 'object' ]
	return object
	
# return the English label of a given object
def searchForLabel ( object ) :
	sparql = 'SELECT ?label WHERE { <' + str( object ) + '> rdfs:label ?label . FILTER(LANG(?label) = "en")}'
	label  = graph.query( sparql ).bindings[ 0 ][ 'label' ]
	return label
	

# process all keywords
for subject, predicate, object in graph.triples( ( None, CARREL.keyword, None ) ) :
	
	# get the subject's corresponding title
	subject = searchForObject( subject, 'http://purl.org/dc/terms/title' )
		
	# update
	nodes.append( ( subject, { 'types' : 'item' } ) )
	nodes.append( ( object, { 'types' : 'keyword' } ) )
	edges.append( ( subject, object, { 'types' : 'keyword' } ) )

# process all subjects
for subject, predicate, object in graph.triples( ( None, DCTERMS.subject, None ) ) :
							
	# get the subject's title and the object's label
	subject = searchForObject( subject, 'http://purl.org/dc/terms/title' )
	object  = searchForLabel( object )
					
	# update
	nodes.append( ( subject, { 'types' : 'item' } ) )
	nodes.append( ( object, { 'types' : 'subject' } ) )
	edges.append( ( subject, object, { 'types' : 'subject' } ) )

# process all authors
for subject, predicate, object in graph.triples( ( None, CARREL.hasAuthor, None ) ) :
	
	# get the subject's corresponding title
	subject = searchForObject( subject, 'http://purl.org/dc/terms/title' )

	# update 
	nodes.append( ( subject, { 'types' : 'item' } ) )
	nodes.append( ( object, { 'types' : 'author' } ) )
	edges.append( ( subject, object, { 'types' : 'author' } ) )

# process all authors
for subject, predicate, object in graph.triples( ( None, DCTERMS.creator, None ) ) :
	
	# get the subject's corresponding title
	subject = searchForObject( subject, 'http://purl.org/dc/terms/title' )
	object  = searchForLabel( object )

	# update 
	nodes.append( ( subject, { 'types' : 'item' } ) )
	nodes.append( ( object, { 'types' : 'creator' } ) )
	edges.append( ( subject, object, { 'types' : 'creator' } ) )

# build the graph; very smart
graph = networkx.Graph()
graph.add_nodes_from( nodes )
graph.add_edges_from( edges )

# output and done
gml = ( rdr.configuration( 'localLibrary' ) )/studyCarrel/( rdr.ETC )/( rdr.GML )
networkx.write_gml( graph, gml )
exit()


