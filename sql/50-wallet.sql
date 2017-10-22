CREATE TABLE wallet (
    sym     VARCHAR NOT NULL PRIMARY KEY,
    value   DECIMAL(12,8),
    data    JSONB
);

