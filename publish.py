#!/usr/bin/python
#-*- coding:utf-8 -*-
"""
引入Python SDK的包
"""
import weibo


"""
授权需要的三个信息,APP_KEY、APP_SECRET均需在微博开放平台注册后获得，CALL_BACK在微博开放平台应用的设置网页中
设置的。【注意】这里授权时使用的CALL_BACK地址与应用中设置的CALL_BACK必须一致，否则会出
现redirect_uri_mismatch的错误。
"""
APP_KEY = 'xxxxxxx'
APP_SECRET = 'xxxxxxxxxxxxxxxxxx'
CALL_BACK = 'https://api.weibo.com/oauth2/default.html'

def run():
#weibo模块的APIClient是进行授权、API操作的类，先定义一个该类对象，传入参数为APP_KEY, APP_SECRET, CALL_BACK
        client = weibo.APIClient(APP_KEY, APP_SECRET, CALL_BACK)
#获取该应用（APP_KEY是唯一的）提供给用户进行授权的url
        auth_url = client.get_authorize_url()
#打印出用户进行授权的url，将该url拷贝到浏览器中，服务器将会返回一个url，该url中包含一个code字段（如图1所示）
        print "auth_url : " + auth_url
#输入该code值（如图2所示）
        code = raw_input("input the retured code : ")
#通过该code获取access_token，r是返回的授权结果，具体参数参考官方文档：
# http://open.weibo.com/wiki/Oauth2/access_token
        r = client.request_access_token(code)
#将access_token和expire_in设置到client对象
        client.set_access_token(r.access_token, r.expires_in)

#以上步骤就是授权的过程，现在的client就可以随意调用接口进行微博操作了，下面的代码就是用用户输入的内容发一条新微博
#将翻译好的文件复制到text子文件夹下。因为newscientist网址获取经常会超时,必须先在台式机上利用getData.py和vpn获取,再在树莓派上发布
        files = os.listdir('./text')
        for onefile in files:
                txt = './text/' + onefile
                textToPic.tToP(txt)
                file = open(txt, 'r')
                title = file.readline()
                #  client.statuses.update.post(status=content)
                f = open(txt+'.jpg', 'rb')
                client.statuses.upload.post(status=title, pic=f)
                f.close() # APIClient不会自动关闭文件，需要手动关闭
                print "Send succesfully!"

                time.sleep(3*60*60)

if __name__ == "__main__":
        run()

