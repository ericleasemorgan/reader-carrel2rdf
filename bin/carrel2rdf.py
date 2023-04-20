#!/usr/bin/env python

# carrel2rdf.py - given the name of a study carrel, output RDF/XML

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 1, 2023 - first investigations
# April 2, 2023 - made great headway


# configure
TEMPLATECARREL  = './etc/template-carrel.txt'
TEMPLATEITEM    = './etc/template-item.txt'
TEMPLATECREATOR = './etc/template-creator.txt'
TEMPLATETITLE   = './etc/template-title.txt'
TEMPLATEDATE    = './etc/template-date.txt'
TEMPLATESUBJECT = './etc/template-subject.txt'
TEMPLATEKEYWORD = './etc/template-keyword.txt'
HTTPROOT        = 'https://distantreader.org/stacks/carrels/'
WIKIDATAROOT    = 'https://www.wikidata.org/wiki/'
THRESHOLD       = 25.0

# require
from   pathlib import Path
import json
import pandas as pd
import rdr
import sys

# escape the bare bonest of entities
def escape( s ) : 

	# do the work, conditionallly
	if not s : return
	else     : return str( s ).replace( '&', '&amp;' ).replace( '<', '&lt;' ).replace( '>', '&gt;' )

# get input
if len( sys.argv ) != 2 : sys.exit( "Usage: " + sys.argv[ 0 ] + " <carrel>" )
carrel = sys.argv[ 1 ]

# debug
#sys.stderr.write( 'RDFing ' + carrel + '\n' )

# initialize
uri = HTTPROOT + carrel
with open( Path( TEMPLATECARREL ) )  as handle : templateCarrel  = handle.read()
with open( Path( TEMPLATEITEM ) )    as handle : templateItem    = handle.read()
with open( Path( TEMPLATESUBJECT ) ) as handle : templateSubject = handle.read()
with open( Path( TEMPLATEKEYWORD ) ) as handle : templateKeyword = handle.read()

# get carrel literals
process          = rdr.provenance( carrel, 'process' )
dateCreated      = rdr.provenance( carrel, 'dateCreated' )
totalSizeInItems = rdr.extents( carrel, 'items' )
totalSizeInWords = rdr.extents( carrel, 'words' )
averageFlesch    = rdr.extents( carrel, 'flesch' )

# get subjects/keywords
subjectWords = None
keywordWords = None
wrds         = ( rdr.configuration( 'localLibrary' ) )/carrel/( rdr.ETC )/( rdr.WRDS )
if wrds.exists() :

	vocabulary   = pd.read_csv( wrds, sep='\t' )
	subjectWords = vocabulary[ vocabulary[ 'qnumber' ].notnull() ]
	keywordWords = vocabulary[ vocabulary[ 'qnumber' ].isnull() ]

# create carrel subjects; check for literary warrant
carrelSubjects = []
subjects       = subjectWords[ [ 'keyword', 'qnumber' ] ].drop_duplicates()
for _, subject in subjects.iterrows() :

	# calculate relative weight of the given subject
	count  = len( subjectWords[ subjectWords[ 'keyword' ] == subject[ 'keyword' ] ] )
	weight = ( count / totalSizeInItems ) * 100

	# create and add subject, conditionally
	if weight > THRESHOLD :		
		qName         = escape( subject[ 'keyword' ] )
		qNumber       = WIKIDATAROOT + subject[ 'qnumber' ]
		carrelSubject = templateSubject.replace( '##QNAME##', qName ).replace( '##QNUMBER##', qNumber )
		carrelSubjects.append( carrelSubject )

# fall back to keywords, conditionally
if len( carrelSubjects ) == 0 :

	keywords = keywordWords[ [ 'keyword' ] ].drop_duplicates()
	for _, keyword in keywords.iterrows() :

		# calculate relative weight of the given subject
		count  = len( keywordWords[ keywordWords[ 'keyword' ] == keyword[ 'keyword' ] ] )
		weight = ( count / totalSizeInItems ) * 100
		
		# create and add keyword, conditionally
		if weight > THRESHOLD :		
			keyword       = escape( keyword[ 'keyword' ] )
			carrelSubject = templateKeyword.replace( '##KEYWORD##', keyword )
			carrelSubjects.append( carrelSubject )

# fall back even more to simply most frequent subjects, conditionally
if len( carrelSubjects ) == 0 :
	
	subjects = list( subjectWords[ 'keyword' ].mode() )		
	subjects = subjectWords[ subjectWords[ 'keyword' ].isin( subjects ) ]
	subjects = subjects[ [ 'keyword', 'qnumber' ] ].drop_duplicates()
	for _, subject in subjects.iterrows() :
	
		qName         = escape( subject[ 'keyword' ] )
		qNumber       = WIKIDATAROOT + subject[ 'qnumber' ]
		carrelSubject = templateSubject.replace( '##QNAME##', qName ).replace( '##QNUMBER##', qNumber )
		carrelSubjects.append( carrelSubject )

# giving up; no subjects
if len( carrelSubjects ) == 0 : carrelSubjects = ''

