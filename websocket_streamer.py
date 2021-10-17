import json
import pprint
import time
from time import sleep
from datetime import datetime
import csv
from binance.client import Client
from binance import ThreadedWebsocketManager
from api_keys import api_key, secret_key
import websocket
import numpy
print("hi")
#from binance.enums import *
socket = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"

trade = 'BTCBUSD'
print()
client = Client(api_key, secret_key)

#initilise global variablz
i=0
#in unix time stamp in milliseconds
times = []
date_and_time_now = []
open_prices = []
high_prices = []
low_prices = []
close_prices = []

#set n_mins as a paramter for now but should be user input
n_mins_historical_data = 30

def start():
    print("hi")
    """
    start time
    we only want to proceed when we are at the beginning of a minute, so stuck until seconds is at beginning of minute
    i.e. when time is form hour:min:00
    """
    beginning_of_min = False
    while beginning_of_min == False:
        """
        #seems to 0.1 ms +- the precise minute mark so we can take datetime.now() and truncate to just the seconds
        #and calulate timestamp based on that (we want timestamp to match up with kline candlesticks which we are getting on 
        the min to the precise min i.e. seconds with 0 d.p.)
        """
        start_at = datetime.now()
        start_time_sec = start_at.strftime("%H:%M:%S")
        start_time_min = start_at.strftime("%H:%M")
        if start_time_sec[-2:] == '00':
            beginning_of_min = True 

        #we will get time for min x and the first data will be for min x-1 since that candle will have just finished and
        #kline provides all the data for that min
    start_time_unix_timestamp_seconds = int(time.time())
    print(start_at)
    print(start_time_unix_timestamp_seconds)
    start_time_unix_timestamp_ms = 1000*start_time_unix_timestamp_seconds
    #start at is in hrs, mins, secs
    print("Starting at", start_at)
    return start_time_unix_timestamp_ms
    
def create_data_file():
    #create data_file
    fieldnames = ["time", "open", "high", "low", "close"]
    #'w' modes overwrites wheres 'a' mode appends
    #we want 'w' mode here in case file was already made so we overwrite not append to old data
    with open('data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

def get_historical_data(start_time_unix_timestamp_ms, n_mins_historical_data):
    #24 hours = 24*60*60*1000 ms

    #we shift back historical data so we are doing 24 hours of data before the start of the min 
    #coz we start caclculating on a min for the end of the min
    historic_start_ms = start_time_unix_timestamp_ms - ((n_mins_historical_data+1)*60*1000)
    bars = client.get_historical_klines('BTCUSDT', '1m', historic_start_ms, limit=1000)
    
    #subtract 1 as current min is being streamed in next function (wierd edge case issue)
    for j in range(0, len(bars)-1):
        date_and_time1 = datetime.fromtimestamp(bars[j][0]/1000)
        info = {
            "time": date_and_time1, 
            "open": bars[j][1], 
            "high": bars[j][2], 
            "low": bars[j][3],
            "close": bars[j][4], 
            }
        fieldnames = ["time", "open", "high", "low", "close"]
        #open file to write timestamp, open, close, high and low prices
        with open('data.csv', 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)
    print(len(bars))
    print(start_time_unix_timestamp_ms)
    print(historic_start_ms)
    print(int(time.time()))

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    #make these global so we can append to them
    global times, date_and_time_now, open_prices, high_prices, low_prices, close_prices, i

    print("recieved message")
    

    json_message = json.loads(message)
    print(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    #when candle for minute is closed extract open, close, high and low prices for candle
    if is_candle_closed:
        #start time for candlestick as unix timestamp in milliseconds
        times.append(candle['t'])
        date_and_time_now.append(datetime.fromtimestamp(candle['t']/1000))
        #o,h,l,c prices
        open_prices.append(candle['o'])
        high_prices.append(candle['h'])
        low_prices.append(candle['l'])
        close_prices.append(candle['c'])

        #create latest row in data frame
        info = {
            "time": date_and_time_now[i], 
            "open": open_prices[i], 
            "high": high_prices[i], 
            "low": low_prices[i],
            "close": close_prices[i], 
            }

        fieldnames = ["time", "open", "high", "low", "close"]
        #open file to write timestamp, open, close, high and low prices
        #here we want to append
        with open('data.csv', 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)
        i+=1

def main():        
    start_time_unix_timestamp_ms = start() 
    create_data_file() 
    get_historical_data(start_time_unix_timestamp_ms, n_mins_historical_data)     
    #next is basically function to add on new data being streamed  
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
    #and this is basically just while True loop
    ws.run_forever()

main()