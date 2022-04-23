import pandas as pd
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter, AsIs
import psycopg2
import psycopg2.extras
import numpy as np

# Numpy type int64 adapter
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(np.int64, addapt_numpy_int64)

DB_CONNECTIONS = {
    'psql': 'postgresql+psycopg2://postgres:Wheninrome1;@database-1.couue7ynblpf.us-west-1.rds.amazonaws.com:5432/postgres'
}

# Class for handling DB transactions
class DatabaseBaseClass:
    
    def __init__(self, db_name):
        self.connection_url = DB_CONNECTIONS[db_name]
        self.conn = None
        self.cur = None
        
    # Reset connection
    def reset(self):
        self.disconnect()
        self.conn = None
        self.cur = None
        self.connect()
        
    # Rollback transaction
    def rollback(self):
        self.conn.rollback()
        
    # Connect to server
    def connect(self):
        
        engine = create_engine(self.connection_url, pool_pre_ping=True)
        self.conn = engine.raw_connection()
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('Connected to db...')
        return self.cur, self.conn
    
    # Disconnect from server
    def disconnect(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
            print('Connection closed')
            
    # Close connection on garbage cleanup
    def __del__(self):
        self.disconnect()
        
    # Extract columns from current cursor
    def cols(self):
        return [i[0] for i in self.cur.description]
        
    # Return what's currently in the cursor as a dataframe
    def df(self):
        
        # Extract Columns
        cols = self.cols()
        
        # Extract data from cursor
        data = self.cur.fetchall()
        
        return pd.DataFrame(data, columns=cols)
        