#!/usr/bin/env python

# configure
DIRECTORY = './subset'
PATTERN   = '*.rdf'
FORMAT    = 'xml'

QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s terms:subject ?o . }"
QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s terms:hasPart ?o . }"
QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s crl:keyword   ?o . }"
QUERY     = "SELECT ?i ?a ?t ?d WHERE { ?i terms:creator ?a. ?i terms:title ?t. ?i terms:created ?d. }"
QUERY     = '''PREFIX terms: <http://purl.org/dc/terms/> SELECT ?s ?o WHERE { ?s terms:subject ?o } LIMIT 25'''
QUERY     = '''
PREFIX terms: <http://purl.org/dc/terms/>
SELECT ?subject ?object
WHERE {
  ?subject terms:subject ?object .
}'''
QUERY     = "SELECT ?s ?o WHERE { { ?s terms:subject ?o } UNION { ?s crl:keyword ?o . } }"
QUERY = '''PREFIX terms: <http://purl.org/dc/terms#>
PREFIX crl: <https://distantreader.org/carrel#>
SELECT *
WHERE {?s crl:keyword ?o }
LIMIT 51200'''

QUERY = '''PREFIX crl: <https://distantreader.org/carrel#>
SELECT *
WHERE {
  { ?s crl:keyword ?o } UNION { ?s terms:subject ?o }}'''


# require
from   pathlib import Path
import rdflib
import sys

# initialize
g         = rdflib.Graph()
directory = Path( DIRECTORY )

# process each file; merge all into a graph
for file in directory.glob( PATTERN ) : g = g.parse( file, format=FORMAT )

# search, output, and done
results = g.query( QUERY )
for result in results :

	s = result.s
	o = result.o
	print( '\t'.join([ s, o ]) )

# done	
exit()
