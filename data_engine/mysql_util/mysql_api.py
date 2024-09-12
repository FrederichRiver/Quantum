# class mysqlHeader用于封装与mysql数据库的连接

import pymysql

class mysqlEngine(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def select(self, col: list, table_name: str, conditions: str) -> tuple:
        cols = ','.join(col)
        sql = f"select {cols} from {table_name} where {conditions}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    
    def dict_insert(self, table_name: str, col_name: list[str], data: list):
        value_pairs = []
        col_list = data[0].keys()
        columns = ','.join(col_name)
        for item in data:
            value_list = []
            for col in col_list:
                value_list.append(f"\'{item[col]}\'")
            values = ','.join(value_list)
            value_pairs.append(f"({values})")
        values = ','.join(value_pairs)
        sql = f"insert into {table_name} ({columns}) values {values}"
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name: str, data: dict):
        keys = ','.join(f"'{data.keys()}'")
        values = ','.join(f"'{data.values()}'")
        sql = f"insert into {table_name} ({keys}) values ({values})"
        self.cursor.execute(sql)
        self.conn.commit()

    def update(self, table_name: str, data: dict, conditions: list):
        values = ','.join([f"{k}={v}" for k, v in data.items()])
        sql = f"update {table_name} set {values} where {conditions}"
        self.cursor.execute(sql)
        self.conn.commit()
    
    def duplicate_table(self, table_name: str, template_table_name: str):
        sql = f"create table if not exists {table_name} like {template_table_name}"
        self.cursor.execute(sql)
        self.conn.commit()

