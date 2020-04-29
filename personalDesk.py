# coding=utf-8
import time
import zipfile
import requests
import os
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
from buildhtm import buildHtml
import re

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

def main():
    grade =4
    date = time.localtime()
    dbs = bdschoolSeminars(grade,date)
    xcs = xcSchoolSeminars()
    dbs.update(xcs)

    #Download all homework packages to local folder and unzip it
    for item in dbs.values():
        #print(item)
        res = requests.get(item.homeworkUrl,verify=False)
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
        item.homeworkTaskSheet = 'files/'+tasksheetPath
    #Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool
    mainpage = buildHtml(dbs.values())
    #raise up web browser to open the portal page
    os.startfile(mainpage)

if __name__ == '__main__':
    main()