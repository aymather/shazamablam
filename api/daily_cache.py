from etc.ClientBase import ClientBase
import requests
import pandas as pd
import numpy as np
import time

db_string = 'postgresql+psycopg2://postgres:Wheninrome1;@database-1.couue7ynblpf.us-west-1.rds.amazonaws.com:5432/postgres'

client = ClientBase(db_string)

string = """
    select *
    from shazamablam.artists
    where name ~* :artist
"""
params = { 'artist': 'doja cat' }
df = client.execute(string, params)

print(df)

f = open('test_file.txt', 'w')
f.write(str(df.to_dict('records')))
f.close()