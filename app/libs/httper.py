# _*_ coding: utf-8 _*_
__author__ = 'bobby'
__date__ = '2019/1/10 21:47'
# import requests
#
# class HTTP:
#     @staticmethod
#     def get(url,return_json = True):
#         r = requests.get(url)
#         if r.status_code !=200:
#             return {} if return_json else ''
#         return r.json() if return_json else r.text

import requests


class HTTP:  # 使用类 方便以后拓展
    @staticmethod
    def get(url, returned_json=True):
        """
        :param url:
        :param returned_json:
        :return:
        """
        r = requests.get(url)

        # 未简化版
        # if r.status_code == 200:
        #     if returned_json:
        #         return r.json()    # 返回json格式
        #     else:
        #         return r.text    # 返回原始字符串
        # else:
        #     if returned_json:
        #         return {}
        #     else:
        #         return ""

        # 简化代码，尽量减少return语句
        if r.status_code != 200:  # 根据状态码判断是否返回成功
            return {} if returned_json else ''
        return r.json() if returned_json else r.text
