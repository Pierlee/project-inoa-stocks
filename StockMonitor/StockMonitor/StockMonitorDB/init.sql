
CREATE TABLE TrackedStocks (
    StockName VARCHAR(100) NOT NULL PRIMARY KEY,
    CreationDate TIMESTAMP(3) NOT NULL,
    MinValue NUMERIC(6,2) NOT NULL,
    MaxValue NUMERIC(6,2) NOT NULL
);

CREATE TABLE StocksHistory (
    StockName VARCHAR(100) NOT NULL,
    Timestamp TIMESTAMP(3) NOT NULL,
    CurrentValue NUMERIC(6,2) NOT NULL,
    FOREIGN KEY (StockName)
    REFERENCES TrackedStocks (StockName)
    ON DELETE CASCADE,
    CONSTRAINT PK_Stocks_History PRIMARY KEY (StockName, Timestamp)
);