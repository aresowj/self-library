#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import connection

def some_query():
    start = datetime.now()
    query_count = len(connection.queries)
    
    # write some database operation
    
    # time elapsed
    print datetime.now() - start
    # queries made
    print len(connection.queries) - query_count
    # detailed query SQL
    for query in connection.queries[query_count:]:
        print query
