# coding=utf-8
import requests
import json
import time
import urllib3
from lxml import etree
from seminar import Seminar
'''
Fetch given date's e-Learning seminar and all resources
'''

def bdschoolSeminars(grade,date):
    #bdschool information fetch
    urlCurrentSchedule = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade={grade}'
    wday = date.tm_wday
    week_index = time.strftime("%U",date)
    urlCurrentSchedule = urlCurrentSchedule.\
        format(grade=grade,yyyyMMdd=time.strftime("%Y/%m/%d",date))

    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64"
    header = {
        'upgrade-insecure-requests': '1',
        'User-Agent': userAgent,
    }

    session = requests.Session()
    urllib3.disable_warnings()
    resp = session.get(url = urlCurrentSchedule,\
            headers=header,verify=False)

    if(resp.ok):
        resp.encoding='utf-8'
        html = etree.HTML(resp.text)
    else:
        raise Exception('Server NOT responding',resp)

    result ={}

    #find col index for the given date param from ceil row
    colIndex = wday
    ceilPath = '//table[@class="content_table"][@grade="{grade}"][@week_index="{week_index}"]\
        /tr[@class="content_table_tr ceil_bg_color"]/td[@class="content_table_td content_reset_colw"]'\
            .format(grade=grade,week_index=week_index)
    ceils=html.xpath(ceilPath)
    targetText = time.strftime('%m{M}%d{D}',date).format(M='月',D='日')
    for idx,val in enumerate(ceils):
        if len(val.xpath('./div')) > 0 and \
            val.xpath('./div')[0].text == targetText:
            colIndex = idx

    #process content table cells
    cellPath='//table[@class="content_table"][@grade="{grade}"][@week_index="{week_index}"]\
        /tr[@class="content_table_tr"]/td[@class="content_table_td"]'\
            .format(grade=grade,week_index=week_index)
    cells = html.xpath(cellPath)
    for idx,val in enumerate(cells):
        if idx%5 ==colIndex:
            if len(val.xpath('./div[@class="content_table_td_subject"]')) != 0 and \
                len(val.xpath('./a[@class="content_table_td_title"]/span[@class="conten_table_td_span_title"]')) != 0:
                subject = val.xpath('./div[@class="content_table_td_subject"]')[0].text
                if subject == '英语':
                    continue
                for a in val.xpath('./a[@class="content_table_td_title"]'):
                    sem = Seminar()
                    sem.subject =subject
                    sem.title = a.xpath('./span[@class="conten_table_td_span_title"]')[0].text
                    sem.videoUrl = a.xpath('./@href')[0]
                    #bypass 北京版数学教学视频
                    if sem.title.find('北京版') > -1 and sem.subject =='数学':
                        continue
                    result[sem.title] = sem
            elif len(val.xpath('./a[@class="conten_table_td_span_title_download"]'))!=0:
                for a in val.xpath('./a[@class="conten_table_td_span_title_download"]'):
                    title =a.xpath('./span[@class="conten_table_td_span_title"]')[0].text
                    if title.find('北京版') > -1:
                        continue
                    result[title].homeworkUrl = a.xpath('./@href')[0]
    return result

if __name__ == '__main__':
    grade =4
    date = time.localtime()
    print(bdschoolSeminars(grade,date))