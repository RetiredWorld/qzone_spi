# -*- coding:utf-8 -*-
# fun for use!
# Author: vegetable chicken
# createtime: 2020/1/4 23:00

import random
import time
import warnings
import os

import requests
import re
from PIL import Image

warnings.filterwarnings('ignore')


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

QRIMG_PATH = 'code.jpg'
IMGSV_PATH = '无敌的小狐狸_外援/'

'''在这里设置你的URL'''
LOGIN_URL = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https://qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=https://z.qzone.com/download.html&self_regurl=https://qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=https://z.qzone.com/download.html&pt_no_auth=0'
LOGIN_PARA = {
    'proxy_url': 'https://qzs.qq.com/qzone/v6/portal/proxy.html',
    'daid': '5',
    'hide_title_bar': '1',
    'low_login': '0',
    'qlogin_auto_login': '1',
    'no_verifyimg': '1',
    'link_target': 'blank',
    'appid': '549000912',
    'style': '22',
    'target': 'self',
    's_url': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
    'pt_qr_app': '手机QQ空间',
    'pt_qr_link': 'https://z.qzone.com/download.html',
    'self_regurl': 'https://qzs.qq.com/qzone/v6/reg/index.html',
    'pt_qr_help_link': 'https://z.qzone.com/download.html',
    'pt_no_auth': '0'
}

QRLOHIN_URL = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'
qrtoken = ''    # 从二维码中获得
login_sig = ''  # 从cookie中获得
QRLOGIN_PARA = {
    'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
    'ptqrtoken': qrtoken,
    'ptredirect': '0',
    'h': '1',
    't': '1',
    'g': '1',
    'from_ui': '1',
    'ptlang': '2052',
    'action': '0-0-' + str(int(time.time())),
    'js_ver': '19112817',
    'js_type': '1',
    'login_sig': login_sig,
    'pt_uistyle': '40',
    'aid': '549000912',
    'daid': '5',
    'ptdrvs': 'AnyQUpMB2syC5zV6V4JDelrCvoAMh-HP6Xy5jvKJzHBIplMBK37jV1o3JjBWmY7j*U1eD8quewY_',
    'has_onekey': '1'
}

QRSHOW_URL = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
QRSHOW_PARA = {
    'appid': '549000912',
    'e': '2',
    'l': 'M',
    's': '3',
    'd': '72',
    'v': '4',
    't': str(random.random()),
    'daid': '5',
    'pt_3rd_aid': '0'
}

ZONEPHO_URL = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?'
g_tk = ''   # 关键参数，破解加密获得
qq_num = ''  # 空间qq号，可在登陆后得到
ZONEPHO_PARA = {
    'g_tk': g_tk,
    'callback': 'shine0_Callback',
    't': 995949761,
    'mode': 0,
    'idcNum': 4,
    'hostUin': qq_num,
    'topicId': 'V121e7pW1cvT31',
    'noTopic': 0,
    'uin': qq_num,
    'pageStart': 0,
    'pageNum': 200,
    'skipCmtCount': 0,
    'singleurl': 1,
    'batchId': '',
    'notice': 0,
    'appid': 4,
    'inCharset': 'utf-8',
    'outCharset': 'utf-8',
    'source': 'qzone',
    'plat': 'qzone',
    'outstyle': 'json',
    'format': 'jsonp',
    'json_esc': 1,
    'question': '',
    'answer': '',
    'callbackFun': 'shine0',
    '_': 1578111026366
}


