-- PostgreSQL schema for Hanoi Air Chatbot
-- Core data tables (A1) + Logging & Evaluation tables (A2)

-- 1) Dimension: locations

CREATE TABLE IF NOT EXISTS locations (
    location_id         SERIAL PRIMARY KEY,
    hanoiair_internal_id VARCHAR(50) UNIQUE,
    hanoiair_admin_id    VARCHAR(50),
    name_vi              VARCHAR(255) NOT NULL,
    name_norm            VARCHAR(255) NOT NULL,
    type                 VARCHAR(20) NOT NULL, -- 'city' | 'ward'
    lat                  DOUBLE PRECISION,
    lon                  DOUBLE PRECISION,
    bbox                 JSONB,                -- {minx, miny, maxx, maxy}
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_locations_name_norm
    ON locations (name_norm);


-- 2) Dimension: api_sources

CREATE TABLE IF NOT EXISTS api_sources (
    source_id            VARCHAR(64) PRIMARY KEY, -- e.g. 'openweather_onecall'
    source_name          TEXT NOT NULL,
    api_version          VARCHAR(32),
    base_url             TEXT,
    rate_limit_per_day   INTEGER,
    rate_limit_per_minute INTEGER,
    notes                TEXT
);


-- 3) Raw ingestion: api_requests / api_responses

CREATE TABLE IF NOT EXISTS api_requests (
    request_id           SERIAL PRIMARY KEY,
    source_id            VARCHAR(64) REFERENCES api_sources(source_id),
    endpoint             TEXT NOT NULL,
    http_method          VARCHAR(10) NOT NULL DEFAULT 'GET',
    params               JSONB,
    requested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    http_status          INTEGER,
    latency_ms           INTEGER,
    response_size_bytes  INTEGER
);

CREATE INDEX IF NOT EXISTS idx_api_requests_source_time
    ON api_requests (source_id, requested_at);


CREATE TABLE IF NOT EXISTS api_responses (
    response_id          SERIAL PRIMARY KEY,
    request_id           INTEGER UNIQUE REFERENCES api_requests(request_id) ON DELETE CASCADE,
    received_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    body_json            JSONB NOT NULL,
    body_hash            VARCHAR(128),
    parse_status         VARCHAR(20),  -- 'pending' | 'success' | 'error'
    parse_error_message  TEXT
);

CREATE INDEX IF NOT EXISTS idx_api_responses_hash
    ON api_responses (body_hash);


-- 4) Parsed observations / forecasts (source-specific)

CREATE TABLE IF NOT EXISTS observations_raw (
    obs_id               SERIAL PRIMARY KEY,
    location_id          INTEGER REFERENCES locations(location_id),
    ts_utc               TIMESTAMPTZ NOT NULL,
    field                VARCHAR(64) NOT NULL,  -- canonical field name
    value                NUMERIC,
    unit                 VARCHAR(32),
    source_id            VARCHAR(64) REFERENCES api_sources(source_id),
    response_id          INTEGER REFERENCES api_responses(response_id) ON DELETE SET NULL,
    quality_flags        JSONB,                -- {missing, outlier, interpolated, ...}
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_observations_raw UNIQUE (location_id, ts_utc, field, source_id)
);

CREATE INDEX IF NOT EXISTS idx_observations_raw_loc_time_field_source
    ON observations_raw (location_id, ts_utc, field, source_id);


CREATE TABLE IF NOT EXISTS forecasts_raw (
    forecast_id          SERIAL PRIMARY KEY,
    location_id          INTEGER REFERENCES locations(location_id),
    issue_ts_utc         TIMESTAMPTZ NOT NULL,
    target_ts_utc        TIMESTAMPTZ NOT NULL,
    field                VARCHAR(64) NOT NULL,
    value                NUMERIC,
    unit                 VARCHAR(32),
    source_id            VARCHAR(64) REFERENCES api_sources(source_id),
    response_id          INTEGER REFERENCES api_responses(response_id) ON DELETE SET NULL,
    forecast_horizon_hours INTEGER,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_forecasts_raw UNIQUE (location_id, issue_ts_utc, target_ts_utc, field, source_id)
);

CREATE INDEX IF NOT EXISTS idx_forecasts_raw_loc_issue_target_field_source
    ON forecasts_raw (location_id, issue_ts_utc, target_ts_utc, field, source_id);


-- 5) Canonical observations / forecasts (unified view for runtime)

CREATE TABLE IF NOT EXISTS observations_canonical (
    canonical_id         SERIAL PRIMARY KEY,
    location_id          INTEGER REFERENCES locations(location_id),
    ts_utc               TIMESTAMPTZ NOT NULL,
    field                VARCHAR(64) NOT NULL,
    value                NUMERIC,
    unit                 VARCHAR(32),
    provenance           JSONB NOT NULL,  -- {selected_source, raw_obs_ids[], fusion_method, confidence, freshness_window_minutes}
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_observations_canonical UNIQUE (location_id, ts_utc, field)
);

