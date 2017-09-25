CREATE TABLE historical (
    id      BIGSERIAL PRIMARY KEY,
    pair_id INTEGER NOT NULL REFERENCES pairs(id) ON DELETE CASCADE,
    value   DECIMAL(16,8) NOT NULL,
    volume  DECIMAL(16,8) NOT NULL,
    op      CHAR(1) NOT NULL,
    ts      FLOAT NOT NULL
);

CREATE INDEX ON historical(ts);
CREATE INDEX ON historical USING BRIN(pair_id);

