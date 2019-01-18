from .book import BookViewModel


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []

        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()
        # 通过结果返回回来， 而不是直接在方法中修改实例变量
        # 这样一旦这个类变得很复杂， 就能在__init__中知道实例变量都在哪里被修改了。

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        my_gift = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),  # gift.book没有转化为BookViewModel,需转化
            'id': gift.id
        }
        return my_gift
