from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import psycopg2.extras
import pandas as pd
import os


class ClientBase():

    def __init__(self, connection_string):

        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.session = sessionmaker(bind=self.engine)

    def execute(self, sql, params={}, raw=False):

        # Init a session
        session = self.session()

        # Execute query and return cursor
        cur = session.execute(text(sql), params)

        # Commit changes if there are any
        session.commit()

        if cur.returns_rows:

            results = cur.fetchall()

            if raw:
                return results
            else:
                return pd.DataFrame(results, columns=cur.keys())

    def big_insert(self, df, table_name):
    
        tmp_df = f'tmp_{table_name}_df.csv'
        
        # Create connection
        conn = self.engine.raw_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Clean the dataframe of the separator we're using and escape characters
        df = df.replace({ ';': '', r'\\': '' }, regex=True)

        # Create a temporary csv file to be used for uploading
        df.to_csv(tmp_df, index=False, sep=';', header=False)
        f = open(tmp_df, 'r')
        
        # Insert csv into database
        cur.copy_from(f, table_name, columns=tuple(list(df.columns)), sep=';', null='')
        conn.commit()

        # Remove temp file
        os.remove(tmp_df)
        
        # Close connection
        cur.close()
        conn.close()

    def end(self):

        self.session = None
        self.engine = None
