from chalice import Chalice
import mysql.connector
from utils.common import insert_data_into_db, parse_ga4_response, get_access_token
from utils.ga4_client import fetch_ga4_data
from load_config import load_config

app = Chalice(app_name='ga4-sync')

# Load configuration from the YAML file
config = load_config('config.yaml')

# Secret DB configuration for accessing refresh token
secret_db_config = config['secret_db']
# Result DB configuration for inserting data
result_db_config = config['result_db']

# GA4 configuration
ga4_config = config['ga4_config']
ga4_property_id = ga4_config['ga4_property_id']
client_id = ga4_config['client_id']
client_secret = ga4_config['client_secret']


def get_refresh_token(property_id):
    """
    Connects to the secret DB to fetch the refresh token for the specified ga4_property_id.
    """
    conn = mysql.connector.connect(
        host=secret_db_config['host'],
        user=secret_db_config['user'],
        password=secret_db_config['password'],
        database=secret_db_config['database']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT refresh_token FROM ga4_credentials WHERE property_id = %s", (property_id,))
    refresh_token = cursor.fetchone()
    cursor.close()
    conn.close()

    if refresh_token:
        return refresh_token[0]
    else:
        raise ValueError(f"No refresh token found for property ID: {property_id}")


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}

@app.schedule('rate(1 day)')
def sync_ga4_data_daily(event):
    """
    Function to be triggered daily for syncing GA4 data to MySQL.
    """
    refresh_token = get_refresh_token(ga4_property_id)
    access_token = get_access_token(client_id, client_secret, refresh_token)

    conn = mysql.connector.connect(
        host=result_db_config['host'],
        user=result_db_config['user'],
        password=result_db_config['password'],
        database=result_db_config['database']
    )
    response_rows = fetch_ga4_data(ga4_property_id, access_token)
    parsed_data = parse_ga4_response(response_rows)
    insert_data_into_db(conn, parsed_data)
    conn.close()


@app.schedule('cron(0 0 1 * ? *)')
def sync_ga4_data_monthly(event):
    """
    Function to be triggered every 30 days to sync GA4 data for the past month.
    """
    refresh_token = get_refresh_token(ga4_property_id)
    access_token = get_access_token(client_id, client_secret, refresh_token)

    conn = mysql.connector.connect(
        host=result_db_config['host'],
        user=result_db_config['user'],
        password=result_db_config['password'],
        database=result_db_config['database']
    )
    response_rows = fetch_ga4_data(ga4_property_id, access_token, start_date="30daysAgo", end_date="yesterday")
    parsed_data = parse_ga4_response(response_rows)
    insert_data_into_db(conn, parsed_data)
    conn.close()


@app.route('/sync-data', methods=['POST'])
def sync_custom_ga4_data():
    """
    Endpoint to sync GA4 data for a custom date range.
    """
    request = app.current_request
    body = request.json_body
    start_date = body.get('start_date')
    end_date = body.get('end_date')

    refresh_token = get_refresh_token(ga4_property_id)
    access_token = get_access_token(client_id, client_secret, refresh_token)

    conn = mysql.connector.connect(
        host=result_db_config['host'],
        user=result_db_config['user'],
        password=result_db_config['password'],
        database=result_db_config['database']
    )
    response_rows = fetch_ga4_data(ga4_property_id, access_token, start_date, end_date)
    parsed_data = parse_ga4_response(response_rows)
    insert_data_into_db(conn, parsed_data)
    conn.close()

    return {'message': f'Successfully synced data from {start_date} to {end_date}.'}



