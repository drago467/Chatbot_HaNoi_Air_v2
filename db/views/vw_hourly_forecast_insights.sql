-- View: vw_hourly_forecast_insights
-- Mục đích: Trả về insights cho hourly forecast với timezone VN, uncertainty, best windows, trend

CREATE OR REPLACE VIEW vw_hourly_forecast_insights AS
WITH forecast_with_local_time AS (
    SELECT 
        fc.location_id,
        fc.field,
        fc.value,
        fc.unit,
        fc.target_ts_utc,
        -- Convert UTC sang local time (UTC+7)
        (fc.target_ts_utc AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh')::TIMESTAMPTZ AS target_ts_local,
        EXTRACT(HOUR FROM (fc.target_ts_utc AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh'))::INTEGER AS hour_local,
        fc.issue_ts_utc,
        fc.provenance
    FROM forecasts_canonical fc
    WHERE fc.target_ts_utc >= NOW()
      AND fc.target_ts_utc <= NOW() + INTERVAL '72 hours'  -- 3 ngày forecast
),
with_uncertainty AS (
    -- Tính uncertainty từ nhiều nguồn (nếu có)
    -- Tạm thời dùng single source, sau có thể mở rộng
    SELECT 
        fw.*,
        -- Nếu có nhiều nguồn trong provenance, có thể tính percentile
        -- Tạm thời dùng value làm p50
        fw.value AS uncertainty_p50,
        fw.value * 0.9 AS uncertainty_p10,  -- Giả định ±10%
        fw.value * 1.1 AS uncertainty_p90
    FROM forecast_with_local_time fw
),
with_trend AS (
    SELECT 
        wu.*,
        -- Tính trend slope từ 6h trước (linear regression đơn giản)
        -- Lấy giá trị 6h trước
        (SELECT fw2.value 
         FROM forecast_with_local_time fw2
         WHERE fw2.location_id = wu.location_id
           AND fw2.field = wu.field
           AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
           AND fw2.target_ts_utc < wu.target_ts_utc
         ORDER BY fw2.target_ts_utc DESC
         LIMIT 1) AS value_6h_ago,
        -- Trend change pct
        CASE 
            WHEN (SELECT fw2.value 
                  FROM forecast_with_local_time fw2
                  WHERE fw2.location_id = wu.location_id
                    AND fw2.field = wu.field
                    AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
                    AND fw2.target_ts_utc < wu.target_ts_utc
                  ORDER BY fw2.target_ts_utc DESC
                  LIMIT 1) IS NOT NULL
            THEN ((wu.value - (SELECT fw2.value 
                               FROM forecast_with_local_time fw2
                               WHERE fw2.location_id = wu.location_id
                                 AND fw2.field = wu.field
                                 AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
                                 AND fw2.target_ts_utc < wu.target_ts_utc
                               ORDER BY fw2.target_ts_utc DESC
                               LIMIT 1)) / 
                  NULLIF((SELECT fw2.value 
                          FROM forecast_with_local_time fw2
                          WHERE fw2.location_id = wu.location_id
                            AND fw2.field = wu.field
                            AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
                            AND fw2.target_ts_utc < wu.target_ts_utc
                          ORDER BY fw2.target_ts_utc DESC
                          LIMIT 1), 0)) * 100.0
            ELSE NULL
        END AS trend_change_pct,
        -- Trend slope (đơn giản: delta / 6h)
        CASE 
            WHEN (SELECT fw2.value 
                  FROM forecast_with_local_time fw2
                  WHERE fw2.location_id = wu.location_id
                    AND fw2.field = wu.field
                    AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
                    AND fw2.target_ts_utc < wu.target_ts_utc
                  ORDER BY fw2.target_ts_utc DESC
                  LIMIT 1) IS NOT NULL
            THEN (wu.value - (SELECT fw2.value 
                              FROM forecast_with_local_time fw2
                              WHERE fw2.location_id = wu.location_id
                                AND fw2.field = wu.field
                                AND fw2.target_ts_utc >= wu.target_ts_utc - INTERVAL '6 hours'
                                AND fw2.target_ts_utc < wu.target_ts_utc
                              ORDER BY fw2.target_ts_utc DESC
                              LIMIT 1)) / 6.0
            ELSE NULL
        END AS trend_slope
    FROM with_uncertainty wu
),
with_trend_label AS (
    SELECT 
        wt.*,
        -- Trend label
        CASE 
            WHEN wt.trend_change_pct IS NULL THEN 'stable'
            WHEN ABS(wt.trend_change_pct) < 5.0 THEN 'stable'
            WHEN wt.trend_change_pct > 0 THEN 'up'
            ELSE 'down'
        END AS trend_label
    FROM with_trend wt
),
with_best_windows AS (
    -- Tính best window (2h window với min AQI, tránh giờ cao điểm 7-9h, 17-19h)
    SELECT 
        wtt.*,
        -- Best window sẽ được tính trong Python query service
        -- Vì cần rolling window 2h và filter theo time_of_day_preference
        NULL::TEXT AS best_window_start,
        NULL::TEXT AS best_window_end,
        NULL::TEXT AS best_window_reason
    FROM with_trend_label wtt
)
SELECT 
    wbw.location_id,
    l.name_vi AS location_name,
    l.type AS location_type,
    l.admin_path,
    wbw.field,
    wbw.value,
    wbw.unit,
    wbw.target_ts_utc,
    wbw.target_ts_local,
    wbw.hour_local,
    wbw.uncertainty_p10,
    wbw.uncertainty_p50,
    wbw.uncertainty_p90,
    wbw.trend_slope,
    wbw.trend_change_pct,
    wbw.trend_label,
    wbw.best_window_start,
    wbw.best_window_end,
    wbw.best_window_reason
FROM with_best_windows wbw
JOIN locations l ON l.location_id = wbw.location_id;

COMMENT ON VIEW vw_hourly_forecast_insights IS 
'View trả về insights cho hourly forecast: timezone VN, uncertainty, trend, best windows';
