# _*_ coding: utf-8 _*_
__author__ = 'bobby'
__date__ = '2019/1/9 21:02'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
