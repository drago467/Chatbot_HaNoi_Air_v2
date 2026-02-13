-- View: District-level current air quality insights (virtual districts)
-- Aggregate từ ward/xã trong cửa sổ 60 phút gần nhất.

CREATE OR REPLACE VIEW vw_district_now_insights AS
WITH district_members AS (
    SELECT
        dm.district_location_id,
        dm.ward_location_id
    FROM location_district_membership dm
),
latest_ward_obs AS (
    SELECT
        oc.location_id      AS ward_location_id,
        oc.ts_utc,
        oc.field,
        oc.value,
        oc.unit,
        ROW_NUMBER() OVER (
            PARTITION BY oc.location_id, oc.field
            ORDER BY oc.ts_utc DESC
        ) AS rn
    FROM observations_canonical oc
    WHERE oc.ts_utc >= NOW() - INTERVAL '60 minutes'
),
ward_latest AS (
    SELECT
        ward_location_id,
        ts_utc,
        field,
        value,
        unit
    FROM latest_ward_obs
    WHERE rn = 1
)
SELECT
    d.district_location_id,
    ld.name_vi        AS district_name_vi,
    ld.name_norm      AS district_name_norm,
    ld.admin_path     AS admin_path,
    w.field           AS field,
    AVG(w.value)      AS value_mean,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY w.value) AS p25,
    PERCENTILE_CONT(0.5)  WITHIN GROUP (ORDER BY w.value) AS p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY w.value) AS p75,
    COUNT(DISTINCT d.ward_location_id) AS wards_total,
    COUNT(DISTINCT w.ward_location_id) AS wards_with_data,
    CASE
        WHEN COUNT(DISTINCT d.ward_location_id) = 0 THEN 0
        ELSE (COUNT(DISTINCT w.ward_location_id)::NUMERIC
              / COUNT(DISTINCT d.ward_location_id)::NUMERIC) * 100.0
    END AS coverage_pct,
    CASE
        WHEN COUNT(DISTINCT d.ward_location_id) = 0 THEN 'insufficient'
        WHEN (COUNT(DISTINCT w.ward_location_id)::NUMERIC
              / COUNT(DISTINCT d.ward_location_id)::NUMERIC) * 100.0 < 30
            THEN 'insufficient'
        WHEN (COUNT(DISTINCT w.ward_location_id)::NUMERIC
              / COUNT(DISTINCT d.ward_location_id)::NUMERIC) * 100.0 < 60
            THEN 'low'
        ELSE 'high'
    END AS quality,
    'wards_communes' AS aggregated_from,
    60               AS time_window_minutes
FROM district_members d
JOIN locations ld
    ON ld.location_id = d.district_location_id
LEFT JOIN ward_latest w
    ON w.ward_location_id = d.ward_location_id
GROUP BY
    d.district_location_id,
    ld.name_vi,
    ld.name_norm,
    ld.admin_path,
    w.field;