class Login:

    def __init__(self):
        self.session = requests.Session()
        self.all_cookies = {}
        self.headers = HEADERS
        self.lg_sig_url = LOGIN_URL
        self.qrshow_url = QRSHOW_URL
        self.qrlogin_url =QRLOHIN_URL
        self.qqnum = ''
        self.p_skey = ''

    # 登陆解密函数
    def decryptQrsig(self, q):
        e = 0
        for c in q:
            e += (e << 5) + ord(c)
        return 2147483647 & e

    # 间隔2s检查二维码状态
    def wait_for_response(self, qrtoken, login_sig):
        params = QRLOGIN_PARA
        params['ptqrtoken'] = qrtoken
        params['login_sig'] = login_sig
        while True:
            params['action'] = '0-0-' + str(int(time.time())),
            res = self.session.get(self.qrlogin_url, headers=self.headers, params=params)
            if '未失效' in res.text:
                print('二维码正常')
            if '认证中' in res.text:
                print('二维码验证中')
            if '登录成功' in res.text:
                print('验证成功！')
                return res
            elif '二维码已经失效' in res.text:
                return None
            time.sleep(2)

    # 主函数
    def main_(self):
        print('正在准备...')
        login_res = self.session.get(self.lg_sig_url, headers=self.headers, verify=False, params=LOGIN_PARA)
        self.all_cookies.update(login_res.cookies)
        login_sig = login_res.cookies['pt_login_sig']

        qr_res = self.session.get(self.qrshow_url, headers=self.headers, params=QRSHOW_PARA)
        self.all_cookies.update(requests.utils.dict_from_cookiejar(qr_res.cookies))
        self.session.cookies.update(self.all_cookies)
        qrsig = self.all_cookies['qrsig']
        qrtoken = self.decryptQrsig(qrsig)

        print('即将打开二维码图片，请扫描确认:')
        with open(QRIMG_PATH, 'wb') as fp:
            fp.write(qr_res.content)

        qr_img = Image.open(QRIMG_PATH)
        qr_img.show()
        res = self.wait_for_response(qrtoken, login_sig)
        if res is None:
            print('二维码已失效，请重新开始!')
            return None
        self.qqnum = re.findall(r'&uin=(.+?)&service', res.text)[0]
        self.all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))

        # 从获得的登陆成功信息中取得刷新链接刷新页面，保存cookie
        url_refresh = res.text[res.text.find('http'): res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
        res = self.session.get(url_refresh, allow_redirects=False, verify=False)
        self.all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
        self.session.cookies.update(self.all_cookies)
        # 这有个小问题，cookie类型为cookiejar而不是字典，所以会有多个重名的索引，对应的应该是不同的域名记录，但是我不知道如何处理得到我想要的值，所以只能在这里得到我后面爬相册的时候需要的p_skey来代替
        self.p_skey = res.cookies['p_skey']
        print('登陆已成功')
        return self.session, self.qqnum


class PhotoData:

    def __init__(self, session, p_skey, qqnum=1234567):
        self.pho_url = ZONEPHO_URL
        self.para = ZONEPHO_PARA
        self.headers = HEADERS
        self.session = session
        self.p_skey = p_skey
        self.qqnum = qqnum

    # g_tk解密函数（获得所有空间数据必要参数解密）
    def g_tk_getter(self, p_skey):
        h = 5381
        g_tk = 100
        for i in p_skey:
            h += (h << 5) + ord(i)
            # print('g_tk', h & 2147483647)
            g_tk = h & 2147483647
        return g_tk

    def main_(self):
        g_tk = self.g_tk_getter(self.p_skey)
        self.para['g_tk'] = g_tk
        self.para['hostUin'] = self.qqnum
        # self.para['hostUin'] = 1239485606
        self.para['uin'] = self.qqnum
        res = self.session.get(self.pho_url, headers=self.headers, params=self.para)
        print('内容已经获得')
        return res.text


def replace(string):
    string = string.replace(' ', '__')
    string = string.replace('-', '')
    string = string.replace(':', '_')
    string = string[2:]
    return string


def img_g_s(data):
    pattern = re.compile(r'"uploadtime" : "(.*?)"[\s\S]*?"url" : "(.*?)"')
    res = pattern.findall(data)
    for i in range(len(res)):
        res[i] = list(res[i])
        res[i][0] = replace(res[i][0])
    print('共{}条记录,时间跨度为{}~{}'.format(len(res), res[0][0], res[-1][0]), len(res))
    return res


def saver(lis, session, path):
    num = 1
    if os.path.exists(path) is False:
        os.makedirs(path)
    for img_lis in lis:
        print('正在获得第{}张图片,共{}张'.format(num, len(lis)))
        num += 1
        with open(path + img_lis[0] + '.jpg', 'wb') as fp:
            img = session.get(img_lis[1], headers=HEADERS)
            fp.write(img.content)
        time.sleep(4)
    print('已完成')


def main():
    login = Login()
    session, qqnum = login.main_()
    pho_data = PhotoData(session, login.p_skey, qqnum)
    data = pho_data.main_()
    res_lis = img_g_s(data)
    saver(res_lis, session, IMGSV_PATH)


if __name__ == '__main__':
    main()
