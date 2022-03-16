import unittest
from dynamodb import dynamodb
import create_tables


class TestDynamodb(unittest.TestCase):
    def test_create_tables(self):
        table = dynamodb.Table('users')
        self.assertEqual(table.item_count, 0)
