import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine


DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'  
DB_PORT = '3307'
DB_NAME = 'db'

engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


ticker = yf.Ticker("TSLA")
end_date = datetime.now()
start_date = end_date - timedelta(days=60)
historical_data = ticker.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))


historical_data.reset_index(inplace=True)

historical_data.to_sql('tesla_stock_data', con=engine, if_exists='replace', index=False)

print("Data stored successfully in MySQL!")
