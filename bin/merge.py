#!/usr/bin/env python

# configure
CARREL  = './carrel.rdf'
THOREAU = './thoreau.rdf'
AUSTEN  = './austen.rdf'
HOMER   = './homer.rdf'
FORMAT  = 'xml'

GRAPHS  = [ CARREL, THOREAU, AUSTEN, HOMER ]

# require
from rdflib import Graph

# initialize
graph = Graph()

# update, output, and done
for rdf in GRAPHS : graph.parse( rdf )
print( graph.serialize( format=FORMAT ) )
