#!/usr/bin/env python

# configure
TEMPLATE = './etc/qnumber2graph.rq'
FORMAT   = 'xml'

# require
import rdflib
import sys
import rdr
import pandas as pd

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
carrel = sys.argv[ 1 ]

# initialize
graph = rdflib.Graph()
with open( TEMPLATE	) as handle: template = handle.read()

# get all subjects
subjects = ( rdr.configuration( 'localLibrary' ) )/carrel/( rdr.ETC )/( rdr.WRDS )
if subjects.exists() :

	subjects = pd.read_csv( subjects, sep='\t' )
	subjects = subjects[ subjects[ 'qnumber' ].notnull() ]
	subjects = sorted( set( subjects[ 'qnumber' ].tolist() ) )

# get all authors
authors = ( rdr.configuration( 'localLibrary' ) )/carrel/( rdr.ETC )/( rdr.AUTHORS )
if authors.exists() :

	authors = pd.read_csv( authors, sep='\t' )
	authors = authors[ authors[ 'qnumber' ].notnull() ]
	authors = sorted( set( authors[ 'qnumber' ].tolist() ) )

# consolidate subjects and authors into qnumbers
qnumbers = sorted( set( subjects + authors ) )

# process each qnumber
for index, qnumber in enumerate( qnumbers ) :

	# debug and re-initialize
	sys.stderr.write( qnumber + '\n')
	results = rdflib.Graph()
	
	# build the query, search, get rdf, and update; tricky
	rdf = results.query( template.replace( '##QNUMBER##', qnumber ) ).serialize( format=FORMAT ).decode()
	graph.parse( data=rdf, format=FORMAT )
	
# output and done
print( graph.serialize( format=FORMAT ) )
exit()
