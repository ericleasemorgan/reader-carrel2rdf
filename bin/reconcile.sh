#!/usr/bin/env bash

# reconcile.sh - a front-end to reconcile.py

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 3, 2023 - first cut


# configure
RECONCILE='./bin/reconcile.py'

# initialize
LIBRARY=$( rdr get )

# find all carrels; create a list of jobs
JOBS=()
CARRELS=( $( find $LIBRARY -type d -maxdepth 1 ) )
for CARREL in ${CARRELS[@]}; do

	# parse
	CARREL=$( basename $CARREL )
	
	# sanity check
	if [[ $CARREL == $( basename $LIBRARY ) ]]; then continue; fi
	
	# update the to-do list
	JOBS+=( $CARREL )
	
done

# do the work and done
parallel $RECONCILE ::: ${JOBS[@]}
exit
