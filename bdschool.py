# coding utf-8
import requests
import json
import time
from lxml import etree

class bdschoolAPI(object):
    #urlCurrentSchedule = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade=4&_d=2020/04/23'
    urlCurrentSchedule = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade={grade}&_d={yyyyMMdd}'

    @staticmethod
    def get_schedule(grade:int, date:str):
        '''
        Get all avaliable nCov data of designated city
        return a 

        if city:
            response = requests.get(url=QQnCovAPI.urlNCOVCityHistory.format(provinceName=province,cityName=city))
        else:
            response = requests.get(url=QQnCovAPI.urlNCOVProvinceHistory.format(provinceName=province))
        
        if(response.ok):
            response.encoding='utf-8'
            jsonObj = json.loads(response.content,encoding='utf-8')
            if(jsonObj['ret']==0):
                return jsonObj['data']
        else:
            raise Exception('Server NOT responding!',response)
        '''
        resp = requests.get(url=bdschoolAPI.urlCurrentSchedule.format(grade=grade,yyyyMMdd=date))
        if(resp.ok):
            resp.encoding='utf-8'
            html = etree.HTML(resp.text)
        else:
            raise Exception('Server NOT responding',resp)

if __name__ == '__main__':
    localtime = time.localtime(time.time())
    print("本地时间为 :", localtime)
    ymd=time.strftime("%Y/%m/%d", time.localtime())
    print(ymd)
    bdschoolAPI.get_schedule(4,ymd)