def insert_data_into_db(conn, parsed_data):
    """
    Inserts data into the MySQL database.
    """
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO daily_metrics (date, country, clicks, spend, sales, conversions, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    ON DUPLICATE KEY UPDATE 
        clicks = VALUES(clicks),
        spend = VALUES(spend),
        sales = VALUES(sales),
        conversions = VALUES(conversions),
        updated_at = NOW()
    """

    for data in parsed_data:
        cursor.execute(insert_query, (
            data["date"],
            data["country"],
            data["clicks"],
            data["spend"],
            data["sales"],
            data["conversions"]
        ))

    conn.commit()
    print(f"{cursor.rowcount} records inserted/updated successfully.")

    conn.commit()
    cursor.close()


def parse_ga4_response(response_rows):
    """
    Parse the GA4 API response rows to extract date, country, and metrics.
    """
    parsed_data = []
    for row in response_rows:
        date = row.dimension_values[0].value  # Ngày
        country = row.dimension_values[1].value  # Quốc gia

        clicks = int(row.metric_values[0].value)
        spend = float(row.metric_values[1].value)
        sales = float(row.metric_values[2].value)
        conversions = int(row.metric_values[3].value)

        parsed_data.append({
            "date": date,
            "country": country,
            "clicks": clicks,
            "spend": spend,
            "sales": sales,
            "conversions": conversions
        })

    return parsed_data
