#!/usr/bin/env python

# reconcile-authors.py - given the name of a Reader study carrel, output a somewhat reconciled set of author names

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May 5, 2023 - rooted in previous work


# configure
DICTIONARY = './etc/dictionary-authors.tsv'
PATTERN    = '*'
COLUMNS    = [ 'id', 'author', 'qnumber' ]

# require
from   glob import glob
import pandas as pd
import rdr
import sys

# get input and debut
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
carrel = sys.argv[ 1 ]

# debug
sys.stderr.write( 'Reconciling ' + carrel + '\n' )

# initialize
library = rdr.configuration( 'localLibrary' )
authors = library/carrel/( rdr.ETC )/( rdr.AUTHORS )
files   = glob( str( library/carrel/( rdr.BIB )/PATTERN ) )
with open( DICTIONARY ) as handle : definitions = handle.read().splitlines()

# create a dictionary of qnames; apropos, and there has got to be a more elegent way
qnames = {}
for definition in definitions :
	( qname, qnumber ) = definition.split( '\t' )
	qnames[ qname ]    = qnumber

# create a dataframe of all records (keywords) and process each; reconcile
reconciliations = []
records         = pd.concat( ( pd.read_csv( file, sep='\t' ) for file in files ) )
for index, record in records.iterrows() :

	# re-initialize
	qnumber = ''
	
	# parse
	id     = record[ 'id' ]
	author = record[ 'author' ]
	
	# get the qnumber, conditionally
	if author in qnames.keys() : qnumber = qnames[ author ]

	# update
	reconciliation = [ id, author, qnumber ]
	reconciliations.append( reconciliation )
		
# create a dataframe of reconciliations, output, and, done
reconciliations = pd.DataFrame( reconciliations, columns=COLUMNS )
with open( authors, 'w' ) as handle : handle.write( reconciliations.to_csv( sep='\t', index=False ) )
exit()
