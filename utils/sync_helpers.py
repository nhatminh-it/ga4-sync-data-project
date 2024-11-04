import logging
import db_config
from utils.common import parse_ga4_response
from utils.ga4_client import fetch_ga4_data
from utils.db_helpers import load_accounts_from_db, get_access_tokens, insert_data_into_db

logger = logging.getLogger(__name__)

def run_data_sync(log_id, secret_conn, start_date=None, end_date=None, account_id=None, property_id=None):
    """
    Runs the data sync process for specific accounts and properties or all if not specified.
    """
    try:
        logger.info(f"[{log_id}] Loading accounts from the database.")
        accounts = load_accounts(log_id, secret_conn, account_id)

        for account in accounts:
            current_account_id = account['account_id']
            try:
                access_tokens = get_access_tokens(log_id, secret_conn, current_account_id)
                process_account_sync_for_properties(log_id, current_account_id, access_tokens, start_date, end_date, property_id)
            except Exception as e:
                logger.error(f"[{log_id}] Error syncing account {current_account_id}: {e}")

        logger.info(f"[{log_id}] Data sync for all specified accounts completed successfully.")

    except Exception as e:
        logger.error(f"[{log_id}] Error during data sync: {e}")

def load_accounts(log_id, secret_conn, account_id=None):
    """
    Loads GA4 account configurations from the 'accounts' table using an existing connection.
    Returns all accounts, a specific account, or a list of accounts if account_id is provided.
    """
    if account_id is None:
        return load_accounts_from_db(log_id, secret_conn)
    elif isinstance(account_id, list):
        return [{'account_id': acc_id} for acc_id in account_id]
    else:
        return [{'account_id': account_id}]

def process_account_sync_for_properties(log_id, account_id, access_tokens, start_date, end_date, property_id=None):
    """
    Processes account sync for all properties or specific properties if provided.
    """
    if property_id is not None:
        if isinstance(property_id, list):
            for prop_id in property_id:
                if prop_id in access_tokens:
                    process_account_sync(log_id, account_id, {prop_id: access_tokens[prop_id]}, start_date, end_date)
                else:
                    logger.warning(f"[{log_id}] Property ID {prop_id} not found for account ID {account_id}.")
        else:
            if property_id in access_tokens:
                process_account_sync(log_id, account_id, {property_id: access_tokens[property_id]}, start_date, end_date)
            else:
                logger.warning(f"[{log_id}] Property ID {property_id} not found for account ID {account_id}.")
    else:
        process_account_sync(log_id, account_id, access_tokens, start_date, end_date)

def process_account_sync(log_id, account_id, access_tokens, start_date=None, end_date=None):
    """
    Processes the GA4 data sync for all property IDs under a given account.
    """
    logger.info(f"[{log_id}] Processing account ID: {account_id}")

    for property_id, access_token in access_tokens.items():
        logger.info(f"[{log_id}] Starting sync for property ID: {property_id}")
        try:
            # Create a connection to the result database
            result_conn = db_config.get_result_db_conn()

            response_rows = fetch_ga4_data(log_id, property_id, access_token, start_date, end_date)
            parsed_data = parse_ga4_response(log_id, response_rows, account_id, property_id)
            insert_data_into_db(log_id, result_conn, parsed_data)
            result_conn.close()

            logger.info(f"[{log_id}] Sync for property ID {property_id} completed successfully.")
        except Exception as e:
            logger.error(f"[{log_id}] Error syncing property ID {property_id}: {e}")
