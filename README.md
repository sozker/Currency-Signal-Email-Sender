# Currency-Signal-Email-Sender
An e-mail sender for currency tops and bottoms

This program sends e-mails when a top or bottom point reached for cryptocurrencies or some chosen foreign currencies.

Program chooses the top 25 cryptocurencies with the highest volume on Binance, plus BTC/USDT. It checks the prices for 12 months and sends an e-mail if the price is close to the bottom or top price in this 12 months with some margin.

Foreign currencies are chosen as EUR/USD, USD/TRY, EUR/TRY and GBP/TRY. Current FX prices are taken from website of QNB Finansbank, a major Turkish bank. Historical FX prices are taken from ECB or BOE using Quandl.

Gold prices versus USD has been added. Current price is taken from Mynet Finans (a Turkish website) while historical data is taken from Quandl.

E-mails are written in Turkish but can be easily changed.


