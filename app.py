import uuid
import logging
import db_config

from chalice import Chalice
from utils.sync_helpers import run_data_sync
from utils.utils import parse_request_body

app = Chalice(app_name='ga4-sync')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Access the global connections and configurations
secret_conn = db_config.get_secret_db_conn()
result_conn = db_config.get_result_db_conn()

@app.route('/')
def index():
    return {'hello': 'world'}

@app.schedule('rate(1 day)')
def sync_ga4_data_daily(event):
    """
    Function to be triggered daily for syncing GA4 data to MySQL.
    """
    log_id = str(uuid.uuid4())  # Generate a unique log ID
    logger.info(f"[{log_id}] Starting daily sync for all accounts.")
    run_data_sync(log_id, secret_conn)
    logger.info(f"[{log_id}] Daily sync for all accounts completed.")


@app.schedule('cron(0 0 1 * ? *)')
def sync_ga4_data_monthly(event):
    """
    Function to be triggered every 30 days to sync GA4 data for the past month.
    """
    log_id = str(uuid.uuid4())  # Generate a unique log ID
    logger.info(f"[{log_id}] Starting monthly sync.")
    run_data_sync(log_id, secret_conn, start_date="30daysAgo", end_date="yesterday")
    logger.info(f"[{log_id}] Monthly sync completed successfully.")


@app.route('/sync-data', methods=['POST'])
def sync_custom_ga4_data():
    """
    Endpoint to sync GA4 data for a custom date range.
    """
    log_id = str(uuid.uuid4())  # Generate a unique log ID
    logger.info(f"[{log_id}] Starting custom sync.")
    request = app.current_request
    start_date, end_date, account_id, property_id = parse_request_body(log_id, request)
    run_data_sync(log_id, secret_conn, start_date, end_date, account_id, property_id)
    logger.info(f"[{log_id}] Custom sync completed successfully.")
    return {'message': f'Successfully synced data from {start_date} to {end_date}.'}
