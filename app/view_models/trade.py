# coding = utf-8


class TradeInfo():
    def __init__(self, goods):
        self.total = 0
        self.trades = []

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_time:
            time = single.create_time.strftime('%Y-%M-%D'),
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )
