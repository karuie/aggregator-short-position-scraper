import scrapy
import pandas as pd
import sqlite3
from io import BytesIO

class ShortPositionsSpider(scrapy.Spider):
    name = 'short_positions'
    start_urls = ['https://www.fca.org.uk/publication/data/short-positions-daily-update.xlsx']

    def __init__(self):
        self.connection = sqlite3.connect('short_positions.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS short_positions (
                id INTEGER PRIMARY KEY,
                position_holder TEXT,
                name_of_share_issuer TEXT,
                isin TEXT,
                net_short_position REAL,
                position_date TEXT
            )
        ''')
        self.connection.commit()

    def parse(self, response):
        with BytesIO(response.body) as f:
            xls = pd.ExcelFile(f)
            sheet_name = self.get_sheet_name(xls.sheet_names, 'historical')
            if sheet_name:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                for index, row in df.iterrows():
                    self.cursor.execute('''
                        INSERT INTO short_positions (position_holder, name_of_share_issuer, isin, net_short_position, position_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (row['Position Holder'], row['Name of Share Issuer'], row['ISIN'], row['Net Short Position (%)'], row['Position Date']))
                    self.connection.commit()
                    yield {
                        'Position Holder': row['Position Holder'],
                        'Name of Share Issuer': row['Name of Share Issuer'],
                        'ISIN': row['ISIN'],
                        'Net Short Position (%)': row['Net Short Position (%)'],
                        'Position Date': row['Position Date']
                    }
            else:
                self.logger.error('Sheet containing "historical" not found.')

    def get_sheet_name(self, sheet_names, keyword):
        for sheet_name in sheet_names:
            if keyword.lower() in sheet_name.lower():
                return sheet_name
        return None

    def close(self, spider, reason):
        self.connection.close()

