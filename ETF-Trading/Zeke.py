# Zeke

import time


class Trader:

    def __init__(self, flux_range, past_trade_feed, symbol, correction_rate, trade_list):
        self.past_trade_feed = past_trade_feed
        self.correction_rate = correction_rate
        self.symbol = symbol
        self.trade_list = trade_list
        self.flux_range = flux_range

    def correction_rate_finder(self):
        self.past_trade_feed = 5

        trade_list = self.trade_list
        base_trade = 1
        negs = [], False
        pos = [], True
        avg_list = [], True
        for trade in range(len(trade_list)):
            diff = trade_list[trade] - trade_list[base_trade]
            base_trade += 1
            if diff <= 0:
                negs[0].append(abs(diff))
            else:
                pos[0].append(abs(diff))
        if len(pos) > len(negs):
            avg_list = pos
        else:
            avg_list = negs
        if avg_list[1]:
            self.correction_rate = int(mean(avg_list[0]))
        else:
            self.correction_rate = -(int(mean(avg_list[0])))

        return self.correction_rate

    def fair_price_finder(self):

        trade_list = self.trade_list
        last_trade = trade_list[len(trade_list) - 1]

        fair_price_est = last_trade + self.correction_rate
        return fair_price_est

    def position_range(self, fair_price_est):
        upper = fair_price_est + self.flux_range
        lower = fair_price_est - self.flux_range

        position = [lower, upper]
        return position

    def make_trades(self):
        while self.correction_rate_finder() > self.flux_range:
            Positions = Trader.position_range(self.fair_price_finder())  # if volatile  new positions
        # if within range make trades
        sell = Positions[1]+1
        buy = Positions[0]-1
        return sell, buy


def main(flux_range, past_trade_feed, symbol, correction_rate, trade_list):
    trader = Trader(flux_range, past_trade_feed, symbol, correction_rate, trade_list)
    sell_position = trader.make_trades()[0]
    buy_position = trader.make_trades()[1]
    return sell_position, buy_position


if __name__ == "__main__":
    main()



