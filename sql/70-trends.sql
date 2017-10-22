CREATE TABLE trends (
    id          SERIAL NOT NULL PRIMARY KEY,
    pair_id     INTEGER NOT NULL REFERENCES pairs(id),
    ts1         FLOAT NOT NULL,
    ts2         FLOAT NOT NULL,
    actual      DECIMAL(12,8),
    predicted   DECIMAL(12,8)
);

CREATE INDEX ON trends(pair_id, ts1);

