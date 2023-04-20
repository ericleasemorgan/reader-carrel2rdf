#!/usr/bin/env python

# wrd2reconcile.py - given the name of a Reader study carrel, output a somewhat reconciled set of keywords

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# March 29, 2023 - on a whim


# configure
DICTIONARY = './etc/dictionary.tsv'
PATTERN    = '*'
COLUMNS    = [ 'id', 'keyword', 'qnumber' ]

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
wrds    = library/carrel/( rdr.ETC )/( rdr.WRDS )
files   = glob( str( library/carrel/( rdr.WRD )/PATTERN ) )
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
	id      = record[ 'id' ]
	keyword = record[ 'keyword' ]
	
	# get the qnumber, conditionally
	if keyword in qnames.keys() : qnumber = qnames[ keyword ]

	# update
	reconciliation = [ id, keyword, qnumber ]
	reconciliations.append( reconciliation )
		
# create a dataframe of reconciliations, output, and, done
reconciliations = pd.DataFrame( reconciliations, columns=COLUMNS )
with open( wrds, 'w' ) as handle : handle.write( reconciliations.to_csv( sep='\t', index=False ) )
exit()
