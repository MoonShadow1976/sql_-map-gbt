import psycopg2
import json


class PostgreSQLDatabaseStructure:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
        except Exception as error:
            print(f"Error connecting to PostgreSQL database: {error}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()

    def get_tables(self):
        if not self.connection:
            print("No connection established.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
            """)
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as error:
            print(f"Error fetching tables: {error}")
            return []

    def get_table_structure(self, table_name):
        if not self.connection:
            print("No connection established.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
            """)
            columns = cursor.fetchall()
            return columns
        except Exception as error:
            print(f"Error fetching table structure: {error}")
            return []

    def get_table_indexes(self, table_name):
        if not self.connection:
            print("No connection established.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename = '{table_name}'
            """)
            indexes = cursor.fetchall()
            return indexes
        except Exception as error:
            print(f"Error fetching table indexes: {error}")
            return []

    def get_table_constraints(self, table_name):
        if not self.connection:
            print("No connection established.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT constraint_name, constraint_type
                FROM information_schema.table_constraints
                WHERE table_name = '{table_name}'
            """)
            constraints = cursor.fetchall()
            return constraints
        except Exception as error:
            print(f"Error fetching table constraints: {error}")
            return []

    def get_database_structure(self):
        database_structure = {}
        tables = self.get_tables()
        for table in tables:
            database_structure[table] = {
                "columns": self.get_table_structure(table),
                "indexes": self.get_table_indexes(table),
                "constraints": self.get_table_constraints(table)
            }
        return database_structure

    def save_database_structure_to_file(self, file_path):
        database_structure = self.get_database_structure()
        with open(file_path, 'w') as json_file:
            json.dump(database_structure, json_file, indent=4)
        print(f"Database structure has been written to {file_path}")
        print(str(database_structure))


# 示例如何使用这个类
if __name__ == "__main__":
    db_structure = PostgreSQLDatabaseStructure(
        user="postgres",
        password="20020727",
        host="localhost",
        port="5432", # PostgreSQL 的默认端口是 5432
        database="china"
    )

    db_structure.connect()
    db_structure.save_database_structure_to_file('database_structure.json')
    db_structure.close()
