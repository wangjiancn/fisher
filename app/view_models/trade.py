# coding = utf-8


class TradeInfo():
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_time:
            push_time = single.create_datetime.strftime('%Y-%m-%d'),
        else:
            push_time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=push_time,
            id=single.id
        )
