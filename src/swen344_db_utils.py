import psycopg2
import yaml

# Load DB config
def load_db_config():
    with open('api/db.yml', 'r') as file:
        return yaml.safe_load(file)['db']

# Connect to DB
def get_db_connection():
    config = load_db_config()
    return psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        dbname=config['name']
    )

# Execute SQL file
def exec_sql_file(filename):
    with open(filename, 'r') as file:
        sql = file.read()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()

# Run a query
def run_query(query, params=None, fetch_one=False):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
