-- View: vw_trend_insights
-- Mục đích: Trả về thống kê trend cho các window khác nhau (last_24h, last_7d, this_week, last_week, this_month)
-- Note: View này sẽ được query với parameters, nên tạm thời tạo function thay vì view

-- Function để tính trend insights cho một window cụ thể
CREATE OR REPLACE FUNCTION get_trend_insights(
    p_location_id INTEGER,
    p_field TEXT,
    p_window_type TEXT,
    p_time_granularity TEXT DEFAULT 'hour'
)
RETURNS TABLE(
    location_id INTEGER,
    field TEXT,
    window_type TEXT,
    time_granularity TEXT,
    current_avg NUMERIC,
    previous_avg NUMERIC,
    delta_abs NUMERIC,
    delta_pct NUMERIC,
    max_value NUMERIC,
    p95_value NUMERIC,
    exceedance_days INTEGER,
    exceedance_hours INTEGER,
    best_hour_of_day INTEGER,
    best_hour_avg NUMERIC,
    diurnal_pattern JSONB
) AS $$
DECLARE
    v_current_start TIMESTAMPTZ;
    v_current_end TIMESTAMPTZ;
    v_previous_start TIMESTAMPTZ;
    v_previous_end TIMESTAMPTZ;
    v_threshold NUMERIC;
BEGIN
    -- Xác định time window dựa trên p_window_type
    CASE p_window_type
        WHEN 'last_24h' THEN
            v_current_start := NOW() - INTERVAL '24 hours';
            v_current_end := NOW();
            v_previous_start := NOW() - INTERVAL '48 hours';
            v_previous_end := NOW() - INTERVAL '24 hours';
        WHEN 'last_7d' THEN
            v_current_start := NOW() - INTERVAL '7 days';
            v_current_end := NOW();
            v_previous_start := NOW() - INTERVAL '14 days';
            v_previous_end := NOW() - INTERVAL '7 days';
        WHEN 'this_week' THEN
            -- Tuần này = Monday đến hiện tại (local timezone)
            v_current_start := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
            v_current_end := NOW();
            -- Tuần trước = Monday đến Sunday của tuần trước
            v_previous_start := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ - INTERVAL '7 days';
            v_previous_end := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
        WHEN 'this_week_vs_last_week' THEN
            -- Giống this_week nhưng tên khác
            v_current_start := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
            v_current_end := NOW();
            v_previous_start := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ - INTERVAL '7 days';
            v_previous_end := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
        WHEN 'last_week' THEN
            -- Tuần trước = Monday đến Sunday của tuần trước
            v_previous_start := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ - INTERVAL '7 days';
            v_previous_end := DATE_TRUNC('week', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
            v_current_start := v_previous_start;
            v_current_end := v_previous_end;
        WHEN 'this_month' THEN
            v_current_start := DATE_TRUNC('month', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ;
            v_current_end := NOW();
            v_previous_start := DATE_TRUNC('month', (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'))::TIMESTAMPTZ - INTERVAL '1 month';
            v_previous_end := v_current_start;
        ELSE
            RAISE EXCEPTION 'Unknown window_type: %', p_window_type;
    END CASE;

    -- Lấy threshold cho exceedance
    v_threshold := get_who_threshold(p_field);
    IF v_threshold IS NULL AND p_field = 'aqi' THEN
        v_threshold := 150;  -- AQI warning threshold
    END IF;

    RETURN QUERY
    WITH current_window AS (
        SELECT 
            oc.value,
            EXTRACT(HOUR FROM (oc.ts_utc AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh'))::INTEGER AS hour_local
        FROM observations_canonical oc
        WHERE oc.location_id = p_location_id
          AND oc.field = p_field
          AND oc.ts_utc >= v_current_start
          AND oc.ts_utc < v_current_end
    ),
    previous_window AS (
        SELECT 
            oc.value
        FROM observations_canonical oc
        WHERE oc.location_id = p_location_id
          AND oc.field = p_field
          AND oc.ts_utc >= v_previous_start
          AND oc.ts_utc < v_previous_end
    ),
    current_stats AS (
        SELECT 
            AVG(cw.value)::NUMERIC AS current_avg,
            MAX(cw.value)::NUMERIC AS max_value,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY cw.value)::NUMERIC AS p95_value,
            COUNT(*) FILTER (WHERE v_threshold IS NOT NULL AND cw.value > v_threshold) AS exceedance_count
        FROM current_window cw
    ),
    previous_stats AS (
        SELECT 
            AVG(pw.value)::NUMERIC AS previous_avg
        FROM previous_window pw
    ),
    diurnal_pattern_data AS (
        SELECT 
            hour_local,
            AVG(value)::NUMERIC AS avg_value
        FROM current_window
        GROUP BY hour_local
        ORDER BY hour_local
    ),
    best_hour_data AS (
        SELECT 
            hour_local,
            AVG(value)::NUMERIC AS avg_value
        FROM current_window
        GROUP BY hour_local
        ORDER BY AVG(value) ASC
        LIMIT 1
    )
    SELECT 
        p_location_id,
        p_field,
        p_window_type,
        p_time_granularity,
        cs.current_avg,
        ps.previous_avg,
        (cs.current_avg - ps.previous_avg)::NUMERIC AS delta_abs,
        CASE WHEN ps.previous_avg != 0 
             THEN (((cs.current_avg - ps.previous_avg) / ps.previous_avg) * 100.0)::NUMERIC
             ELSE NULL
        END AS delta_pct,
        cs.max_value,
        cs.p95_value,
        -- Exceedance days/hours (tạm thời dùng count, có thể refine sau)
        CASE WHEN p_time_granularity = 'day' 
             THEN cs.exceedance_count::INTEGER
             ELSE NULL
        END AS exceedance_days,
        CASE WHEN p_time_granularity = 'hour' 
             THEN cs.exceedance_count::INTEGER
             ELSE NULL
        END AS exceedance_hours,
        COALESCE(bhd.hour_local, NULL)::INTEGER AS best_hour_of_day,
        bhd.avg_value AS best_hour_avg,
        -- Diurnal pattern as JSONB
        COALESCE(
            (SELECT jsonb_object_agg(hour_local::TEXT, avg_value)
             FROM diurnal_pattern_data),
            '{}'::jsonb
        ) AS diurnal_pattern
    FROM current_stats cs
    CROSS JOIN previous_stats ps
    LEFT JOIN best_hour_data bhd ON TRUE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_trend_insights IS 
'Function trả về trend insights cho một location, field, và window type cụ thể';
