import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tradingview_ta import TA_Handler, Interval
from datetime import datetime, timedelta



DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'  
DB_PORT = '3307'
DB_NAME = 'db'
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
    print(f"Data stored successfully for {today} ")

def send_email(content_msg,content_header):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    email = "patara1929@gmail.com"
    password = "hnoy gqhk trmx bhyn" 
    
    to_email = "64011224@kmitl.ac.th"
    subject = content_header
    body = content_msg
    
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def Analysis():
    tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
    )
    
    analysis = tesla.get_analysis()
    rsi_indicator_value = analysis.indicators['RSI']
    
    if rsi_indicator_value < 30:
        content_header = "ซื้อด่วน!!!"
        content_msg = "ราคาต่ำมากแล้ว!! รีบซื้อ ขณะนี้อยู่ในจังหวะช้อน"
        
    elif 30 < rsi_indicator_value < 70:
        content_header = "รายงานสถานการณ์หุ้นประจำวัน"
        content_msg = "ช่วงไม่มีอะไรน่าสนใจ ยังไม่ต้องซื้อขาย" 
        
    elif rsi_indicator_value >= 70:
        content_header = "ขายด่วน!!!"
        content_msg = "ราคาสูงมากแล้ว!! ควรขายก่อนจะขาดทุน"
    else:
        content_header = "รายงานสถานการณ์หุ้นประจำวัน"
        content_msg = "ช่วงไม่มีอะไรน่าสนใจ ยังไม่ต้องซื้อขาย"
        
    send_email(content_msg,content_header)

   
schedule.every().monday.at("22:00").do(Analysis)
schedule.every().tuesday.at("22:00").do(Analysis)
schedule.every().wednesday.at("22:00").do(Analysis)
schedule.every().thursday.at("22:00").do(Analysis)
schedule.every().friday.at("22:00").do(Analysis)

schedule.every().day.at("06:00").do(store_daily_tesla_data)

ticker = yf.Ticker("TSLA")
try:
    while True:
        data = ticker.history(period="1d", interval="5m")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} - TSLA Real-Time Price: [{current_price:.3f}$]")
            
            if current_price > 345:
                content_header = f"เกิน 400$ รีบขายเร็ว"
                content_msg = f"ราคาTSLA : {current_price}$ ได้เวลาขายเอากำไรแล้ว"
                send_email(content_msg,content_header)
            elif current_price < 300:
                content_header = f"จังหวะช้อนมาแล้ว"
                content_msg = f"ราคาTSLA : {current_price} ได้เวลาช้อนแล้ว"
                send_email(content_msg,content_header)
        else:
            print("No data available.")
            
            
        schedule.run_pending()
        time.sleep(60)

except KeyboardInterrupt:
    print("Real-time price monitoring stopped.")






