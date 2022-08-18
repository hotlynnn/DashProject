"""
Tests for cpi.py
"""
# Built-ins
import datetime
import unittest
# 3rd-party
# Internal
from cpi import Observation


class TestObservation(unittest.TestCase):

    def test___init__(self):
        inputs = {'Date': datetime.date.today(), 'Item': 'Dozen eggs', 'Price': 3.99, 'Category': 'Food',
                  'State': 'Texas', 'City': 'Dallas'}
        obj = Observation(**inputs)
        self.assertEqual(obj.Date, datetime.date.today())
        self.assertEqual(obj.Category, 'Food')

    def test_create_table(self):
        Observation.create_table()

    def test_get_test_data(self):
        df = Observation.get_test_data()
        self.assertGreater(len(df.index), 0)


if __name__ == '__main__':
    unittest.main()
