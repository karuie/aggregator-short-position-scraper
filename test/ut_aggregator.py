# tests/test_aggregator.py

import unittest
import pandas as pd
from aggregation.aggregator import Aggregator

class TestAggregator(unittest.TestCase):
    def setUp(self):
        # Sample data
        self.data = pd.DataFrame({
            "Position Holder": ["Kintbury Capital LLP", "Kintbury Capital LLP"],
            "Name of Share Issuer": ["Company 1", "Company 1"],
            "ISIN": ["GB0031743007", "GB0031743007"],
            "Net Short Position (%)": [0.46, 0.57],
            "Position Date": ["2024-04-30", "2024-04-24"]
        })
        self.data["Position Date"] = pd.to_datetime(self.data["Position Date"])

    def test_aggregate_short_positions(self):
        aggregator = Aggregator(self.data)
        aggregated_short = aggregator.aggregate_short_positions()
        expected_result = {
            'GB0031743007': {
                ('Kintbury Capital LLP', pd.Timestamp('2024-04-24 00:00:00')): 0.57,
                ('Kintbury Capital LLP', pd.Timestamp('2024-04-25 00:00:00')): 0.57,
                ('Kintbury Capital LLP', pd.Timestamp('2024-04-26 00:00:00')): 0.57,
                ('Kintbury Capital LLP', pd.Timestamp('2024-04-29 00:00:00')): 0.57,
                ('Kintbury Capital LLP', pd.Timestamp('2024-04-30 00:00:00')): 0.46
            }
        }
        self.assertEqual(aggregated_short, expected_result)

if __name__ == '__main__':
    unittest.main()
