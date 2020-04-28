# coding=utf-8
import time
import zipfile
import requests
import os
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
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
    with open(fileName, 'wb') as f:
        f.write(res.content)
    if zipfile.is_zipfile(fileName):
        with zipfile.ZipFile(fileName,'r') as zf:
            zf.extractall('files/')
#Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool

#raise up web browser to open the portal page