# _*_ coding: utf-8 _*_
from flask import Blueprint

__author__ = 'bobby'
__date__ = '2019/1/11 22:47'

web = Blueprint('web', __name__)

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
