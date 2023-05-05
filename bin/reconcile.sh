#!/usr/bin/env bash

# reconcile.sh - a front-end to reconcile.py

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 3, 2023 - first cut
# May   5, 2023 - added authors/creators


# configure
RECONCILESUBJECTS='./bin/reconcile.py'
RECONCILECREATORS='./bin/reconcile-authors.py'

# initialize
LIBRARY=$( rdr get )

# find all carrels; create a list of jobs
JOBS=()
CARRELS=( $( find $LIBRARY -maxdepth 1 -type d ) )
for CARREL in ${CARRELS[@]}; do

	# parse
	CARREL=$( basename $CARREL )
	
	# sanity check
	if [[ $CARREL == $( basename $LIBRARY ) ]]; then continue; fi
	
	# update the to-do list
	JOBS+=( $CARREL )
	
done

# do the work
echo "Reconciling subjects" >&2
parallel $RECONCILESUBJECTS ::: ${JOBS[@]}
#echo "Reconciling creators" >&2
#parallel $RECONCILECREATORS ::: ${JOBS[@]}

# done
exit
