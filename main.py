import backtrader as bt
import datetime
import yfinance as yf

class MyStrategy(bt.Strategy):
    params = (('sma_period', 20),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

cerebro = bt.Cerebro()

# Definir o valor inicial do investimento
starting_cash = 1000
cerebro.broker.setcash(starting_cash)

# Obter dados usando yfinance
ticker = "AAPL"
start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2020, 1, 1)  # Data atual
data = yf.download(ticker, start=start_date, end=end_date)

data = bt.feeds.PandasData(dataname=data)

cerebro.adddata(data)

cerebro.addstrategy(MyStrategy)

print("Starting Value: ${:.2f}".format(cerebro.broker.getvalue()))

result = cerebro.run()

final_value = cerebro.broker.getvalue()

print("Final Value: ${:.2f}".format(final_value))

cerebro.plot()