#!/usr/bin/env python

# configure
DICTIONARY = './etc/dictionary.tsv'
ENDPOINT   = 'https://query.wikidata.org/sparql'
QUERY      = 'SELECT ?o WHERE { wd:##QNUMBER## schema:description ?o FILTER( LANG( ?o ) = "en" ) }'

# require
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

# initialize
dictionary = pd.read_csv( DICTIONARY, sep='\t' )
sparql     = SPARQLWrapper( ENDPOINT )
sparql.setReturnFormat( JSON )

# process each item in the dictionary; output definitions
for index, entry in dictionary.iterrows() :

	# parse
	qname   = entry[ 'qname' ]
	qnumber = entry[ 'qnumber' ]
	
	# create query and search
	sparql.setQuery( QUERY.replace( '##QNUMBER##', qnumber ) )
	bindings = sparql.queryAndConvert()
	
	# process the results
	for binding in bindings[ "results" ][ "bindings" ] : 
	
		# parse and output
		value = binding[ 'o' ][ 'value' ]
		print( '\t'.join( [ qname, value ] ) )
	
# done
exit()

	    