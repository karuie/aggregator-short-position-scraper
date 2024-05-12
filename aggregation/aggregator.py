import pandas as pd
import sqlite3
from pandas.tseries.offsets import BDay

class AggregationIsinHolderPositionForHfintv:
    def __init__(self, df=None):
        self.df = df

    def load_from_sqlite(self, db_file):
        """
        Load data from SQLite database into a DataFrame and rename columns.

        Parameters:
        - db_file: str, path to the SQLite database file

        Returns:
        - DataFrame: DataFrame containing the loaded data with renamed columns
        """
        connection = sqlite3.connect(db_file)
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

        # Assign the loaded DataFrame to self.df
        self.df = df
        return df

    def aggregate_short_positions(self):
        aggregated_short = {}
        self.df["Position Date"] = pd.to_datetime(self.df["Position Date"])
        self.df = self.df.sort_values(by=["ISIN", "Position Date"])

        # Iterate through DataFrame
        for index, row in self.df.iterrows():
            isin = row["ISIN"]
            position_date = row["Position Date"]
            short_position = row["Net Short Position (%)"]
            holder = row["Position Holder"]

            if isin in aggregated_short:
                if (holder, position_date) not in aggregated_short[isin]:
                    previous_date = self.df[(self.df["ISIN"] == isin) & (self.df["Position Holder"] == holder) & (
                                self.df["Position Date"] < position_date)]["Position Date"].max()
                    if pd.isnull(previous_date):
                        previous_date = \
                        self.df[(self.df["ISIN"] == isin) & (self.df["Position Holder"] == holder)][
                            "Position Date"].min() - pd.Timedelta(days=1)

                    while previous_date < position_date:
                        aggregated_short[isin][(holder, previous_date)] = aggregated_short[
                            isin].get((holder, previous_date), 0)
                        previous_date += pd.Timedelta(days=1)
                        if previous_date.weekday() >= 5:
                            previous_date += BDay(1)

        output_df = pd.DataFrame(columns=["ISIN", "Position Date", "Aggregated short"])
        for isin, positions in aggregated_short.items():
            for (holder, position_date), value in positions.items():
                output_df = output_df.append({"ISIN": isin, "Position Date": position_date, "Aggregated short": value}, ignore_index=True)
        output_df = output_df.sort_values(by=["ISIN", "Position Date"]).reset_index(drop=True)
        return output_df

    def upload_to_sqlite(self, db_file):
        """
        Upload aggregated data to SQLite database.

        Parameters:
        - db_file: str, path to the SQLite database file
        """
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        with connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS aggregated_short_positions")

        self.aggregate_short_positions().to_sql('aggregated_short_positions', connection,
                                                index=False)

        connection.close()