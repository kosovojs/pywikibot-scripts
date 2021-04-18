#!/usr/bin/env python3
# -*- coding: utf-8  -*-
import os, sys
print os.path.dirname(os.path.abspath(__file__))


sys.path.append('/data/project/edgars/pywikibot/')
#sys.path.append('/data/project/edgars/pwb_helpers/toolforge/')


import re, os, sys#, toolforge
from glob import glob


import functools
import os
import pymysql
import requests


def connect(dbname, cluster='web', **kwargs):
    """
    Get a database connection for the
    specified wiki
    :param dbname: Database name
    :param cluster: Database cluster (analytics or web)
    :param kwargs: For pymysql.connect
    :return: pymysql connection
    """
    assert cluster in ['tools', 'analytics', 'labsdb', 'web']

    if cluster == 'labsdb':
        domain = 'labsdb'
    else:
        domain = '{}.db.svc.eqiad.wmflabs'.format(cluster)

    if dbname.endswith('_p'):
        dbname = dbname[:-2]

    if dbname == 'meta':
        host = 's7.{}'.format(domain)
    else:
        host = '{}.{}'.format(dbname, domain)
    host = kwargs.pop('host', host)

    return pymysql.connect(
        database=dbname + '_p',
        host=host,
        read_default_file=os.path.expanduser("~/replica.my.cnf"),
        charset='utf8mb4',
        **kwargs
    )

def connect_tools(dbname, cluster='web', **kwargs):
    """
    Get a database connection for the
    specified wiki
    :param dbname: Database name
    :param cluster: Database cluster (analytics or web)
    :param kwargs: For pymysql.connect
    :return: pymysql connection
    """
    assert cluster in ['tools', 'analytics', 'labsdb', 'web']

    domain = 'tools-db'

   # if dbname.endswith('_p'):
    #    dbname = dbname[:-2]

    if dbname == 'meta':
        host = 's7.{}'.format(domain)
    else:
        host = '{}'.format(domain)
    host = kwargs.pop('host', host)

    return pymysql.connect(
        database=dbname,
        host=host,
        read_default_file=os.path.expanduser("~/replica.my.cnf"),
        charset='utf8mb4',
        **kwargs
    )



connLabs = connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = connLabs):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#

query = "select balsotajs from labakais"
query_res = run_query(query,connLabs)
print query_res
#encode_if_necessary(query_res[0][0])