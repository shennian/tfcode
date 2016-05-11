import requests
from bs4 import BeautifulSoup
import json


zh_cookie = dict(
    __utma='51854390.1881384520.1462849265.1462954642.1462954956.8',
    __utmb='51854390.22.8.1462964937913',
    __utmc='51854390',
    __utmt='1',
    __utmv='51854390.100-1|2=registration_date=20131118=1^3=entry_date=20131118=1',
    __utmz='51854390.1462797693.1.1.utmcsr=zhuanlan.zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/p/20871029/voters',
    _xsrf='976458f5d1951b1d32128366f3c560aa',
    _za='7af426ae-aeb0-4ec6-a0cf-8075541e4cd6',
    _zap='f1148b2b-3c9e-4f85-8676-b116061365c3',
    cap_id='\"ZmQ0ZTEwM2QxODM3NGI5Y2FkYjlmMzU2ZjcxZjJjNWQ=|1461738267|9f31cbad9d12e0202437fc1e87963c2dad4922ad\"',
    d_c0='\"AGAAqZxCoQmPTvPgh7NOQRamG85RRfpLPWc=|1461288741\"',
    l_cap_id='\"YTQ0NzljZDdjMGQ2NDIyOGI5NTBhMGE3OTMwMGM1N2I=|1461738267|b5529c39a9b4a3c19b2496122ee6ba63e6874eb0\"',
    q_cl='71e8b8ef03444146a2e6cdb8c9f1a741|1461762535000|1452251589000',
    udid='\"AJDArNSulQmPTiWReCeTjk4LUbLJuijeuAA=|1457527256\"',
    z_c0='Mi4wQUFBQWVlRWdBQUFBWUFDcG5FS2hDUmNBQUFCaEFsVk5QZWhIVndCUW5pdHlLdjNyTG51M0p3RFBETjRUcWQyNnZR|1461738301|4347e2381ac3db2d23e710f3dcb257612ddf27c2'
)


def request_ajax_data(url, start, _xsrf):
    response_data = json.loads(requests.post(url, cookies=zh_cookie, data=dict(start=start, _xsrf=_xsrf)).content)
    start = handle_html(response_data['msg'][1])
    request_ajax_data(url, start, _xsrf)


def handle_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.select('.zm-profile-section-item.zm-item.clearfix'):
        if i['data-type-detail'] != 'member_answer_question':
            continue
        detail = i.select('.zm-profile-section-main a:nth-of-type(3)')[0]
        print 'title: %s - link: https://www.zhihu.com%s' % (unicode(detail.string), detail['href'])
    return i['data-time']


main_page = requests.get('https://www.zhihu.com/people/seasee-youl', cookies=zh_cookie).content
start_time = handle_html(main_page)
request_ajax_data('https://www.zhihu.com/people/seasee-youl/activities',
                  start_time,
                  '976458f5d1951b1d32128366f3c560aa')


# request_ajax_data 没有做终止的判断
# handle_html 过滤了用户点赞和发布专栏的动态，所以如果第一次抓，没有回答的动态，就会出现bug