CREATE INDEX IF NOT EXISTS idx_observations_canonical_time
    ON observations_canonical (ts_utc);


CREATE TABLE IF NOT EXISTS forecasts_canonical (
    canonical_forecast_id SERIAL PRIMARY KEY,
    location_id           INTEGER REFERENCES locations(location_id),
    issue_ts_utc          TIMESTAMPTZ, -- last issue time used for this snapshot (optional metadata)
    target_ts_utc         TIMESTAMPTZ NOT NULL,
    field                 VARCHAR(64) NOT NULL,
    value                 NUMERIC,
    unit                  VARCHAR(32),
    provenance            JSONB NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- For chatbot explain, we care about the latest snapshot per (location, target time, field),
    -- không cần phân biệt mọi issue_ts chạy mô hình dự báo.
    CONSTRAINT uq_forecasts_canonical UNIQUE (location_id, target_ts_utc, field)
);

CREATE INDEX IF NOT EXISTS idx_forecasts_canonical_target_time
    ON forecasts_canonical (target_ts_utc);


-- 6) Evaluation runs (group experiments / evaluation sessions)

CREATE TABLE IF NOT EXISTS eval_runs (
    run_id              SERIAL PRIMARY KEY,
    name                VARCHAR(128) NOT NULL,
    description         TEXT,
    ckg_version         VARCHAR(64),
    mapping_version     VARCHAR(64),
    code_version        VARCHAR(64),
    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ,
    notes               TEXT
);


-- 7) Chat turns (user-facing interactions)

CREATE TABLE IF NOT EXISTS chat_turns (
    turn_id             SERIAL PRIMARY KEY,
    run_id              INTEGER REFERENCES eval_runs(run_id) ON DELETE SET NULL,
    user_query          TEXT NOT NULL,
    resolved_intent     VARCHAR(64),
    resolved_location_id INTEGER REFERENCES locations(location_id),
    resolved_time       TIMESTAMPTZ,
    response_text       TEXT,
    model_name          VARCHAR(128),
    latency_ms          INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    meta                JSONB
);

CREATE INDEX IF NOT EXISTS idx_chat_turns_run_intent
    ON chat_turns (run_id, resolved_intent);


-- 8) Condition evaluations (ConditionEvaluator logs)

CREATE TABLE IF NOT EXISTS condition_evaluations (
    eval_id             SERIAL PRIMARY KEY,
    run_id              INTEGER REFERENCES eval_runs(run_id) ON DELETE SET NULL,
    turn_id             INTEGER REFERENCES chat_turns(turn_id) ON DELETE SET NULL,
    location_id         INTEGER REFERENCES locations(location_id),
    ts_utc              TIMESTAMPTZ NOT NULL,
    evaluated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    relationship_id     VARCHAR(100) NOT NULL,
    condition_index     INTEGER NOT NULL,
    result              VARCHAR(20) NOT NULL, -- 'true' | 'false' | 'unknown' | etc.
    evidence_score      NUMERIC,             -- optional per-condition or relationship-level
    observed_value      NUMERIC,
    observed_unit       VARCHAR(32),
    expected_value      JSONB,
    expected_operator   VARCHAR(16),
    snapshot_fields_used JSONB,
    notes               TEXT,
    evaluation_latency_ms INTEGER,
    CONSTRAINT uq_condition_eval UNIQUE (run_id, location_id, ts_utc, relationship_id, condition_index)
);

CREATE INDEX IF NOT EXISTS idx_condition_eval_run_rel
    ON condition_evaluations (run_id, relationship_id, condition_index);

CREATE INDEX IF NOT EXISTS idx_condition_eval_loc_time
    ON condition_evaluations (location_id, ts_utc, evaluated_at);

CREATE INDEX IF NOT EXISTS idx_condition_eval_rel_result
    ON condition_evaluations (relationship_id, result);


-- 9) Explanations (final causal/knowledge/what-if answers)

CREATE TABLE IF NOT EXISTS explanations (
    explanation_id      SERIAL PRIMARY KEY,
    run_id              INTEGER REFERENCES eval_runs(run_id) ON DELETE SET NULL,
    turn_id             INTEGER UNIQUE REFERENCES chat_turns(turn_id) ON DELETE CASCADE,
    location_id         INTEGER REFERENCES locations(location_id),
    ts_utc              TIMESTAMPTZ,
    explanation_type    VARCHAR(32),  -- 'causal_now' | 'causal_knowledge' | 'what_if' | ...
    explanation_text    TEXT NOT NULL,
    top_relationship_ids JSONB,       -- array of relationship_id
    relationship_evidence JSONB,      -- array of {relationship_id, evidence_score, ...}
    citations           JSONB,        -- array of {source_id, authors, year, title}
    confidence_score    NUMERIC,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_explanations_run_type
    ON explanations (run_id, explanation_type);

CREATE INDEX IF NOT EXISTS idx_explanations_loc_time
    ON explanations (location_id, ts_utc);

