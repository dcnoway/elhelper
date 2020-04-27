# coding=utf-8
import requests
import http.cookiejar as cookielib
from seminar import Seminar

# session代表某一次连接
session = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
session.cookies = cookielib.LWPCookieJar(filename="xc.cookies")

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64"
header = {
    "origin": "https://xcmicro.17zuoye.comn",
    "Referer": "https://xcmicro.17zuoye.com/pc/login.html",
    'User-Agent': userAgent,
}


def xcLogin(account, password):
    # 模仿登录
    print("开始模拟登录")

    postUrl = "https://zx.17zuoye.com/mstudent/XcUser/login"
    postData = {
        "user_id": account,
        "password": password,
    }
    # 使用session直接post请求
    responseRes = session.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取首页的时候，就不需要再走Login的流程了，因为已经从文件中拿到cookie了
    session.cookies.save()


def isLogin():
    # 通过访问个人中心页面的返回状态码来判断是否为登录状态

    routeUrl = "https://xcmicro.17zuoye.com/pc/index.html"
    # 下面有两个关键点
    # 第一个是header，如果不设置，会返回500的错误
    # 第二个是allow_redirects，如果不设置，session访问时，服务器返回302，
    # 然后session会自动重定向到登录页面，获取到登录页面之后，变成200的状态码
    # allow_redirects = False  就是不允许重定向
    responseRes = session.get(routeUrl, headers=header, allow_redirects=False)
    print(f"isLoginStatus = {responseRes.status_code}")
    if responseRes.status_code != 200:
        return False
    else:
        return True

