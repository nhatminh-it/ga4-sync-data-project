import mysql
import requests
import mysql.connector
from datetime import datetime, timedelta
from mysql.connector import MySQLConnection
import logging

from utils.utils import generate_mock_data

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def insert_data_into_db(log_id: str, conn: MySQLConnection, parsed_data: list) -> int:
    """
    Inserts data into the MySQL database.

    Args:
        log_id (str): A unique identifier for logging purposes.
        conn (MySQLConnection): MySQL database connection object.
        parsed_data (list): List of tuples containing data to insert. Each tuple should match
                            the structure (campaign_id, campaign_name, start_date, end_date,
                            sessions, advertiser_ad_clicks, advertiser_ad_cost,
                            advertiser_ad_cost_per_click, advertiser_ad_impressions, total_revenue).

    Returns:
        int: Number of records inserted.
    """
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO ga4_report (campaign_id, campaign_name, start_date, end_date, sessions, 
                            advertiser_ad_clicks, advertiser_ad_cost, advertiser_ad_cost_per_click, 
                            advertiser_ad_impressions, total_revenue)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    record_count = 0
    for data in parsed_data:
        try:
            cursor.execute(insert_query, data)
            record_count += 1
        except mysql.connector.Error as e:
            logger.error(f"[{log_id}] Error inserting record {data}: {e}")

    conn.commit()
    cursor.close()

    logger.info(f"[{log_id}] Inserted {record_count} records into the database.")
    return record_count


def parse_ga4_response(log_id: str, response_rows) -> list:
    """
    Parse the GA4 API response rows to extract campaign ID, campaign name, start date, end date,
    and metrics such as sessions, advertiser ad clicks, advertiser ad cost, advertiser ad cost per click,
    advertiser ad impressions, and total revenue.

    Args:
        log_id (str): A unique identifier for logging purposes.
        response_rows (list): List of response rows from the GA4 API.

    Returns:
        list: A list of tuples, each containing the extracted data ready for database insertion.
    """
    # Generate mock data if response_rows is None or empty
    if response_rows is None or len(response_rows) == 0:
        logger.warning(f"[{log_id}] No data received from GA4 API, generating mock data.")
        response_rows = generate_mock_data(log_id)

    parsed_data = []

    for row in response_rows:
        campaign_id = row['dimensionValues'][2]['value']  # campaignId
        campaign_name = row['dimensionValues'][3]['value']  # campaignName
        date_str = row['dimensionValues'][1]['value']  # date

        end_date = datetime.strptime(date_str, '%Y%m%d').date()
        start_date = end_date - timedelta(days=1)

        sessions = row['metricValues'][0]['value']
        advertiser_ad_clicks = row['metricValues'][1]['value']
        advertiser_ad_cost = row['metricValues'][2]['value']
        advertiser_ad_cost_per_click = row['metricValues'][3]['value']
        advertiser_ad_impressions = row['metricValues'][4]['value']
        total_revenue = row['metricValues'][5]['value']

        parsed_data.append((
            campaign_id,
            campaign_name,
            start_date,
            end_date,
            sessions,
            advertiser_ad_clicks,
            advertiser_ad_cost,
            advertiser_ad_cost_per_click,
            advertiser_ad_impressions,
            total_revenue
        ))

    logger.info(f"[{log_id}] Parsed {len(parsed_data)} records from GA4 response.")
    return parsed_data


def get_access_token(log_id: str, client_id: str, client_secret: str, refresh_token: str) -> str:
    """
    Get access token from Google OAuth 2.0.

    Args:
        log_id (str): A unique identifier for logging purposes.
        client_id (str): The client ID of your application.
        client_secret (str): The client secret of your application.
        refresh_token (str): The refresh token for your application.

    Returns:
        str: The access token.
    """
    token_url = 'https://oauth2.googleapis.com/token'

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    logger.info(f"[{log_id}] Requesting access token.")
    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        logger.error(f"[{log_id}] Error fetching access token: {response.text}")
        raise Exception(f"[{log_id}] Error fetching access token: {response.text}")

    token_info = response.json()
    logger.info(f"[{log_id}] Access token fetched successfully.")
    return token_info['access_token']
