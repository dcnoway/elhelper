# coding=utf-8
import time
import zipfile
import requests
import os
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
from buildhtm import buildHtml
from buildhtm import htmlPath
import re
# import certifi
# import urllib3


def findTaskSheetPath(indexFilePath):
    #MAKE SURE YOU ARE UNDER GBK encoding editor!!!!
    #remove GBK encoding pattern string from source code
    #load GBK encoding pattern string from GBK encoding txt file
    #for source code edit convinences
    with open('taskptn.txt','r') as f:
        pattern = f.readline()

    passPtn = '__MACOSX'
    with open(indexFilePath,'r') as f:
        readlines = f.readlines()
    for readline in readlines:
        #bypass __MACOSX lines
        passed = re.findall(passPtn,readline)
        if len(passed) > 0:
            continue
        #find task sheet file path string pattern
        finded = re.findall(pattern,readline)
        if len(finded) > 0:
            readline = readline[25:].lstrip(' ')
            i = readline.find(' ')
            readline = readline[i:].lstrip(' ')
            i = readline.find(' ')
            readline = readline[i:].lstrip(' ')
            #print(readline)
            return readline
    raise Exception('Can not find task sheet fild path')

def fixIllegalPath(indexFilePath:str):
    dir = os.path.dirname(indexFilePath)
    if dir[-1:] =='.':
        lst = list(dir)
        lst[-1:]='_'
        dir = ''.join(lst)
    return dir+'/'+os.path.basename(indexFilePath)

def main():
    if not (os.path.exists('files') and os.path.isdir('files')):
        os.path.mkdir('files')

    if os.path.exists(htmlPath()) and os.path.isfile(htmlPath()):
        os.startfile(htmlPath())
        return
        
    if os.system('7z>nul')!=0:
        print('Please install 7-Zip and make sure 7z.exe is in the PATH.')
        
    grade =4
    date = time.localtime()
    dbs = bdschoolSeminars(grade,date)
    xcs = xcSchoolSeminars()
    dbs.update(xcs)

    #Download all homework packages to local folder and unzip it
    # http = urllib3.PoolManager(
    #     cert_reqs='CERT_REQUIRED',
    #     ca_certs=certifi.where())    
    # session = requests.Session()
    for item in dbs.values():
        #print(item)
        res = requests.get(item.homeworkUrl,verify=False)
        # res = session.get(item.homeworkUrl,verify = False)
        # res = http.request('GET',item.homeworkUrl)
        if len(item.homeworkName) == 0:
            fileName = os.path.basename(item.homeworkUrl)
        else:
            fileName = item.homeworkName
        fileName = 'files/'+fileName
        if not os.path.exists(fileName):
            with open(fileName, 'wb') as f:
                f.write(res.content)
        
        os.system('7z x -ofiles -aos "'+fileName+'" >>nul')
        os.system('7z l "'+fileName+'" >"'+fileName+'.idx"')

        #search for task sheet file path in idx file
        tasksheetPath = findTaskSheetPath(fileName+'.idx')
        tasksheetPath = fixIllegalPath(tasksheetPath)
        item.homeworkTaskSheet = 'files/'+tasksheetPath
    #Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool
    mainpage = buildHtml(dbs.values())
    #raise up web browser to open the portal page
    os.startfile(mainpage)

if __name__ == '__main__':
    main()