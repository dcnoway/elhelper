# coding=GBK
import time
import zipfile
from unzipmbcs import extractZip
import requests
import os
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
from buildhtm import buildHtml
import re

def findTaskSheetPath(indexFilePath):
    pattern = '����.(docx|pdf)'
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
            print(readline)
            return readline
    raise Exception('Can not find task sheet fild path')

def main():
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
        
        os.system('7z x -ofiles -aos "'+fileName+'"')
        os.system('7z l "'+fileName+'" >"'+fileName+'.idx"')

        #search for task sheet file path in idx file
        tasksheetPath = findTaskSheetPath(fileName+'.idx')
        item.homeworkTaskSheet = 'files/'+tasksheetPath
    #Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool
    mainpage = buildHtml(dbs.values())
    #raise up web browser to open the portal page
    #webbrowser.open_new("file://./"+mainpage)
    #webbrowser.WindowsDefault.open_new(url = "file://./"+mainpage)
    #webbrowser.Chrome.open_new(url = "file://./"+mainpage)
    #webbrowser.open_new(url = "file://./"+mainpage)
    os.startfile(mainpage)

if __name__ == '__main__':
    main()
    #findTaskSheetPath('files/b.idx')