-- Customers table (Optional, can infer from account names)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100)
);

-- Accounts table
CREATE TABLE accounts (
    account_id VARCHAR(100) PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    account_type VARCHAR(50)
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    step INT,
    transaction_type VARCHAR(50),
    amount NUMERIC(12,2),
    nameOrig VARCHAR(100),
    oldbalanceOrg NUMERIC(12,2),
    newbalanceOrig NUMERIC(12,2),
    nameDest VARCHAR(100),
    oldbalanceDest NUMERIC(12,2),
    newbalanceDest NUMERIC(12,2),
    isFraud BOOLEAN,
    isFlaggedFraud BOOLEAN
);
