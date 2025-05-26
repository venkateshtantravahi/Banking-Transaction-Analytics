import pandas as pd
from sqlalchemy import create_engine

# Load CSV data
df = pd.read_csv('data/raw/PaySim.csv')

# Create SQLite database
engine = create_engine('sqlite:///banking.db')

# Save to SQL
df.to_sql('transactions', con=engine, index=False, if_exists='replace')

print("Data loaded into 'transactions' table in banking.db!")
