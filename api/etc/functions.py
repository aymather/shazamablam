import pandas as pd
import os

def big_insert(client, df, table_name, commit=True):
    
    tmp_df = f'tmp_{table_name}_df.csv'
    
    # Clean the dataframe of the separator we're using and escape characters
    df = df.replace({ ';': '', r'\\': '' }, regex=True)
    
    # Temporarily write the data as a csv
    df.to_csv(tmp_df, index=False, sep=';', header=False)
    f = open(tmp_df, 'r')
    
    # Copy tmp csv into database
    client.cur.copy_from(f, table_name, columns=tuple(list(df.columns)), sep=';', null='')
    
    if commit:
        client.conn.commit()
        
    os.remove(tmp_df)