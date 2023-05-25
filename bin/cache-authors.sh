#!/usr/bin/env bash

# configure
DICTIONARY='./etc/dictionary-authors.tsv'
ROOT='https://www.wikidata.org/entity'
EXTENSION='.rdf'
DIRECTORY='./authors'

# create a list of jobs (very elegant), submit them, and done
JOBS=$( tail -n+2 $DICTIONARY | cut -f2 | sort )
parallel "echo 'Processing {}'; wget -O $DIRECTORY/{}$EXTENSION $ROOT/{}$EXTENSION" ::: ${JOBS[@]}
exit
