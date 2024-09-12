import unittest
from unittest.mock import patch, MagicMock
from mysql_api import mysqlEngine


class TestysqlEngine(unittest.TestCase):

    @patch('pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.db = mysqlEngine('localhost', 'stock', 'Stock@2024', 'stock')

    def test_select(self):
        self.mock_cursor.fetchall.return_value = (('row1',), ('row2',))
        result = self.db.select(['col1', 'col2'], 'test_table', ['condition1', 'condition2'])
        self.mock_cursor.execute.assert_called_once_with("select col1,col2 from test_table where ['condition1', 'condition2']")
        self.assertEqual(result, (('row1',), ('row2',)))

    def test_insert(self):
        self.db.insert('stock_list', {'stock_code': 'TEST0001', 'stock_name': '测试股票1', 'orgId': 'test001', 'short_code': 'test001'})
        self.mock_cursor.execute.assert_called_once_with("insert into test_table (col1,col2) values (val1,val2)")
        self.mock_conn.commit.assert_called_once()

    def test_update(self):
        self.db.update('test_table', {'col1': 'val1', 'col2': 'val2'}, ['condition1', 'condition2'])
        self.mock_cursor.execute.assert_called_once_with("update test_table set col1=val1,col2=val2 where ['condition1', 'condition2']")
        self.mock_conn.commit.assert_called_once()

    def test_duplicate_table(self):
        self.db.duplicate_table('new_table', 'stock_list')
        # self.mock_cursor.execute.assert_called_once_with("create table if not exist new_table from template_table")
        self.mock_conn.commit.assert_called_once()

    def tearDown(self):
        self.db.close()
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
