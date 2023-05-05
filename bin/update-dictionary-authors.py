#!/usr/bin/env python

# update-dictionary-authors.py - given a carrel, update the dictionary are qnames and their qnumbers

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May 5, 2023 - sometimes I scare myself


# configure
DICTIONARY = './etc/dictionary-authors.tsv'
COLUMNS    = [ 'id' ]
MAP        = { 'author':'qname' }

# require
import pandas as pd
import rdr
import sys

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
carrel = sys.argv[ 1 ]

# initialize
library    = rdr.configuration( 'localLibrary' )
authors    = library/carrel/( rdr.ETC )/( rdr.AUTHORS )
dictionary = pd.read_csv( DICTIONARY, sep='\t' )

# create and normalize a dataframe of the carrel's reconciled authors
authors = pd.read_csv( authors, sep='\t' )
authors = authors[ authors[ 'qnumber' ].notnull() ]
authors = authors.rename( columns=MAP )
authors = authors.drop( columns=COLUMNS )
authors = authors.drop_duplicates()

# add the authors to the dictionary, remove duplicates, and sort
dictionary = pd.concat( [ dictionary, authors ] )
dictionary = dictionary.drop_duplicates()
dictionary = dictionary.sort_values( 'qname' )

# output and done
with open( DICTIONARY, 'w' ) as handle : handle.write( dictionary.to_csv( sep='\t', index=False ) )
exit()
