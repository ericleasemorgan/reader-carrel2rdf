#!/usr/bin/env python

# configure
ENDPOINT = 'http://localhost:3030/reader/sparql'
QUERY    = './etc/query.txt'

# require
from SPARQLWrapper import SPARQLWrapper2, XML

# initialize
sparql = SPARQLWrapper2( ENDPOINT )
with open( QUERY ) as handle : sparql.setQuery( handle.read() )


sparql.setReturnFormat(XML)
results = sparql.query().convert()
print(results.toxml())