# coding=utf-8
import os
import lxml
import time

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
        homework = lxml.etree.Element("a")
        homework.set("href",item.homeworkUrl)
        homework.text = "学习任务单"
        td.append(homework)
        tr.append(td)
    lxml.etree.tostring(table)
    date = time.strftime("%d%d",time.localtime())
    filename = date + "index.html"
    print(lxml.etree.tostring(table))
    # with open(filename,"w") as f:
    #     f.write(lxml.etree.tostring(table,encoding='utf-8'))
    return filename