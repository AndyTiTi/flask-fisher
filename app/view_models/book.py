# from app.libs.helper import get_isbn
# from app.view_models.book import get_isbn

class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):  # 单个的，即isbn查找
        returned = {'books': [],
                    'total': 0,
                    'keyword': keyword
                    }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_bookdata(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):  # 关键字查找
        returned = {'books': [],
                    'total': 0,
                    'keyword': keyword
                    }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_bookdata(book) for book in data['books']]
            # __cut_bookdata是处理单个book数据的， 这样使用就可以处理多个book数据了
        return returned

    @classmethod
    def __cut_bookdata(cls, data):
        # 处理单个的数据方法， 这样package_single和package_collection都可以用。
        # 不要想着定义个列表， 然后来的不管是多个数据还是单个数据，都放进去。这样的编码并不好。
        book = {'title': data['title'],
                'publisher': data['publisher'],
                'pages': data['pages'] or '',  # 这里使用or， 如果data['pages']返回的是none，我们让它为''
                'author': '、'.join(data['author']),  # 作者如果有多个的话是列表， 我们把它变成字符串
                'price': data['price'],
                'summary': data['summary'] or '',
                'image': data['image']
                }
        return book

class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.isbn = data['isbn']
        # self.isbn = get_isbn(data)
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword


# class BookViewModelOld:
#     @classmethod
#     def from_api(cls, keyword, data):
#         '''
#             为什么不在spider里做成viewmodel？
#             从豆瓣获取的数据可能是单本，也可能是多本集合
#             data 有三种情况：
#             1. 单本
#             2. 空对象
#             3. 有对象
#         '''
#         # if not data:
#
#         yushu_books = data.get('books', 'null')
#         if yushu_books == 'null':
#             total = 1
#             temp_books = [data]
#         else:
#             if len(yushu_books) > 0:
#                 total = data['total']
#                 temp_books = yushu_books
#             else:
#                 total = 0
#                 temp_books = []
#
#         books = []
#         for book in temp_books:
#             book = cls.get_detail(book, 'from_api')
#             books.append(book)
#         # douban_books = result['books'] if result.get('books') else [result]
#         view_model = {
#             'total': total,
#             'keyword': keyword,
#             'books': books
#         }
#         return view_model
#
#     @classmethod
#     def single_book_from_mysql(cls, keyword, data):
#         count = 1
#         if not data:
#             count = 0
#         returned = {
#             'total': count,
#             'keyword': keyword,
#             'books': [cls.get_detail(data)]
#         }
#         return returned
#
#     @classmethod
#     def get_detail(cls, data, from_where='from_mysql'):
#         if from_where == 'from_api':
#             book = {
#                 'title': data['title'],
#                 'author': '、'.join(data['author']),
#                 'binding': data['binding'],
#                 'publisher': data['publisher'],
#                 'image': data['images']['large'],
#                 'price': data['price'],
#                 'isbn': data['isbn'],
#                 'pubdate': data['pubdate'],
#                 'summary': data['summary'],
#                 'pages': data['pages']
#             }
#         else:
#             book = {
#                 'title': data['title'],
#                 'author': '、'.join(data['author']),
#                 'binding': data['binding'],
#                 'publisher': data['publisher'],
#                 'image': data.image,
#                 'price': data['price'],
#                 'isbn': data.isbn,
#                 'pubdate': data['pubdate'],
#                 'summary': data['summary'],
#                 'pages': data['pages']
#             }
#         return book
#
#         # @classmethod
#         # def get_isbn(cls, book):
#         #     isbn13 = book.get('isbn13', None)
#         #     isbn10 = book.get('isbn10', None)
#         #     return isbn13 if isbn13 else (isbn10 if isbn10 else '')
