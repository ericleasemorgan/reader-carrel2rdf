#!/usr/bin/env python

# update-dictionary.py - given a carrel, update the dictionary are qnames and their qnumbers

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# March 30, 2023 - whirrr!


# configure
DICTIONARY = './etc/dictionary.tsv'
COLUMNS    = [ 'id' ]
MAP        = { 'keyword':'qname' }

# require
import pandas as pd
import rdr
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
carrel = sys.argv[ 1 ]

# initialize
library    = rdr.configuration( 'localLibrary' )
keywords   = library/carrel/( rdr.ETC )/( rdr.WRDS )
dictionary = pd.read_csv( DICTIONARY, sep='\t' )

# create and normalize a dataframe of the carrel's reconciled keywords
keywords = pd.read_csv( keywords, sep='\t' )
keywords = keywords[ keywords[ 'qnumber' ].notnull() ]
keywords = keywords.rename( columns=MAP )
keywords = keywords.drop( columns=COLUMNS )
keywords = keywords.drop_duplicates()

# add the keywords to the dictionary, remove duplicates, and sort
dictionary = pd.concat( [ dictionary, keywords ] )
dictionary = dictionary.drop_duplicates()
dictionary = dictionary.sort_values( 'qname' )

# output and done
with open( DICTIONARY, 'w' ) as handle : handle.write( dictionary.to_csv( sep='\t', index=False ) )
exit()
