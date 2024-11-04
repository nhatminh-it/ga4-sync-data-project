import logging

import mysql
from mysql.connector import MySQLConnection

logger = logging.getLogger(__name__)

def get_access_tokens(log_id, conn, account_id):
    """
    Fetches access tokens for all property IDs associated with a given account.
    """
    logger.info(f"[{log_id}] Fetching access tokens for account ID: {account_id}")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT property_id, access_token FROM ga4_credentials WHERE account_id = %s", (account_id,))
    credentials = cursor.fetchall()
    cursor.close()

    access_tokens = {cred['property_id']: cred['access_token'] for cred in credentials}
    logger.info(f"[{log_id}] Access tokens for {len(access_tokens)} properties fetched.")
    return access_tokens

def load_accounts_from_db(log_id, conn):
    """
    Loads GA4 account configurations from the 'accounts' table using an existing connection.
    """
    logger.info(f"[{log_id}] Loading accounts from the database.")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT account_id FROM accounts")
    accounts = cursor.fetchall()
    cursor.close()

    logger.info(f"[{log_id}] {len(accounts)} accounts loaded.")
    return accounts

def insert_data_into_db(log_id: str, conn: MySQLConnection, parsed_data: list) -> int:
    """
    Inserts data into the MySQL database in batches.

    Args:
        log_id (str): A unique identifier for logging purposes.
        conn (MySQLConnection): MySQL database connection object.
        parsed_data (list): List of tuples containing data to insert. Each tuple should match
                            the structure (account_id, property_id, campaign_id, campaign_name,
                            start_date, end_date, sessions, advertiser_ad_clicks,
                            advertiser_ad_cost, advertiser_ad_cost_per_click,
                            advertiser_ad_impressions, total_revenue).

    Returns:
        int: Number of records inserted.
    """
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO ga4_report (account_id, property_id, campaign_id, campaign_name, start_date, end_date, sessions, 
                            advertiser_ad_clicks, advertiser_ad_cost, advertiser_ad_cost_per_click, 
                            advertiser_ad_impressions, total_revenue)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    record_count = 0
    batch_size = 1000  # Define the batch size
    batch_data = []  # List to hold records for batch insert

    try:
        for data in parsed_data:
            batch_data.append(data)
            if len(batch_data) >= batch_size:
                cursor.executemany(insert_query, batch_data)  # Insert the batch
                record_count += len(batch_data)  # Update the record count
                batch_data = []  # Reset the batch

        # Insert any remaining records in the batch
        if batch_data:
            cursor.executemany(insert_query, batch_data)
            record_count += len(batch_data)

        conn.commit()
        logger.info(f"[{log_id}] Inserted {record_count} records into the database.")
    except mysql.connector.Error as e:
        logger.error(f"[{log_id}] Database error during insert operation: {e}")
    finally:
        cursor.close()

    return record_count