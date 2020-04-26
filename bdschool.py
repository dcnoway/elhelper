# coding=utf-8
import requests
import json
import time
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

    resp = requests.get(
        url=urlCurrentSchedule.format(grade=grade,yyyyMMdd=time.strftime("%Y/%m/%d",date)),
        verify = False)
    if(resp.ok):
        resp.encoding='utf-8'
        html = etree.HTML(resp.text)
    else:
        raise Exception('Server NOT responding',resp)

    result ={}

    cellPath='//table[@class="content_table"][@grade="4"][@week_index="{week_index}"]\
        /tr[@class="content_table_tr"]/td[@class="content_table_td"]'.format(week_index=week_index)
    cells = html.xpath(cellPath)
    print('Total cells:{}'.format(len(cells)))
    for idx,val in enumerate(cells):
        if idx%5 ==wday:
            if len(val.xpath('./div[@class="content_table_td_subject"]')) != 0 and \
                len(val.xpath('./a[@class="content_table_td_title"]/span[@class="conten_table_td_span_title"]')) != 0:
                subject = val.xpath('./div[@class="content_table_td_subject"]')[0].text
                print(subject)
                for a in val.xpath('./a[@class="content_table_td_title"]'):
                    sem = Seminar()
                    sem.subject =subject
                    sem.title = a.xpath('./span[@class="conten_table_td_span_title"]')[0].text
                    sem.videoUrl = a.xpath('./@href')[0]
                    result[sem.title] =sem
                    print(sem.title)
                    print(sem.videoUrl)
            elif len(val.xpath('./a[@class="conten_table_td_span_title_download"]'))!=0:
                for a in val.xpath('./a[@class="conten_table_td_span_title_download"]'):
                    title =a.xpath('./span[@class="conten_table_td_span_title"]')[0].text
                    print(title)
                    result[title].homeworkUrl = a.xpath('./@href')[0]
                    print(result[title].homeworkUrl)
    return result

if __name__ == '__main__':
    grade =4
    date = time.localtime()
    bdschoolSeminars(grade,date)