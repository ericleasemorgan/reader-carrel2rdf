#!/usr/bin/env bash

# carrel2rdf.sh - a front-end to carrel2rdf.py

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 3, 2023 - first cut


# configure
CARREL2RDF='./bin/carrel2rdf.py'
RDF='./carrels'
LOGS='./logs'

# initialize
LIBRARY=$( rdr get )

# find all carrels; create a list of jobs
JOBS=()
CARRELS=( $( find $LIBRARY -maxdepth 1 -type d  ) )
for CARREL in ${CARRELS[@]}; do

	# parse
	CARREL=$( basename $CARREL )
		
	# sanity check
	if [[ $CARREL == $( basename $LIBRARY ) ]]; then continue; fi
	
	# do not do the work if it has already been done
	if [[ -f "$RDF/$CARREL.rdf" ]]; then continue; fi
	
	# update the to-do list
	JOBS+=( $CARREL )
	
done

# do the work (tricky) and done
parallel "echo 'Processing {}'; $CARREL2RDF {} 2>$LOGS/{}.log | xmllint --format - 1>$RDF/{}.rdf 2>/dev/null" ::: ${JOBS[@]}
exit

