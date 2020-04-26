# coding=utf-8
import requests

import http.cookiejar as cookielib

# session代表某一次连接
mafengwoSession = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
mafengwoSession.cookies = cookielib.LWPCookieJar(filename = "mafengwoCookies.txt")

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "https://passport.mafengwo.cn/",
    'User-Agent': userAgent,
}

def mafengwoLogin(account, password):
    # 马蜂窝模仿 登录
    print("开始模拟登录马蜂窝")

    postUrl = "https://passport.mafengwo.cn/login/"
    postData = {
        "passport": account,
        "password": password,
    }
    # 使用session直接post请求
    responseRes = mafengwoSession.post(postUrl, data = postData, headers = header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
    mafengwoSession.cookies.save()


if __name__ == "__main__":
    # 从返回结果来看，有登录成功
    # mafengwoLogin("13756567832", "000000001")
————————————————
版权声明：本文为CSDN博主「Kosmoo」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/zwq912318834/java/article/details/79571110