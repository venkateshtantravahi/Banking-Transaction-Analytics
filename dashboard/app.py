from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, Div, DataTable, TableColumn
from bokeh.plotting import figure
from sqlalchemy import create_engine
import pandas as pd

# === Connect to DB ===
engine = create_engine('sqlite:///../banking.db')
transactions = pd.read_sql('SELECT * FROM transactions', engine)

# === KPIs ===
total_transactions = len(transactions)
total_fraud = transactions['isFraud'].sum()
total_flagged = transactions['isFlaggedFraud'].sum()
high_value_txns = len(transactions[transactions['amount'] > 10000])
unique_accounts = transactions['nameOrig'].nunique()

# === Header ===
header = Div(text="""
    <div style='text-align: center; font-family: Segoe UI, sans-serif; margin-bottom: 20px;'>
        <h1 style='color: #2c3e50; font-size: 36px; margin: 0;'>Fraud & Money Laundering Dashboard</h1>
        <p style='color: #7f8c8d; font-size: 18px; max-width: 800px; margin: 8px auto 0; line-height: 1.6;'>
            This dashboard provides real-time insights from PaySim transaction data to identify patterns of fraudulent behavior, 
            highlight suspicious accounts, and monitor high-risk activities in financial systems.
        </p>
    </div>
""")

# === KPI Summary (Inline Text) ===
kpi_summary = Div(text=f"""
    <div style='text-align:center; margin-right: 40px; font-family:Segoe UI, sans-serif; margin-top:20px; margin-bottom:20px;'>
        <span style='margin-right:30px; font-size:20px; color:#34495e;'>Total Transactions: <b>{total_transactions:,}</b></span>
        <span style='margin-right:30px; font-size:20px; color:#e74c3c;'>Fraudulent: <b>{total_fraud:,}</b></span>
        <span style='margin-right:30px; font-size:20px; color:#f39c12;'>Flagged Fraud: <b>{total_flagged:,}</b></span>
        <span style='margin-right:30px; font-size:20px; color:#2980b9;'>High-Value (&gt;10K): <b>{high_value_txns:,}</b></span>
        <span style='font-size:20px; color:#27ae60;'>Unique Accounts: <b>{unique_accounts:,}</b></span>
    </div>
""")

# === Charts ===
fraud_type = transactions.groupby('type').agg(total=('isFraud', 'count'), frauds=('isFraud', 'sum')).reset_index()
fraud_type['fraud_rate'] = (fraud_type['frauds'] / fraud_type['total']) * 100
fraud_src = ColumnDataSource(fraud_type)
fraud_plot = figure(x_range=fraud_type['type'], height=300, title="Fraud Rate by Transaction Type", background_fill_color="#ffffff", toolbar_location=None)
fraud_plot.vbar(x='type', top='fraud_rate', source=fraud_src, width=0.7, color='#f39c12')
fraud_plot.yaxis.axis_label = "Fraud Rate (%)"

step_trend = transactions.groupby('step').agg(total=('isFraud', 'count')).reset_index()
step_src = ColumnDataSource(step_trend)
step_plot = figure(height=300, title="Transactions Over Time", x_axis_label="Step", y_axis_label="Count", background_fill_color="#ffffff", toolbar_location=None)
step_plot.line(x='step', y='total', source=step_src, line_width=2, color='#2980b9')

top_accounts = transactions.groupby('nameOrig').agg(total_amount=('amount', 'sum')).reset_index().sort_values(by='total_amount', ascending=False).head(10)
top_src = ColumnDataSource(top_accounts)
top_plot = figure(x_range=top_accounts['nameOrig'], height=300, title="Top Accounts by Volume", background_fill_color="#ffffff", toolbar_location=None)
top_plot.vbar(x='nameOrig', top='total_amount', source=top_src, width=0.7, color='#27ae60')
top_plot.xaxis.major_label_orientation = 1

# === Table for High-Value Transactions ===
high_risk_txns = transactions[transactions['amount'] > 10000][['nameOrig', 'nameDest', 'amount', 'isFraud', 'isFlaggedFraud']].sort_values(by='amount', ascending=False).head(10)
table_src = ColumnDataSource(high_risk_txns)
table = DataTable(source=table_src, columns=[
    TableColumn(field='nameOrig', title='Origin'),
    TableColumn(field='nameDest', title='Destination'),
    TableColumn(field='amount', title='Amount'),
    TableColumn(field='isFraud', title='Fraud'),
    TableColumn(field='isFlaggedFraud', title='Flagged')
], width=600, height=300)

# === Grid Layout ===
grid = gridplot([[fraud_plot, step_plot], [top_plot, table]], sizing_mode='stretch_width', toolbar_location=None)

# === Final Layout ===
curdoc().add_root(column(header, kpi_summary, grid, sizing_mode='stretch_width', spacing=20))
curdoc().title = "Fraud Detection Dashboard"
