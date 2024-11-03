import random
from datetime import datetime, timedelta
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_mock_data(log_id: str) -> list:
    """
    Generate mock data for GA4 API response.

    Args:
        log_id (str): A unique identifier for logging purposes.

    Returns:
        list: A list of mock data dictionaries for testing purposes.
    """
    mock_data = []
    today = datetime.now().date()

    for i in range(5):
        campaign_id = random.randint(1000, 99999)
        campaign_name = f"Mock Campaign {i + 1}"
        end_date = today - timedelta(days=i)
        start_date = end_date - timedelta(days=1)

        sessions = random.randint(100, 1000)
        advertiser_ad_clicks = random.randint(10, 100)
        advertiser_ad_cost = random.uniform(100.0, 500.0)
        advertiser_ad_cost_per_click = advertiser_ad_cost / advertiser_ad_clicks if advertiser_ad_clicks > 0 else 0
        advertiser_ad_impressions = random.randint(1000, 5000)
        total_revenue = random.uniform(50.0, 200.0)

        mock_data.append({
            'dimensionValues': [
                {},  # Placeholder for other dimensions
                {'value': end_date.strftime('%Y%m%d')},  # date
                {'value': campaign_id},  # campaignId
                {'value': campaign_name},  # campaignName
            ],
            'metricValues': [
                {'value': sessions},  # sessions
                {'value': advertiser_ad_clicks},  # advertiser_ad_clicks
                {'value': advertiser_ad_cost},  # advertiser_ad_cost
                {'value': advertiser_ad_cost_per_click},  # advertiser_ad_cost_per_click
                {'value': advertiser_ad_impressions},  # advertiser_ad_impressions
                {'value': total_revenue},  # total_revenue
            ]
        })

    logger.info(f"[{log_id}] Generated mock data: {mock_data}")
    return mock_data
