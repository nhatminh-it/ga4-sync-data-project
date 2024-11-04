import mysql.connector
from load_config import load_config

# Load configuration
config = load_config('config.yaml')
secret_db_config = config['secret_db']
result_db_config = config['result_db']

# Export necessary configurations and connections
def get_secret_db_config():
    return secret_db_config

def get_result_db_config():
    return result_db_config

def get_secret_db_conn():
    return mysql.connector.connect(
        host=secret_db_config['host'],
        user=secret_db_config['user'],
        password=secret_db_config['password'],
        database=secret_db_config['database']
    )

def get_result_db_conn():
    return mysql.connector.connect(
        host=result_db_config['host'],
        user=result_db_config['user'],
        password=result_db_config['password'],
        database=result_db_config['database']
    )
