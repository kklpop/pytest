# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import re
URL='https://movie.douban.com/coming'
DOUBANAPI='https://api.douban.com/v2/movie'
def get_html(url,writeflag):           #writeflag数组 [是否写入标志] [写入文件名]
    #url = 'https://movie.douban.com/coming'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
    }
    r = requests.get(url, headers=headers)
    if writeflag[0]=='y':
        try:
            with open(writeflag[1], "w") as f:
                f.write(r.text)
        except Exception as e:
            print("写入错误")
    elif writeflag[0]=='n':
        return r.text

def analyze_filmscoming():
    try:
        with open('coming.txt', "r") as f:
            soup = BeautifulSoup(f.read(), 'lxml')
    except Exception as e:
        print("读取错误")

    wr=''
    i=0
    e=0
    for td in soup.find_all(name='td'):
        #print(td.string)
        if td.string!=None and i!=5:
            wr=wr+str(td.string).strip()+','
        elif i==5:
            wr = wr + str(td.string).strip() + '\n'
            i=0
        i=i+1
        #print(wr)
        for a in td.find_all(name='a'):
            if a.string!=None and e!=0:
                wr = wr + str(a.string).strip()+','+a.get('href')+','
                #print(a.get('href'))
            e=e+1

    with open('td.txt', "w") as f:
        f.write(wr)

def get_filmdetail(url):
    filmsdetail=('n','')
    html=get_html(url,filmsdetail)
    fsoup = BeautifulSoup(html, 'lxml')
    #print(fdetail.find('h1',name='span').string)
    fdetail=''
    for child in fsoup.h1.children:
        #print(str(child.string).strip())
        fdetail=fdetail+str(child.string).strip()
    print(fdetail)

    '''for i in fsoup.find_all(re.compile('span')):
        print(i.text)'''

    info=fsoup.find(id='info')

    #for d in info:
    #e=re.findall('rel="v:directedBy">(.*?)</a>',str(info))
    print("导演："+','.join(re.findall('rel="v:directedBy">(.*?)</a>',str(info))))
    print("编剧：" + ','.join(re.findall('<a href=".*?\/\">(.*?)</a>', str(info))))
    print("演员：" + ','.join(re.findall('<a.*?rel="v:starring">(.*?)</a>', str(info))))
    print("片长：" + ','.join(re.findall('property="v:runtime".*?>(.*?)</span>', str(fsoup))))
    #print("又名：" + ','.join(re.findall('\:</span>(.*?)<br>', str(info))))


    #print (type(i))
    #for a in i.find_all('a'):
    #print(a.string)
    '''for child in fsoup.find(id='info'):
        if str(type(child))!='<class \'bs4.element.NavigableString\'>':
            for span in child.children:
                if str(type(span)) != '<class \'bs4.element.NavigableString\'>':
                    #for a in span.find(name='a'):

                    #print(str(span.string))
                    r=span.find_all(name='a')
                    print(r)
                    print (type(r))'''
                #print(type(span))
        #print(str(child.string).strip())
        #print(type(child))



if __name__ == "__main__":
    '''filmscoming =('y','coming.txt')

    get_html(URL,filmscoming)
    analyze_filmscoming()'''
    get_filmdetail('https://movie.douban.com/subject/27605698/')


    #result = urlsplit('https://movie.douban.com/subject/27605698/')
    #print (result.path)
    '''https://api.douban.com/v2/movie/subject/1764796'''
    '''test'''