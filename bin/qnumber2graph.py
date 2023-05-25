#!/usr/bin/env python

# configure
TEMPLATE = './etc/qnumber2graph.rq'
FORMAT   = 'xml'

# require
import rdflib
import sys

# get input and debut
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <qnumber>" )
qnumber = sys.argv[ 1 ]

# initialize
graph = rdflib.Graph()
with open( TEMPLATE	) as handle: sparql = handle.read().replace( '##QNUMBER##', qnumber )

# do the work, output, and done
results = graph.query( sparql )
print( results.serialize( format=FORMAT ).decode() )
exit()