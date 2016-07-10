#!/usr/bin/python
#-*- coding:utf-8 -*-
import urllib,re,urllib2,time,pickle
#需要在有道网站申请http://fanyi.youdao.com/openapi
KEYFROM = 'xxxxxxxx'
KEY = 'xxxx'
def getArticle(html):
    articlelist = []
    reg = r'https://www.newscientist.com/article/.+/"'
    article = re.compile(reg)
    articlelist0 = re.findall(article, html)
    '''删除重复内容'''
    articlelist1 = sorted(set(articlelist0), key=articlelist0.index)
    '''删除最后一个字符'''
    for str in articlelist1:
        str = str[:-1]
        articlelist.append(str)
    return articlelist
def getPara():
    paralist = []
    oldLinks = []
    oldArticle = []
    different = []
    r = urllib2.urlopen('https://www.newscientist.com/',timeout=1000)
    html = r.read()

    try:
        s = open('dump.txt', 'rb')
        oldLinks= pickle.load(s)
        oldArticle = [a[0] for a in oldLinks]
        s.close()
    except StandardError as e:
            pass
    s = open('dump.txt', 'wb')
    article = getArticle(html)
    if oldArticle == [] :
        unPublish = [[a, 0] for a in article]
        pickle.dump(unPublish, s)
        different = article
    elif list(set(article).difference(set(oldArticle))) != []:
        different = list(set(article).difference(set(oldArticle)))
        # 序列化文章标题,发布状态为未发布
        unPublish = [[a, 0] for a in different]
        pickle.dump(oldLinks + unPublish, s)
    else:
        unPublish = [[a, 0] for a in article]
        pickle.dump(unPublish, s)
        s.close()
        return 
    s.close()
    for article1 in different:
        r = urllib2.urlopen(article1,timeout=1000)
        html = r.read()

        #查找文章主题内容
        indexBegin =  html.find('article-content')
        indexEnd =  html.find('entry-content')
        content = html[indexBegin:indexEnd]
        regContent = r'<p>.+</p>'
        articleMatch = re.compile(regContent)
        contentlist = re.findall(articleMatch, content)
    
        for para in contentlist:
            indexBeginA = para.find('&#8220;<span')
            indexendA = para.find('&quot;:1}">')
            if indexBeginA >= 0:
                para = para[:indexBeginA] + para[indexendA + 11:]
    
            indexBeginA = para.find('<p><iframe')
            indexendA = para.find('</iframe></p>')
            if indexBeginA >= 0:
                para = para[:indexBeginA] + para[indexendA + 13:]
    
            while para.find('<a href') != -1:
                indexBeginA = para.find('<a href')
                indexendA = para.find('">')
                para = para[:indexBeginA]+para[indexendA+2:]
            para = para.replace('</a>','')
            para = para.replace('</span>&#8220;', '')
            para = para.replace('<p>','')
            para = para.replace('</p>','')
            para = para.replace('&#8217;',"'")
            para = para.replace('<em>', '')
            para = para.replace('</em>', '')
            para = para.replace('<strong>', '')
            para = para.replace('</strong>', '')
            para = para.replace(' – ', ',')#姑且这么替换
            para = para.replace('...', '')
            paralist.append(para)
        getTranslate(''.join(paralist))
        paralist = []


def getTranslate(para='This is empty.'):
    hydrid = []
    paralist = para.split('.')
    print paralist
    for paraTemp in paralist:
        if paraTemp.strip() == '':
            continue

        paraTemp = paraTemp.replace('\xc2\xa0', '')
        paraTemp2 = paraTemp.replace('&#8220;','%22').replace(' ','%20')
        paraTemp2 = paraTemp2.replace('&#8221;', '%22')
        paraTemp2 = paraTemp2.replace('"', '%22')
        paraTemp2 = paraTemp2.replace('\xe2\x80\x9c', '%22')
        paraTemp2 = paraTemp2.replace('\xe2\x80\x9d', '%22')
        paraTemp2 = paraTemp2.replace('\xe2\x80\x99', '%27')
        paraTemp2 = paraTemp2.replace("'", '%27')
        paraTemp2 = paraTemp2.replace('&#8211;', '%2D')

        url = "http://fanyi.youdao.com/openapi.do?keyfrom="+KEYFROM+"&key="+KEY+"&type=data&doctype=json&version=1.1&q="+paraTemp2
        r = urllib2.urlopen(url.encode('utf-8'), timeout=1000)
        temp = eval(r.read())
        temp['translation'][0] =  temp['translation'][0].replace('\u2022', '·')
        temp['translation'][0] = temp['translation'][0].replace('\u0080\u0099', "'")
        temp['translation'][0] = temp['translation'][0].replace('\u201C', '"')
        temp['translation'][0] = temp['translation'][0].replace('\u201D', '"')
        print temp['translation'][0]

        paraTemp = paraTemp.replace('&#8220;','"').lstrip()
        paraTemp = paraTemp.replace('&#8221;', '"')
        paraTemp = paraTemp.replace('&#8211;', '-')
        hydrid.append(paraTemp+'\r\n')
        hydrid.append(temp['translation'][0]+'\r\n')
        time.sleep(5)

    strTime = time.strftime('%Y_%m_%d_%H_%M_%S')
    f = open(strTime, "w+")
    f.writelines(hydrid)
    f.close()

if __name__ == "__main__":
    getPara()

