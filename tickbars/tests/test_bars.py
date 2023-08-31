import unittest
from tickbars.bars import calculate_tick_bars, generate_ohlc_bars, create_volume_bars
import datetime
from datetime import timedelta

class TestBarsFunctions(unittest.TestCase):
    def test_calculate_tick_bars(self):
        # Define test data
        test_data = [
            {'timestamp': '2023-08-01 00:00:00', 'price': 10, 'volume': 1},
            {'timestamp': '2023-08-01 00:00:01', 'price': 11, 'volume': 5},
            {'timestamp': '2023-08-01 00:00:03', 'price': 9, 'volume': 3},
            {'timestamp': '2023-08-01 00:00:04', 'price': 10, 'volume': 2},
            {'timestamp': '2023-08-01 00:00:09', 'price': 12, 'volume': 3},

            # Add more test data entries here
        ]

        # Call the function being tested
        tick_threshold = 3
        tick_bars = calculate_tick_bars(test_data, tick_threshold)

        # Compare actual output with expected output
        expected_tick_bars = [
            {'timestamp': '2023-08-01 00:00:03', 'open': 10, 'high': 11, 'low': 9, 'close': 9, 'volume': 9},
            # Add more expected tick bars here
        ]
        self.assertEqual(tick_bars, expected_tick_bars)

    def test_generate_ohlc_bars(self):
        # Define test data
        test_data = [
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 0), 'price': 10, 'volume': 1},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 1), 'price': 11, 'volume': 5},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 3), 'price': 9, 'volume': 3},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 4), 'price': 10, 'volume': 2},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 9), 'price': 12, 'volume': 3},
        ]

        # Call the function being tested
        tick_threshold = 2
        tick_bars = generate_ohlc_bars(test_data, tick_threshold)

        # Compare actual output with expected output
        expected_tick_bars = [
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 2), 'open': 10.0, 'high': 11.0, 'low': 10.0,
             'close': 11.0, 'volume': 6.0},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 4), 'open': 9.0, 'high': 10.0, 'low': 9.0, 'close': 10.0,
             'volume': 5.0},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 10), 'open': 12.0, 'high': 12.0, 'low': 12.0,
             'close': 12.0, 'volume': 3.0}
        ]
        self.assertListEqual(tick_bars, expected_tick_bars)

    def test_create_volume_bars(self):
        # Define test data
        test_data = [
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 0), 'price': 10, 'volume': 1},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 1), 'price': 11, 'volume': 5},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 3), 'price': 9, 'volume': 3},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 4), 'price': 10, 'volume': 2},
            {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 9), 'price': 12, 'volume': 3},
        ]

        # Call the function being tested
        tick_threshold = 5
        tick_bars = create_volume_bars(test_data, tick_threshold)

        # Compare actual output with expected output
        expected_tick_bars = [{'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 1), 'open': 10, 'high': 11, 'low': 10, 'close': 11, 'volume': 6}, {'timestamp': datetime.datetime(2023, 8, 1, 0, 0, 4), 'open': 11, 'high': 11, 'low': 9, 'close': 10, 'volume': 5}]

        self.assertListEqual(tick_bars, expected_tick_bars)

if __name__ == '__main__':
    unittest.main()






