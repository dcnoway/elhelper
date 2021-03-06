# coding=utf-8
import time
#import zipfile
import requests
import os
import sys
from bdschool import bdschoolSeminars
from xcschool import xcSchoolSeminars
from buildhtm import buildHtml
from buildhtm import htmlPath
import re
import urllib3
import platform

def findTaskSheetPath(indexFilePath,colIndex):
    #load GBK encoding pattern string from GBK encoding txt file
    #for source code edit convinences
    with open('taskptn.txt','r',encoding='GBK') as f:
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
            readline = readline.strip()
            for _ in range(colIndex):
                i = readline.find(' ')
                readline = readline[i:].lstrip(' ')
            return readline

            # if isWindows:
            #     readline = readline[25:].lstrip(' ')
            #     i = readline.find(' ')
            #     readline = readline[i:].lstrip(' ')
            #     i = readline.find(' ')
            #     readline = readline[i:].strip()
            #     return readline
            # else:
            #     readline = readline.strip()
            #     i = readline.find(' ')
            #     readline = readline[i:].lstrip(' ')
            #     i = readline.find(' ')
            #     readline = readline[i:].lstrip(' ')
            #     i = readline.find(' ')
            #     readline = readline[i:].lstrip(' ')
            #     return readline
    raise Exception('Can not find task sheet file path')

def fixIllegalPath(indexFilePath:str):
    dir = os.path.dirname(indexFilePath)
    if dir[-1:] =='.':
        lst = list(dir)
        lst[-1:]='_'
        dir = ''.join(lst)
    return dir+'/'+os.path.basename(indexFilePath)

def main():
    print("中古友谊小学学生网课个人桌面 willswu@outlook.com")
    isWindows =platform.system().startswith('Win')
    isLinux = platform.system().startswith('Linux')
    if not (isWindows or isLinux):
        print('Running on a not supported OS!')
        return 1
    if not (os.path.exists('files') and os.path.isdir('files')):
        os.mkdir('files')

    if os.path.exists(htmlPath()) and os.path.isfile(htmlPath()):
        os.startfile(htmlPath())
        return 0
        
    if isWindows:
        if os.system('7z>nul')!=0:
            print('Please install 7-Zip and make sure 7z.exe is in the PATH.')
            return 1
    elif isLinux:
        if os.system('unzip>/dev/null')!=0 :
            print('unzip is not exists!')
            print('please run \'sudo apt install unzip\' manually.')
            return 1
        if os.system('unrar>/dev/null')!=0 :
            print('unrar is not exists!')
            print('please run \'sudo apt install unrar\' manually.')
            return 1
        
    if len(sys.argv) <2:
        grade =4
    elif len(sys.argv) == 2:
        try:
            grade = int(sys.argv[1])
        except TypeError:
            print('第一个参数应为数字，表示获取几年级的当日网课')
            return

    date = time.localtime()
    print('Downloading bdschool.cn seminar index...')
    dbs = bdschoolSeminars(grade,date)
    print('Downloading xcmicro.17zuoye.com seminar index...')
    xcs = xcSchoolSeminars()
    dbs.update(xcs)

    #Download all homework packages to local folder and unzip it
    print('Downloading and unzipping seminar homework packages...')
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64"
    header = {
        'User-Agent': userAgent,
    }
    session = requests.Session()
    urllib3.disable_warnings()
    for item in dbs.values():
        res = session.get(item.homeworkUrl,headers=header,verify=False)
        if len(item.homeworkName) == 0:
            fileName = os.path.basename(item.homeworkUrl)
        else:
            fileName = item.homeworkName
        fileName = 'files/'+fileName
        if not os.path.exists(fileName):
            with open(fileName, 'wb') as f:
                f.write(res.content)
        
        #extract archive file
        if isWindows:
            if os.system('7z x -ofiles -aos "'+fileName+'" >>nul')!=0 :
                print('Extract archive file error!')
                return 1
            #list archive content to a temp text file
            if os.system('7z l "'+fileName+'" >"'+fileName+'.idx"')!=0 :
                print('List archive content error!')
                return 1          
            #search RegEx in the text file and extract the full path of it
            tasksheetPath = findTaskSheetPath(fileName+'.idx',5)
            #clear the temp text file
            os.remove(fileName+'.idx')      
            #if the last char in the dir path is '.', 7-zip will replace it to '_'
            #so we need to fix this path 
            tasksheetPath = fixIllegalPath(tasksheetPath)                                
        elif isLinux:
            _,ext = os.path.splitext(fileName)
            if ext == '.zip':
                if os.system('unzip -nq "'+fileName+'" -d files')!=0:
                    print('Extract archive file error')
                    return 1
                #list archive content to a temp text file
                if os.system('unzip -l "'+fileName+'" >"'+fileName+'.idx"')!=0 :
                    print('List archive content error!')
                    return 1        
                #search RegEx in the text file and extract the full path of it
                tasksheetPath = findTaskSheetPath(fileName+'.idx',3)
                #clear the temp text file
                os.remove(fileName+'.idx')
                     
            elif ext == '.rar':
                shcmd = 'unrar x -inul -o+ "'+fileName+'" files'
                if os.system(shcmd)!=0:
                    print('Extract archive file error')
                    print(shcmd)
                    return 1
                #list archive content to a temp text file
                if os.system('unrar l "'+fileName+'" >"'+fileName+'.idx"')!=0 :
                    print('List archive content error!')
                    return 1                   
                #search RegEx in the text file and extract the full path of it
                tasksheetPath = findTaskSheetPath(fileName+'.idx',4)
                #clear the temp text file
                os.remove(fileName+'.idx')   
            else:
                print("Unsupported archive format!")
                return 1
        else:
            print("Unsupported OS!")
            return 1
        
        item.homeworkTaskSheet = 'files/'+tasksheetPath
    #Make a personal portal contains all seminars and student task sheet links from bdschool and xcschool
    mainpage = buildHtml(dbs.values())
    #raise up web browser to open the portal page
    os.startfile(mainpage)

if __name__ == '__main__':
    main()