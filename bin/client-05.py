#!/usr/bin/env python

# configure
ENDPOINT = 'http://localhost:3030/reader/sparql'
QUERY    = './etc/query.txt'

# require
from SPARQLWrapper import SPARQLWrapper2

# initialize
sparql = SPARQLWrapper2( ENDPOINT )
with open( QUERY ) as handle : sparql.setQuery( handle.read() )

# search and process each resulting row (binding)
bindings = sparql.query().bindings
for binding in bindings :

	s = binding[ "s" ].value.split( '/' )[ -1 ]
	o = binding[ "o" ].value
	print( '\t'.join( [ s, o ]) )