# _*_ coding: utf-8 _*_
from flask import Blueprint, render_template

__author__ = 'bobby'
__date__ = '2019/1/11 22:47'

web = Blueprint('web', __name__)

@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'),404

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
