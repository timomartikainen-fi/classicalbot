import psycopg
from psycopg.rows import dict_row

class DatabaseManager:
    def __init__(self, conn_info):
        self.conn_info = conn_info
        self.conn = None

    def __enter__(self):
        self.conn = psycopg.connect(**self.conn_info, row_factory = dict_row)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params = None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description: # if there's a result set
                return cur.fetchall()
            self.conn.commit()