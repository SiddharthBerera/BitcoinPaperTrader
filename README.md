# BitcoinPaperTrader
A bitcoin paper trader with interactive dynamic candlestick graph
note api keys are read only.

This project was submitted for the Adahackr blackrock hackathon.
The goal of this project was to make a web based, bitcoin paper trader. 
Users would then be able to paper trade on the platform and results would be published on a high scores page. 
This could then be used to verify the legitamcy of so called 'trading signal' providers, filtering out 'fake gurus' and other scammers.

Bitcoin price data is streamed from the Binance Cryptocurrency trading platform in python. The flask framework is then used to send this data to the front end.
On the front end, makes use of JavaScript to take the real time price data of BTC to make a live candlestick graph.
The user can then place market orders with a fixed amount of funds and can choose to have their PNL published on the high scores leaderboard page.
High scoring users can opt to be reviewed and verifyed, this will allow both legitimate trading signal providers to advertise themselves and retail
crypto traders to feel safer taking advice from said signal providers - it's a win-win!


