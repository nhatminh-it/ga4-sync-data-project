CREATE DATABASE IF NOT EXISTS ga4_data;
USE ga4_data;

CREATE TABLE IF NOT EXISTS daily_metrics (
    date DATE,
    country VARCHAR(50),
    clicks INT,
    spend DECIMAL(10, 2),
    sales DECIMAL(10, 2),
    conversions INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (date, country)
);

CREATE INDEX idx_date_country ON daily_metrics (date, country);

