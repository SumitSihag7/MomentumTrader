import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import warnings

warnings.filterwarnings('ignore')

class MomentumBacktester:
    def __init__(self, file_path: str, company_name: str, short_window: int = 10, long_window: int = 50, rsi_window: int = 14):
        self.file_path = file_path
        self.company_name = company_name
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_window = rsi_window
        self.df = None

    def load_data(self):
        df = pd.read_csv(self.file_path).iloc[2:]
        df['Close'] = df['Close'].astype(float)
        df['Price'] = pd.to_datetime(df['Price'])
        self.df = df

    def calculate_indicators(self):
        if self.df is None:
            self.load_data()
            
        self.df['daily_return'] = self.df['Close'].pct_change(1)
        self.df['ma_short'] = ta.trend.sma_indicator(self.df['Close'], window=self.short_window)
        self.df['ma_long'] = ta.trend.sma_indicator(self.df['Close'], window=self.long_window)
        self.df['rsi'] = ta.momentum.rsi(self.df['Close'], window=self.rsi_window)

    def generate_signals(self):
        self.df['ma_signal'] = np.where(self.df['ma_short'] > self.df['ma_long'], 1, 0)
        self.df['rsi_signal'] = np.where((self.df['rsi'] < 70) & (self.df['rsi'] > 30), 1, 0)
        self.df['signal'] = self.df['ma_signal'] * self.df['rsi_signal']

    def calculate_metrics(self):
        self.df['strategy_return'] = self.df['signal'].shift(1) * self.df['daily_return']
        self.df['cumul_market_return'] = (1 + self.df['daily_return']).cumprod()
        self.df['cumul_strategy_return'] = (1 + self.df['strategy_return']).cumprod()
        self.df.dropna(inplace=True)

        total_days = len(self.df)
        trading_days_per_year = 252
        years = total_days / trading_days_per_year

        self.total_return_market = self.df['cumul_market_return'].iloc[-1] - 1
        self.total_return_strategy = self.df['cumul_strategy_return'].iloc[-1] - 1

        self.annual_return_market = (1 + self.total_return_market) ** (1 / years) - 1
        self.annual_return_strategy = (1 + self.total_return_strategy) ** (1 / years) - 1

        self.df['market_peak'] = self.df['cumul_market_return'].cummax()
        self.df['market_drawdown'] = (self.df['cumul_market_return'] / self.df['market_peak']) - 1
        self.max_drawdown_market = self.df['market_drawdown'].min()

        self.df['strategy_peak'] = self.df['cumul_strategy_return'].cummax()
        self.df['strategy_drawdown'] = (self.df['cumul_strategy_return'] / self.df['strategy_peak']) - 1
        self.max_drawdown_strategy = self.df['strategy_drawdown'].min()

    def print_performance(self):
        print(f"Performance of {self.company_name} (MA {self.short_window}/{self.long_window}, RSI {self.rsi_window}):")
        print(f"Total Return (Market):     {self.total_return_market:.2%}")
        print(f"Total Return (Strategy):   {self.total_return_strategy:.2%}")
        print(f"Annualized Return (Market):   {self.annual_return_market:.2%}")
        print(f"Annualized Return (Strategy): {self.annual_return_strategy:.2%}")
        print(f"Maximum Drawdown (Market):    {self.max_drawdown_market:.2%}")
        print(f"Maximum Drawdown (Strategy):  {self.max_drawdown_strategy:.2%}")
        print("-" * 60)

    def plot_results(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Price'], self.df['cumul_market_return'], label='Buy and Hold')
        plt.plot(self.df['Price'], self.df['cumul_strategy_return'], label='Momentum Strategy')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.title(f'Strategy vs. Buy & Hold: {self.company_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def run(self, plot=False):
        self.load_data()
        self.calculate_indicators()
        self.generate_signals()
        self.calculate_metrics()
        self.print_performance()
        if plot:
            self.plot_results()

def run_all_backtests(datasets: dict, plot=False):
    for company, path in datasets.items():
        bt = MomentumBacktester(file_path=path, company_name=company)
        bt.run(plot=plot)
