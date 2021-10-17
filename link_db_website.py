from flask import Flask
import csv

app = Flask(__name__)

@app.route("/")
def read_in_csv():
    date_and_time=[]
    date_and_time_msg = ''
    open_prices=[]
    open_prices_msg = ''
    high_prices=[]
    high_prices_msg = ''
    low_prices=[] 
    low_prices_msg = ''
    close_prices=[]
    close_prices_msg = ''
    
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        nr_lines=0
        for row in reader:
            if nr_lines >= 1 and nr_lines <= 3:
                date_and_time.append(row[0])
                date_and_time_msg += str(date_and_time[nr_lines])

                open_prices.append(row[1])
                open_prices_msg += str(open_prices[nr_lines])

                high_prices.append(row[2])
                high_prices_msg += str(high_prices[nr_lines])

                low_prices.append(row[3])
                low_prices_msg += str(low_prices[nr_lines])

                close_prices.append(row[4])
                close_prices_msg += str(close_prices[nr_lines])
            nr_lines += 1
    return date_and_time_msg
app.run()