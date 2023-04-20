#!/usr/bin/env python

# configure
DIRECTORY = './rdf'
PATTERN   = '*.rdf'
FORMAT    = 'xml'

QUERY     = "SELECT ?o ( COUNT( ?o ) AS ?c ) WHERE { ?s terms:subject ?o . } GROUP BY ?o ORDER BY DESC( ?c )"
QUERY     = "SELECT ?o ( COUNT( ?o ) AS ?c ) WHERE { ?s crl:keyword   ?o . } GROUP BY ?o ORDER BY DESC( ?c )"
QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s terms:subject ?o . }"
QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s terms:hasPart ?o . }"
QUERY     = "SELECT DISTINCT ?s ?p ?o WHERE { ?s crl:keyword   ?o . }"
QUERY     = "SELECT ?i ?a ?t ?d WHERE { ?i terms:creator ?a. ?i terms:title ?t. ?i terms:created ?d. }"

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

	i = result.i
	a = result.a
	t = result.t
	d = result.d
	
	print( '\t'.join( [ i, a, t, d ] ) )

# done	
exit()
