from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d'),
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()
        # 通过结果返回回来， 而不是直接在方法中修改实例变量
        # 这样一旦这个类变得很复杂， 就能在__init__中知道实例变量都在哪里被修改了。

    def __parse(self):
        temp_trades = []
        for gift in self.__trades_of_mine:
            my_gift = self.__matching(gift)
            temp_trades.append(my_gift)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),  # gift.book没有转化为BookViewModel,需转化
            'id': trade.id
        }
        return r
