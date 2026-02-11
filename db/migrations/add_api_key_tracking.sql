-- Migration: Add API Key Tracking
-- Purpose: Track API key usage for multiple keys support and monitoring

-- 1) Add api_key_id column to api_requests table
ALTER TABLE api_requests 
ADD COLUMN IF NOT EXISTS api_key_id VARCHAR(64);

CREATE INDEX IF NOT EXISTS idx_api_requests_key_id 
ON api_requests (api_key_id);

-- 2) Create api_key_usage table for tracking per-key usage
CREATE TABLE IF NOT EXISTS api_key_usage (
    key_id VARCHAR(64) PRIMARY KEY,  -- e.g., 'openweather_key_0'
    source_id VARCHAR(64) NOT NULL REFERENCES api_sources(source_id),
    calls_today INTEGER DEFAULT 0,
    calls_this_minute INTEGER DEFAULT 0,
    last_reset_minute TIMESTAMPTZ,
    last_reset_day DATE,
    is_active BOOLEAN DEFAULT TRUE,
    error_count INTEGER DEFAULT 0,
    last_error_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_api_key_usage_source_active
ON api_key_usage (source_id, is_active);

CREATE INDEX IF NOT EXISTS idx_api_key_usage_reset_minute
ON api_key_usage (last_reset_minute);

-- 3) Function to reset minute counter (called periodically)
CREATE OR REPLACE FUNCTION reset_minute_counters()
RETURNS void AS $$
BEGIN
    UPDATE api_key_usage
    SET calls_this_minute = 0,
        last_reset_minute = NOW(),
        updated_at = NOW()
    WHERE last_reset_minute IS NULL 
       OR last_reset_minute < NOW() - INTERVAL '1 minute';
END;
$$ LANGUAGE plpgsql;

-- 4) Function to reset daily counter (called daily)
CREATE OR REPLACE FUNCTION reset_daily_counters()
RETURNS void AS $$
BEGIN
    UPDATE api_key_usage
    SET calls_today = 0,
        last_reset_day = CURRENT_DATE,
        updated_at = NOW()
    WHERE last_reset_day IS NULL 
       OR last_reset_day < CURRENT_DATE;
END;
$$ LANGUAGE plpgsql;

-- 5) Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_api_key_usage_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_api_key_usage_timestamp
BEFORE UPDATE ON api_key_usage
FOR EACH ROW
EXECUTE FUNCTION update_api_key_usage_timestamp();
