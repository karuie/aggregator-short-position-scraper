import pandas as pd
import sqlite3

connection = sqlite3.connect('short_positions.db')

query = 'SELECT * FROM short_positions'

df = pd.read_sql_query(query, connection)

connection.close()

df = df.rename(columns={
    'position_holder': 'Position_Holder',
    'name_of_share_issuer': 'Name_of_Share_Issuer',
    'isin': 'ISIN',
    'net_short_position': 'Net_Short_Position',
    'position_date': 'Position_Date'
})

