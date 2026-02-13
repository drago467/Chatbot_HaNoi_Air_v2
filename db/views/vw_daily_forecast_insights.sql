-- View: vw_daily_forecast_insights
-- Mục đích: Trả về insights cho daily forecast (aggregate từ hourly)

CREATE OR REPLACE VIEW vw_daily_forecast_insights AS
WITH hourly_forecast AS (
    SELECT 
        fc.location_id,
        fc.field,
        fc.target_ts_utc,
        (fc.target_ts_utc AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh')::DATE AS target_date_local,
        fc.value
    FROM forecasts_canonical fc
    WHERE fc.target_ts_utc >= NOW()
      AND fc.target_ts_utc <= NOW() + INTERVAL '7 days'
),
daily_aggregates AS (
    SELECT 
        hf.location_id,
        hf.field,
        hf.target_date_local,
        TO_CHAR(hf.target_date_local, 'Day') AS day_of_week_local,
        AVG(hf.value) AS value_avg,
        MIN(hf.value) AS value_min,
        MAX(hf.value) AS value_max,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY hf.value) AS value_p95
    FROM hourly_forecast hf
    GROUP BY hf.location_id, hf.field, hf.target_date_local
),
with_flags AS (
    SELECT 
        da.*,
        -- Best day flag (ngày có value_avg thấp nhất trong window)
        CASE 
            WHEN da.value_avg = (SELECT MIN(da2.value_avg) 
                                 FROM daily_aggregates da2 
                                 WHERE da2.location_id = da.location_id 
                                   AND da2.field = da.field
                                   AND da2.target_date_local >= CURRENT_DATE
                                   AND da2.target_date_local <= CURRENT_DATE + INTERVAL '7 days')
            THEN TRUE
            ELSE FALSE
        END AS best_day_flag,
        -- Worst day flag
        CASE 
            WHEN da.value_avg = (SELECT MAX(da2.value_avg) 
                                 FROM daily_aggregates da2 
                                 WHERE da2.location_id = da.location_id 
                                   AND da2.field = da.field
                                   AND da2.target_date_local >= CURRENT_DATE
                                   AND da2.target_date_local <= CURRENT_DATE + INTERVAL '7 days')
            THEN TRUE
            ELSE FALSE
        END AS worst_day_flag,
        -- Exceedance risk (AQI > 150 hoặc PM > WHO threshold)
        CASE 
            WHEN da.field = 'aqi' AND da.value_avg > 150 THEN TRUE
            WHEN da.field IN ('pm25', 'pm10', 'o3', 'no2') 
                 AND da.value_avg > COALESCE(get_who_threshold(da.field), 0) THEN TRUE
            ELSE FALSE
        END AS exceedance_risk
    FROM daily_aggregates da
)
SELECT 
    wf.location_id,
    l.name_vi AS location_name,
    l.type AS location_type,
    l.admin_path,
    wf.field,
    wf.target_date_local,
    wf.day_of_week_local,
    wf.value_avg,
    wf.value_min,
    wf.value_max,
    wf.value_p95,
    wf.best_day_flag,
    wf.worst_day_flag,
    wf.exceedance_risk
FROM with_flags wf
JOIN locations l ON l.location_id = wf.location_id;

COMMENT ON VIEW vw_daily_forecast_insights IS 
'View trả về insights cho daily forecast: aggregates, best/worst day flags, exceedance risk';
