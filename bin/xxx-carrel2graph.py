#!/usr/bin/env python

# configure
NAMESPACE = 'https://distantreader.org/carrel#'
PREFIX    = 'carrel'
FORMAT    = 'xml'
GRAPHROOT = 'http://distantreader.org/stacks/carrels/'
CREATOR   = { 'name':"Eric Lease Morgan", 'qnumber':'https://www.wikidata.org/wiki/Q102275801' }

# require
from rdflib           import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS, DCMITYPE, RDFS
import rdr
import pandas as pd
import json
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
studyCarrel = sys.argv[ 1 ]

# initialize
graph  = Graph()
CARREL = Namespace( NAMESPACE )
graph.bind( PREFIX, CARREL )

# denote a carrel and update the graph
carrel  = URIRef( GRAPHROOT + studyCarrel )
graph.add( ( carrel, RDF.type,        CARREL.carrel ) )
graph.add( ( carrel, RDF.type,        DCMITYPE.Dataset ) )
graph.add( ( carrel, RDF.type,        DCMITYPE.Collection ) )
graph.add( ( carrel, DCTERMS.title,   Literal( studyCarrel ) ) )

# add the carrel's creator (me)
qnumber = URIRef( CREATOR[ 'qnumber' ] )
graph.add( ( carrel, DCTERMS.creator, qnumber ) )
graph.add( ( qnumber, RDFS.label,     Literal( CREATOR[ 'name' ] ) ) )

# get provenance and extents...
dateCreated      = rdr.provenance( studyCarrel, 'dateCreated' )
process          = rdr.provenance( studyCarrel, 'process' )
totalSizeInItems = rdr.extents( studyCarrel,    'items' )
totalSizeInWords = rdr.extents( studyCarrel,    'words' )
averageFlesch    = rdr.extents( studyCarrel,    'flesch' )

# ...and update the graph
graph.add( ( carrel, DCTERMS.created,            Literal( dateCreated ) ) )
graph.add( ( carrel, CARREL.hasCreationProcess,  Literal( process ) ) )
graph.add( ( carrel, CARREL.hasTotalSizeInItems, Literal( totalSizeInItems ) ) )
graph.add( ( carrel, CARREL.hasTotalSizeInWords, Literal( totalSizeInWords ) ) )
graph.add( ( carrel, CARREL.hasAverageFlesch,    Literal( averageFlesch ) ) )

# for future reference, get keywords
keywords = ( rdr.configuration( 'localLibrary' ) )/studyCarrel/( rdr.ETC )/( rdr.WRDS )
if keywords.exists() : keywords = pd.read_csv( keywords, sep='\t' )
	
print( keywords )
exit()

# for future reference, get authors
authors = ( rdr.configuration( 'localLibrary' ) )/studyCarrel/( rdr.ETC )/( rdr.AUTHORS )
if authors.exists() : authors = pd.read_csv( authors, sep='\t' )

# get and process each bibliographic item
bibliographics = json.loads( rdr.bibliography( studyCarrel, format='json' ) )
for index, bibliographic in enumerate( bibliographics ) :
		
	# get the item's id and update the graph
	idItem = str( bibliographic[ 'id' ] )
	item   = URIRef( idItem )
	graph.add( ( carrel, DCTERMS.hasPart, item ) )
	
	# add author, conditionally
	if not authors.empty :

		# iterate over each author
		for _, author in authors.iterrows() :
			
			# update the graph, conditionally
			if str( author[ 'id' ] ) == idItem : graph.add( ( item, CARREL.hasAuthor, Literal( author[ 'author' ] ) ) )

	# add title
	graph.add( ( item, DCTERMS.title, Literal( bibliographic[ 'title' ] ) ) )

	# add date
	graph.add( ( item, DCTERMS.date, Literal( bibliographic[ 'date' ] ) ) )

	# add extents
	graph.add( ( item, CARREL.hasFlesch, Literal( int( bibliographic[ 'flesch' ] ) ) ) )
	graph.add( ( item, CARREL.hasSizeInWords, Literal( int( bibliographic[ 'words' ] ) ) ) )

	# add cache and plain text	
	cache = URIRef( GRAPHROOT + studyCarrel + '/' + ( rdr.CACHE ) + '/' + idItem + bibliographic[ 'extension' ] )
	text  = URIRef( GRAPHROOT + studyCarrel + '/' + ( rdr.TXT )   + '/' + idItem + '.txt' )
	graph.add( ( item,  CARREL.hasCache,     cache ) )
	graph.add( ( item,  CARREL.hasPlainText, text ) )
	graph.add( ( cache, DCTERMS.type,        Literal( bibliographic[ 'mime' ] ) ) )
	graph.add( ( text,  DCTERMS.type,        Literal( 'text/plain' ) ) )
	
	# process keywords, conditionally
	if not keywords.empty :
	
		# iterate over the keywords
		for _, keyword in keywords.iterrows() :
			
			# update the graph, conditionally
			if str( keyword[ 'id' ] ) == idItem : graph.add( ( item, CARREL.keyword, Literal( keyword[ 'keyword' ] ) ) )

# output and done
rdf = ( rdr.configuration( 'localLibrary' ) )/studyCarrel/( rdr.INDEXRDF )
with open( rdf, 'w' ) as handle : handle.write( graph.serialize( format=FORMAT ) )
exit()
