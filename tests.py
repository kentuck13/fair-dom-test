import unittest
from uuid import uuid4
from datetime import datetime

from dynamodb import dynamodb
from boto3.dynamodb.conditions import Attr


class TestStringMethods(unittest.TestCase):
    table = dynamodb.Table('users')

    def _fixtures(self):
        data = [
            {
                'uuid': 'c5016bba-6394-4420-9d4c-4330c58eefed',
                'date_time': datetime(2021, 1, 1).isoformat(),
            },
            {
                'uuid': 'd94be86f-548a-42a8-8ac3-8669ed3bd63e',
                'date_time': datetime(2022, 1, 1).isoformat(),
            },
            {
                'uuid': '42b24bd5-bcce-4c14-a75f-7267574898ac',
                'date_time': datetime(2022, 1, 1).isoformat(),
            },
        ]

        scan = self.table.scan()
        with self.table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key=each
                )

        with self.table.batch_writer() as batch:
            for i in data:
                batch.put_item(Item=i)

        return data

    def test_create(self):
        self.table.put_item(
            Item={
                'uuid': str(uuid4()),
                'date_time': str(datetime.utcnow()),
            }
        )
        self.assertEqual(self.table.item_count, 4)

    def test_get_item(self):
        data = self._fixtures()
        self.assertEqual(self.table.item_count, 3)

        response = self.table.get_item(Key=data[0])
        self.assertEqual(response['Item'], data[0])

    def test_scan(self):
        self.assertEqual(self.table.item_count, 3)

        response = self.table.scan(
            FilterExpression=Attr('date_time').gt(
                datetime(2021, 1, 1).isoformat()
            )
        )
        self.assertEqual(
            response['Items'],
            [
                {
                    'date_time': '2022-01-01T00:00:00',
                    'uuid': '42b24bd5-bcce-4c14-a75f-7267574898ac'
                },
                {
                    'date_time': '2022-01-01T00:00:00',
                    'uuid': 'd94be86f-548a-42a8-8ac3-8669ed3bd63e'
                }
            ]

        )


if __name__ == '__main__':
    unittest.main()
