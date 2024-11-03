import requests

def fetch_ga4_data(property_id, access_token, start_date="7daysAgo", end_date="yesterday"):
    """
    Fetch data from GA4 API using the specified property ID and access token.

    Args:
        property_id (str): The GA4 property ID.
        access_token (str): The OAuth 2.0 access token.
        start_date (str): The start date for the report.
        end_date (str): The end date for the report.

    Returns:
        list: Rows of data from the GA4 API response.
    """
    api_url = f'https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    request_body = {
        "dimensions": [
            {"name": "campaignId"},
            {"name": "campaignName"},
            {"name": "date"}
        ],
        "metrics": [
            {"name": "sessions"},
            {"name": "advertiserAdClicks"},
            {"name": "advertiserAdCost"},
            {"name": "advertiserAdCostPerClick"},
            {"name": "advertiserAdImpressions"},
            {"name": "totalRevenue"},
        ],
        "dateRanges": [{"startDate": start_date, "endDate": end_date}]
    }

    response = requests.post(api_url, headers=headers, json=request_body)

    if response.status_code != 200:
        raise Exception(f"Error fetching data from GA4 API: {response.text}")

    return response.json().get('rows', [])
