#!/usr/bin/env python

# configure
ENDPOINT = 'http://localhost:3030/reader/sparql'
QUERY    = './etc/query.txt'

# require
from SPARQLWrapper import SPARQLWrapper, JSON

# initialize
sparql = SPARQLWrapper( ENDPOINT )
sparql.setReturnFormat( JSON )

# read the query and search
with open( QUERY ) as handle : sparql.setQuery( handle.read() )
rows = sparql.queryAndConvert()

# proces each resulting row
for row in rows[ "results" ][ "bindings" ] :

	print( row )