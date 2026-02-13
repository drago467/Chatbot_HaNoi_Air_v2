-- View: vw_current_air_quality_insights
-- Mục đích: Trả về insights cho air quality hiện tại (snapshot mới nhất)
-- Bao gồm: value, minutes_ago, aqi_level, who_exceedance, delta, ranking, percentile

-- Cần chạy db/aqi_thresholds.sql trước để có các functions

CREATE OR REPLACE VIEW vw_current_air_quality_insights AS
WITH latest_snapshots AS (
    -- Lấy snapshot mới nhất cho mỗi (location_id, field) trong cửa sổ ±1h
    SELECT DISTINCT ON (location_id, field)
        oc.location_id,
        oc.field,
        oc.value,
        oc.unit,
        oc.ts_utc,
        EXTRACT(EPOCH FROM (NOW() - oc.ts_utc)) / 60.0 AS minutes_ago
    FROM observations_canonical oc
    WHERE oc.ts_utc >= NOW() - INTERVAL '1 hour'
    ORDER BY oc.location_id, oc.field, oc.ts_utc DESC
),
with_deltas AS (
    -- Tính delta so với 1h, 2h, 3h trước
    SELECT 
        ls.*,
        -- Lấy giá trị 1h trước (query riêng vì cần chính xác 1h trước, không phải row trước)
        (SELECT oc1.value 
         FROM observations_canonical oc1
         WHERE oc1.location_id = ls.location_id
           AND oc1.field = ls.field
           AND oc1.ts_utc >= ls.ts_utc - INTERVAL '1 hour 30 minutes'
           AND oc1.ts_utc < ls.ts_utc - INTERVAL '30 minutes'
         ORDER BY oc1.ts_utc DESC
         LIMIT 1) AS value_1h_ago,
        -- Lấy giá trị 2h trước
        (SELECT oc2.value 
         FROM observations_canonical oc2
         WHERE oc2.location_id = ls.location_id
           AND oc2.field = ls.field
           AND oc2.ts_utc >= ls.ts_utc - INTERVAL '2 hours 30 minutes'
           AND oc2.ts_utc < ls.ts_utc - INTERVAL '1 hour 30 minutes'
         ORDER BY oc2.ts_utc DESC
         LIMIT 1) AS value_2h_ago,
        -- Lấy giá trị 3h trước
        (SELECT oc3.value 
         FROM observations_canonical oc3
         WHERE oc3.location_id = ls.location_id
           AND oc3.field = ls.field
           AND oc3.ts_utc >= ls.ts_utc - INTERVAL '3 hours 30 minutes'
           AND oc3.ts_utc < ls.ts_utc - INTERVAL '2 hours 30 minutes'
         ORDER BY oc3.ts_utc DESC
         LIMIT 1) AS value_3h_ago
    FROM latest_snapshots ls
),
with_calculations AS (
    SELECT 
        wd.*,
        -- Delta 1h, 2h, 3h
        CASE WHEN wd.value_1h_ago IS NOT NULL 
             THEN wd.value - wd.value_1h_ago 
             ELSE NULL 
        END AS delta_1h,
        CASE WHEN wd.value_2h_ago IS NOT NULL 
             THEN wd.value - wd.value_2h_ago 
             ELSE NULL 
        END AS delta_2h,
        CASE WHEN wd.value_3h_ago IS NOT NULL 
             THEN wd.value - wd.value_3h_ago 
             ELSE NULL 
        END AS delta_3h,
        -- Delta 1h phần trăm
        CASE WHEN wd.value_1h_ago IS NOT NULL AND wd.value_1h_ago != 0
             THEN ((wd.value - wd.value_1h_ago) / wd.value_1h_ago) * 100.0
             ELSE NULL
        END AS delta_1h_pct,
        -- AQI level (chỉ cho field = 'aqi')
        CASE WHEN wd.field = 'aqi' 
             THEN get_aqi_level(wd.value)
             ELSE NULL
        END AS aqi_level,
        -- WHO exceedance
        (check_who_exceedance(wd.field, wd.value)).exceedance_flag AS who_exceedance_flag,
        (check_who_exceedance(wd.field, wd.value)).exceedance_ratio AS exceedance_ratio,
        -- Trend label
        get_trend_label(
            CASE WHEN wd.value_1h_ago IS NOT NULL 
                 THEN ((wd.value - wd.value_1h_ago) / NULLIF(wd.value_1h_ago, 0)) * 100.0
                 ELSE NULL
            END
        ) AS trend_label
    FROM with_deltas wd
),
with_rankings AS (
    SELECT 
        wc.*,
        -- Ranking citywide (toàn Hà Nội)
        RANK() OVER (
            PARTITION BY wc.field 
            ORDER BY wc.value DESC
        ) AS rank_citywide,
        PERCENT_RANK() OVER (
            PARTITION BY wc.field 
            ORDER BY wc.value DESC
        ) AS percentile_citywide,
        -- Ranking theo scope (có thể filter sau trong Python)
        -- Tạm thời dùng citywide, scope sẽ được filter trong query service
        RANK() OVER (
            PARTITION BY wc.field 
            ORDER BY wc.value DESC
        ) AS rank_scope,
        PERCENT_RANK() OVER (
            PARTITION BY wc.field 
            ORDER BY wc.value DESC
        ) AS percentile_scope
    FROM with_calculations wc
)
SELECT 
    wr.location_id,
    l.name_vi AS location_name,
    l.type AS location_type,
    l.admin_path,
    wr.field,
    wr.value,
    wr.unit,
    wr.ts_utc,
    wr.minutes_ago,
    wr.aqi_level,
    wr.who_exceedance_flag,
    wr.exceedance_ratio,
    wr.delta_1h,
    wr.delta_2h,
    wr.delta_3h,
    wr.delta_1h_pct,
    wr.trend_label,
    wr.rank_citywide,
    wr.percentile_citywide,
    wr.rank_scope,
    wr.percentile_scope
FROM with_rankings wr
JOIN locations l ON l.location_id = wr.location_id;

COMMENT ON VIEW vw_current_air_quality_insights IS 
'View trả về insights cho air quality hiện tại: value, minutes_ago, aqi_level, who_exceedance, delta, ranking, percentile';
