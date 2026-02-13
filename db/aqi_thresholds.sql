-- AQI và WHO thresholds cho PostgreSQL views
-- Dùng trong các view insights để tính exceedance, levels, rankings

-- AQI Levels (theo thang HanoiAir)
-- Tốt: 0-50
-- Trung bình: 51-100
-- Kém: 101-150
-- Xấu: 151-200
-- Rất xấu: 201-300
-- Nguy hại: >300

-- WHO 24h Guidelines (µg/m³)
-- PM2.5: 15 µg/m³
-- PM10: 45 µg/m³
-- O3 (8h): 100 µg/m³
-- NO2 (24h): 25 µg/m³

-- Function để lấy AQI level từ giá trị
CREATE OR REPLACE FUNCTION get_aqi_level(aqi_value NUMERIC)
RETURNS TEXT AS $$
BEGIN
    CASE
        WHEN aqi_value <= 50 THEN RETURN 'Tốt';
        WHEN aqi_value <= 100 THEN RETURN 'Trung bình';
        WHEN aqi_value <= 150 THEN RETURN 'Kém';
        WHEN aqi_value <= 200 THEN RETURN 'Xấu';
        WHEN aqi_value <= 300 THEN RETURN 'Rất xấu';
        ELSE RETURN 'Nguy hại';
    END CASE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function để lấy WHO threshold cho field
CREATE OR REPLACE FUNCTION get_who_threshold(field_name TEXT)
RETURNS NUMERIC AS $$
BEGIN
    CASE LOWER(field_name)
        WHEN 'pm25' THEN RETURN 15.0;
        WHEN 'pm10' THEN RETURN 45.0;
        WHEN 'o3' THEN RETURN 100.0;
        WHEN 'ozone' THEN RETURN 100.0;
        WHEN 'no2' THEN RETURN 25.0;
        WHEN 'nitrogen_dioxide' THEN RETURN 25.0;
        ELSE RETURN NULL;
    END CASE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function để check WHO exceedance
CREATE OR REPLACE FUNCTION check_who_exceedance(field_name TEXT, value NUMERIC)
RETURNS TABLE(exceedance_flag BOOLEAN, exceedance_ratio NUMERIC) AS $$
DECLARE
    threshold NUMERIC;
BEGIN
    threshold := get_who_threshold(field_name);
    
    IF threshold IS NULL THEN
        RETURN QUERY SELECT FALSE, NULL::NUMERIC;
    ELSE
        RETURN QUERY SELECT 
            (value > threshold) AS exceedance_flag,
            CASE WHEN threshold > 0 THEN value / threshold ELSE NULL END AS exceedance_ratio;
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function để xác định trend label từ delta
CREATE OR REPLACE FUNCTION get_trend_label(delta_1h NUMERIC, threshold_pct NUMERIC DEFAULT 5.0)
RETURNS TEXT AS $$
BEGIN
    IF delta_1h IS NULL THEN
        RETURN 'ổn định';
    END IF;
    
    IF ABS(delta_1h) < threshold_pct THEN
        RETURN 'ổn định';
    ELSIF delta_1h > 0 THEN
        RETURN 'tăng';
    ELSE
        RETURN 'giảm';
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
