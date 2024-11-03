CREATE DATABASE IF NOT EXISTS ga4_data;
USE ga4_data;

CREATE TABLE ga4_report (
    campaign_id BIGINT NOT NULL,                    -- campaignId
    campaign_name VARCHAR(255) NOT NULL,            -- campaignName
    start_date DATE NOT NULL,                        -- startDate
    end_date DATE NOT NULL,                          -- endDate
    sessions BIGINT NULL,                            -- sessions
    advertiser_ad_clicks BIGINT NULL,               -- advertiserAdClicks
    advertiser_ad_cost DOUBLE NULL,                  -- advertiserAdCost
    advertiser_ad_cost_per_click DOUBLE NULL,       -- advertiserAdCostPerClick
    advertiser_ad_impressions BIGINT NULL,          -- advertiserAdImpressions
    total_revenue DOUBLE NULL,                       -- totalRevenue
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (campaign_id, campaign_name, start_date, end_date)
);

CREATE INDEX idx_campaign_start_date ON ga4_report (campaign_id, start_date);


