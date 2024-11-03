from chalice import Chalice
import mysql.connector

from utils.common import insert_data_into_db, parse_ga4_response
from utils.ga4_client import fetch_ga4_data
from google.oauth2 import service_account

app = Chalice(app_name='ga4-sync')

# GA4 configuration
GA4_PROPERTY_ID = 'YOUR_GA4_PROPERTY_ID'
CREDENTIALS = service_account.Credentials.from_service_account_file('path/to/your/credentials.json')


@app.schedule('rate(1 day)')
def sync_ga4_data_daily(event):
    """
    Function to be triggered daily for syncing GA4 data to MySQL.
    """
    conn = mysql.connector.connect(
        host='YOUR_MYSQL_HOST',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        database='ga4_data'
    )
    response_rows = fetch_ga4_data(GA4_PROPERTY_ID, CREDENTIALS)
    parsed_data = parse_ga4_response(response_rows)
    insert_data_into_db(conn, parsed_data)
    conn.close()


@app.schedule('cron(0 0 1 * ? *)')
def sync_ga4_data_monthly(event):
    """
    Function to be triggered every 30 days to sync GA4 data for the past month.
    """
    conn = mysql.connector.connect(
        host='YOUR_MYSQL_HOST',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        database='ga4_data'
    )
    response_rows = fetch_ga4_data(GA4_PROPERTY_ID, CREDENTIALS, start_date="30daysAgo", end_date="yesterday")
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

    conn = mysql.connector.connect(
        host='YOUR_MYSQL_HOST',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        database='ga4_data'
    )
    response_rows = fetch_ga4_data(GA4_PROPERTY_ID, CREDENTIALS, start_date, end_date)
    parsed_data = parse_ga4_response(response_rows)
    insert_data_into_db(conn, parsed_data)
    conn.close()

    return {'message': f'Successfully synced data from {start_date} to {end_date}.'}
