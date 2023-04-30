#!/usr/bin/env python

# configure
ENDPOINT = 'http://localhost:3030/reader/sparql'
QUERY    = './etc/query.txt'

# require
from SPARQLWrapper import SPARQLWrapper, JSON


# initialize
sparql = SPARQLWrapper( ENDPOINT )
sparql.setReturnFormat( JSON )
with open( QUERY ) as handle : query = handle.read()
sparql.setQuery( query )


results = sparql.query().convert()

for result in results["results"]["bindings"] :
    print( result )