# create a list of bibliographic items
bibliographicItems = []
bibliographics     = json.loads( rdr.bibliography( carrel, format='json' ) )
for index, bibliographic in enumerate( bibliographics ) :
		
	# parse the simple stuff
	idItem          = str( bibliographic[ 'id' ] )
	flesch          = str( bibliographic[ 'flesch' ] )
	sizeInWords     = str( bibliographic[ 'words' ] )
	extension       = str( bibliographic[ 'extension' ] )
	mimetypeitem    = bibliographic[ 'mime' ]
	descriptionitem = escape( bibliographic[ 'summary' ] )

	# author/creator
	creator              = escape( bibliographic[ 'author' ] )
	bibliographicCreator = ''
	if creator :
		with open( Path( TEMPLATECREATOR ) ) as handle : templateCreator = handle.read()
		bibliographicCreator = templateCreator.replace( '##CREATOR##', creator )
	
	# title
	titleItem          = escape( bibliographic[ 'title' ] )
	bibliographicTitle = ''
	if titleItem :
		with open( Path( TEMPLATETITLE ) ) as handle : templateTitle = handle.read()
		bibliographicTitle = templateTitle.replace( '##TITLEITEM##', titleItem )
	
	# date
	date              = escape( bibliographic[ 'date' ] )
	bibliographicDate = ''
	if date :
		with open( Path( TEMPLATEDATE ) ) as handle : templateDate = handle.read()
		bibliographicDate = templateDate.replace( '##DATE##', date )
	
	# subjects
	bibliographicSubjects = []
	if not subjectWords.empty :
	
		for _, subjectWord in subjectWords.iterrows() :
			
			# check for the current identifier
			if str( subjectWord[ 'id' ] ) == idItem :
						
				# parse, fill template, and updatae
				qName                = escape( subjectWord[ 'keyword' ] )
				qNumber              = WIKIDATAROOT + subjectWord[ 'qnumber' ]
				bibliographicSubject = templateSubject.replace( '##QNAME##', qName ).replace( '##QNUMBER##', qNumber )
				bibliographicSubjects.append( bibliographicSubject )
	
	# keywords
	bibliographicKeywords = []
	if not keywordWords.empty :
	
		for _, keywordWord in keywordWords.iterrows() :
			
			# check for the current identifier
			if str( keywordWord[ 'id' ] ) == idItem :
		
				# parse, fill template, and updatae
				keyword              = escape( keywordWord[ 'keyword' ] )
				bibliographicKeyword = templateKeyword.replace( '##KEYWORD##', keyword )
				bibliographicKeywords.append( bibliographicKeyword )

	# sanity checks
	if len( bibliographicSubjects ) == 0 : bibliographicSubjects = ''
	if len( bibliographicKeywords ) == 0 : bibliographicKeywords = ''
	
	# fill in template and update
	bibliographicItem = templateItem.replace( '##IDITEM##', idItem )
	bibliographicItem = bibliographicItem.replace( '##BIBLIOGRAPHICCREATOR##', bibliographicCreator )
	bibliographicItem = bibliographicItem.replace( '##BIBLIOGRAPHICTITLE##', bibliographicTitle )
	bibliographicItem = bibliographicItem.replace( '##BIBLIOGRAPHICDATE##', bibliographicDate )
	bibliographicItem = bibliographicItem.replace( '##BIBLIOGRAPHICSUBJECTS##', ' '.join( bibliographicSubjects ) )	
	bibliographicItem = bibliographicItem.replace( '##BIBLIOGRAPHICKEYWORDS##', ' '.join( bibliographicKeywords ) )	
	bibliographicItem = bibliographicItem.replace( '##DESCRIPTIONITEM##', descriptionitem )
	bibliographicItem = bibliographicItem.replace( '##EXTENSION##', extension )
	bibliographicItem = bibliographicItem.replace( '##FLESH##', flesch )
	bibliographicItem = bibliographicItem.replace( '##MIMETYPEITEM##', mimetypeitem )
	bibliographicItem = bibliographicItem.replace( '##SIZEINWORDS##', sizeInWords )
	bibliographicItem = bibliographicItem.replace( '##URI##', uri )
	bibliographicItems.append( bibliographicItem )
	
	#if index > 1 : break
	
# build the rdf
rdf = templateCarrel.replace( '##CARREL##', carrel )
rdf = rdf.replace( '##URI##', uri )
rdf = rdf.replace( '##PROCESS##', process )
rdf = rdf.replace( '##DATECREATED##', dateCreated )
rdf = rdf.replace( '##TOTALSIZEINITEMS##', str( totalSizeInItems ) )
rdf = rdf.replace( '##TOTALSIZEINWORDS##', str( totalSizeInWords ) )
rdf = rdf.replace( '##AVERAGEFLESCH##', str( averageFlesch ) )
rdf = rdf.replace( '##CARRELSUBJECTS##', ' '.join( carrelSubjects ) )
rdf = rdf.replace( '##BIBLIOGRAPHICITEMS##', ' '.join( bibliographicItems ) )

# output and done
print( rdf )
exit()