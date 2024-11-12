import yfinance as yf
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import schedule
import time

# Database connection configuration
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'   # or your MySQL server's IP
DB_PORT = '3307'
DB_NAME = 'db'

# Create a MySQL connection engine
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def store_daily_tesla_data():
    today = datetime.now().date()
    ticker = yf.Ticker("TSLA")
    daily_data = ticker.history(start=today.strftime('%Y-%m-%d'), end=(today + pd.Timedelta(days=1)).strftime('%Y-%m-%d'))

    if daily_data.empty:
        print("No data to save today.")
        return

    daily_data.reset_index(inplace=True)
    daily_data.to_sql('tesla_stock_data', con=engine, if_exists='append', index=False)
    print(f"Data stored successfully for {today} in MySQL!")


store_daily_tesla_data()