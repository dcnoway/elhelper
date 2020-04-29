# coding=utf-8
import time
import zipfile
from unzipmbcs import extractZip
import requests
import os
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
from buildhtm import buildHtml
import webbrowser
grade =4
date = time.localtime()
dbs = bdschoolSeminars(grade,date)
xcs = xcSchoolSeminars()
dbs.update(xcs)

#Download all homework packages to local folder and unzip it
for item in dbs.values():
    print(item)
    res = requests.get(item.homeworkUrl,verify=False)
    if len(item.homeworkName) == 0:
        fileName = os.path.basename(item.homeworkUrl)
    else:
        fileName = item.homeworkName
    fileName = 'files/'+fileName
    if not os.path.exists(fileName):
        with open(fileName, 'wb') as f:
            f.write(res.content)
    
    os.system('7z x -ofiles "'+fileName+'"')
    # if zipfile.is_zipfile(fileName):
    #     if item.subject == '英语':
    #         extractZip(fileName,'utf-8')
    #     else:
    #         with zipfile.ZipFile(fileName,'r') as zf:
    #             zf.extractall('files/')
#Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool
mainpage = buildHtml(dbs.values())
#raise up web browser to open the portal page
#webbrowser.open_new("file://./"+mainpage)
#webbrowser.WindowsDefault.open_new(url = "file://./"+mainpage)
#webbrowser.Chrome.open_new(url = "file://./"+mainpage)
webbrowser.open_new(url = "file://./"+mainpage)