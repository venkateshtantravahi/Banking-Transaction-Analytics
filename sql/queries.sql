-- total transaction count and fraud count
SELECT
    COUNT(*) as total_transactions,
    SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) as total_fraud_transactions
FROM transactions;


-- Transaction by type
SELECT
    type as transaction_type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount
FROM transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- Fraud rate by transaction type
SELECT
    type as transaction_type,
    ROUND(SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_rate_percentage
FROM transactions
GROUP BY transaction_type
ORDER BY fraud_rate_percentage DESC;


-- Hourly Transactions trends
SELECT
    step,
    COUNT(*) as total_transactions,
    SUM(amount) as total_amount
FROM transactions
GROUP BY step
ORDER BY step;

-- Top Accounts by Transaction Volume
SELECT
    nameOrig as account,
    SUM(amount) as total_sent
FROM transactions
GROUP BY nameOrig
order by total_sent DESC
LIMIT 10;
