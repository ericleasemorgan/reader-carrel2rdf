#!/usr/bin/env python

import rdflib

g = rdflib.Graph()
qres = g.query(
    """
    SELECT ?s
    WHERE {
      SERVICE <http://localhost:3030/reader/sparql> {
        ?s a ?o .
      }
    }
    LIMIT 3
    """
)

for row in qres:
    print(row)