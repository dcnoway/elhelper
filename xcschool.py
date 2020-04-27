# coding=utf-8
import requests

import http.cookiejar as cookielib

# session代表某一次连接
session = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
session.cookies = cookielib.LWPCookieJar(filename = "xc.cookies")

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
    responseRes = session.post(postUrl, data = postData, headers = header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
    session.cookies.save()


if __name__ == "__main__":
    # 从返回结果来看，有登录成功
    xcLogin("xc062040074", "184385")
