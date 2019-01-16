from . import web


@web.route('/')
def index():
    return 'hello world'


@web.route('/personal')
def personal_center():
    pass