'''
1,Get all subject list   getXcSubjectList(): array of {"subjectIds":["132"],"subjectName":"心灵万花筒","bookIds":["BK_13200004493791"]}
2,Get all weekly list getUITree(["BK_13200004493791"]): array of {"ids":["BKC_13200265448587"],"subjectIds":[132],"bookIds":["BK_13200004493791"],"name":"第一周"}
3,Get last unit of the given subject getSubjectLastUnit(subject_ids: ["132"]): array of {"unit_ids":["BKC_13200266078126"]}
4,Get video list of the given unit getVideoList(unit_ids: ["BKC_10300266278706"]): {"books":[{"id":"BK_10300004400142","seriesId":"BKC_10300263626216","name":"西城区微课-英语-四年级下学期","alias":"西城区微课-英语-四年级下学期","brief":null,"publisher":"一起科技","clazzLevel":4,"startClazzLevel":1,"termType":2,"imgUrl":"","ugcAuthor":"","bookType":"XICHENG","bookTypes":["XICHENG"],"latestVersion":1,"year":2020,"status":"ONLINE","subjectId":103,"shortName":"西城区微课-英语-四年级下学期","shortPublisher":"一起科技","publisherRank":84,"showLevels":[],"createdAt":"2020-02-13T19:03:03.392+08:00","updatedAt":"2020-04-12T16:25:40.586+08:00","deletedAt":null,"oldId":null,"extras":{"has_review_tag_on_m":false,"pronunciation":"美音","review_tag_name":"","open_exam":0},"online":true,"deletedTrue":false}],"units":[{"id":"BKC_10300266278706","name":"第十周","alias":"","brief":null,"subjectId":103,"rank":11,"nodeType":"UNIT","nodeAttr":0,"nodeLevel":3,"hasChild":false,"parentId":"BK_10300004400142","ancestors":[{"id":"BKC_10300263626216","nodeType":"SERIES","nodeLevel":"1"},{"id":"BK_10300004400142","nodeType":"BOOK","nodeLevel":"2"}],"printedCatalog":null,"page":null,"show":true,"shortName":"","createdAt":"2020-04-12T16:23:59.783+08:00","updatedAt":"2020-04-12T16:25:26.847+08:00","deletedAt":null,"oldTable":null,"oldId":null,"extras":[],"audioUrl":null,"lrcUrl":null,"deletedTrue":false}],"video_list":[{"id":"MC_10300009361327","subjectId":103,"name":"新标准四年级下册  Module 3 Unit 1 He shouted, \"Wolf, wolf!\"","courseDesc":"高佳","courseType":"EXPLAIN","coverUrl":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c6f9282393fa3c4bb3300.png","videoUrl":"https://v.17zuoye.cn/other/2020419/5e9c65c482393fa3c4bb2f77.mp4","videoSeconds":1375,"courseSummary":"","courseSeconds":1375,"regions":[{"provinceId":110000,"cityId":110100,"regionId":110102}],"unitId":"BKC_10300266278706","questionIds":[],"status":"ONLINE","orderNumber":1,"creatorId":"5a715303b1e48a284355926f","extras":[],"createdAt":"2020-04-19T23:35:01.221+08:00","updatedAt":"2020-04-20T08:34:02.646+08:00","deletedAt":null,"remark":"","openedAt":"2020-04-21T08:00:00.000+08:00","attachments":[{"url":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c6fa282393fa3c4bb331b.rar","name":"0421四年级英语(外研版)-Module 3 Unit 1 He shouted, Wolf, wolf!.rar"}],"notDeleted":true,"openStatus":1,"study_duration":1375},{"id":"MC_10300009364698","subjectId":103,"name":"新标准四年级下册  Module 3 Unit 2 Let's tell stories.","courseDesc":"高佳","courseType":"EXPLAIN","coverUrl":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c701782393fa3c4bb3353.png","videoUrl":"https://v.17zuoye.cn/ai_teacher/2020419/5e9c67f43cb75e11f943f9a3.mp4","videoSeconds":1188,"courseSummary":"","courseSeconds":1188,"regions":[{"provinceId":110000,"cityId":110100,"regionId":110102}],"unitId":"BKC_10300266278706","questionIds":[],"status":"ONLINE","orderNumber":2,"creatorId":"5a715303b1e48a284355926f","extras":[],"createdAt":"2020-04-19T23:37:18.920+08:00","updatedAt":"2020-04-20T08:34:23.132+08:00","deletedAt":null,"remark":"","openedAt":"2020-04-23T08:00:00.000+08:00","attachments":[{"url":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c702982393fa3c4bb3369.rar","name":"0423四年级英语(外研版)-Module 3 Unit 2 Let's tell stories!.rar"}],"notDeleted":true,"openStatus":1,"study_duration":1188},{"id":"MC_10300009368425","subjectId":103,"name":"新标准四年级下册 Revision 1 (Module 1 & Module 3)","courseDesc":"李云乔","courseType":"EXPLAIN","coverUrl":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c70a482393fa3c4bb33b2.png","videoUrl":"https://v.17zuoye.cn/ai_teacher/2020419/5e9c681f3cb75e11f943f9bb.mp4","videoSeconds":1431,"courseSummary":"","courseSeconds":1431,"regions":[{"provinceId":110000,"cityId":110100,"regionId":110102}],"unitId":"BKC_10300266278706","questionIds":[],"status":"ONLINE","orderNumber":3,"creatorId":"5a715303b1e48a284355926f","extras":[],"createdAt":"2020-04-19T23:39:55.708+08:00","updatedAt":"2020-04-20T08:34:42.068+08:00","deletedAt":null,"remark":"","openedAt":"2020-04-24T08:00:00.000+08:00","attachments":[{"url":"https://cdn-cnc.17zuoye.cn/fs-resource/5e9c70c53cb75e11f943fced.rar","name":"0424四年级英语(外研版)-Revision I (Module1&Module3).rar"}],"notDeleted":true,"openStatus":1,"study_duration":1419}]}
'''
def getXcSubjectList():
    result = []
    return result

def getUITree(bookIds):
    result = []
    return result

def getSubjectLastUnit(subjectIds):
    result = []
    return result

def getVideoList(unitIds):
    result = {}
    return result

def xcSchoolSeminars(date=''):
    session.cookies.load()
    if not isLogin():
        # 从返回结果来看，有登录成功
        xcLogin("xc062040074", "184385")
    if isLogin:
        resp = session.get("https://xcmicro.17zuoye.com/pc/index.html",
                           headers=header, allow_redirects=False)
    result = {}
    return result

if __name__ == "__main__":
    xcSchoolSeminars()
