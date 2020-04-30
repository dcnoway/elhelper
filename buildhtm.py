# coding=utf-8
import os
import lxml
import time

def htmlPath():
    date = time.strftime("%m%d",time.localtime())
    filename = date + "index.html"
    return filename

def buildHtml(seminars):
    table = lxml.etree.Element("table")
    tr = lxml.etree.Element("tr")
    table.append(tr)
    for item in seminars:
        td = lxml.etree.Element("td")
        div = lxml.etree.Element("div")
        td.append(div)
        div.text = item.subject
        title = lxml.etree.Element("a")
        title.set("href",item.videoUrl)
        title.text = item.title
        td.append(title)
        td.append(lxml.etree.Element("br"))
        homework = lxml.etree.Element("a")
        homework.set("href",item.homeworkTaskSheet)
        homework.text = "学习任务单"
        td.append(homework)
        tr.append(td)
    lxml.etree.tostring(table)
    filename = htmlPath()
    with open(filename,"wb") as f:
        f.write(lxml.etree.tostring(table,encoding='utf-8'))
    return filename