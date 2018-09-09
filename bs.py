# coding: utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
URL='https://movie.douban.com/coming'
DOUBANAPI='https://api.douban.com/v2/movie'
def get_html(url,writeflag):           #writeflag数组 [是否写入标志] [写入文件名]
    #url = 'https://movie.douban.com/coming'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
    }
    r = requests.get(url, headers=headers,timeout=10)
    if writeflag[0]=='y':
        try:
            with open(writeflag[1], "w",encoding='utf-8') as f:
                f.write(r.text)
                print('ok')
        except Exception as e:
            print(str(e)+"写入错误")
    #elif writeflag[0]=='n':
    return r.text

def get_html_withphantomjs(url):
    browser=webdriver.Chrome()
    browser.get(url)

    cookies = browser.get_cookies()
    print(cookies)
    browser.delete_all_cookies()
    browser.add_cookie({'name': 'country', 'value': 'all'})  # 加cookies
    browser.get(url)

    wait = WebDriverWait(browser, 2)
    wait.until(EC.presence_of_element_located((By.ID, 'movielist')))
    try:
        with open('bluray.html', "w",encoding='utf-8') as f:
            absoup = BeautifulSoup(browser.page_source, 'lxml')
            info=absoup.find(id='movielist')
            f.write(str(info))

    except Exception as e:
        print(str(e)+"写入错误")
    result=browser.page_source
    browser.close()
    return result

def analyze_filmscoming_indouban():
    temp=''
    furl=[]
    try:
        with open('coming.txt', "r",encoding='utf-8') as f:
            #dbsoup = BeautifulSoup(f.read(), 'lxml')
            temp=f.read()
    except Exception as e:
        print(str(e)+"读取错误")
    dbsoup=BeautifulSoup(temp, 'lxml')
    wr=''
    i=0
    e=0
    for td in dbsoup.find_all(name='td'):
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
                furl.append(a.get('href'))
            e=e+1
    #print(furl)
    with open('td.txt', "w") as f:
        f.write(wr)

def get_filmdetail_indouban(url):
    filmsdetail=('n','')
    html=get_html(url,filmsdetail)
    fsoup = BeautifulSoup(html, 'lxml')
    #print(fdetail.find('h1',name='span').string)
    fntemp=''
    '''for child in fsoup.h1.children:
        #print(str(child.string).strip())
        fntemp=fntemp+str(child.string).strip()
    t=re.findall('[\u4e00-\u9fa5]',fntemp)
    tm=''.join(t)+'(.*?)\('
    print(tm)

    res=re.findall('.*[\u4E00-\u9FA5](.*?)\(',fntemp)
    print(res[0].strip())'''

    info=fsoup.find(id='info')
    d = fsoup.find(property ="v:summary")
    print("导演："+','.join(re.findall('rel="v:directedBy">(.*?)</a>',str(info))))
    print("编剧：" + ','.join(re.findall('<a href=".*?\/\">(.*?)</a>', str(info))))
    print("演员：" + ','.join(re.findall('<a.*?rel="v:starring">(.*?)</a>', str(info))))
    print("片长：" + ','.join(re.findall('property="v:runtime".*?>(.*?)</span>', str(info))))
    print("评分：" + ','.join(re.findall('property="v:average">(.*?)</strong>', str(fsoup))))
    print("IMDb：" + ','.join(re.findall('<a href="(.*?)" rel="nofollow"', str(info))))
    print("简介：" +d.text.strip())
    print("上映时间：" + ','.join(re.findall('property="v:initialReleaseDate">(.*?)\(.*\)', str(info))))
    datetmp=','.join(re.findall('property="v:initialReleaseDate">(.*?)</span>', str(info)))
    #date=re.findall('(.*?)\(',datetmp)
    return datetmp
def get_filmbluray_inbluray(fename):
    bluray=('y','bluray.html')
    #html = get_html_withphantomjs(url)
    try:
        with open('bluray.html', "r",encoding='utf-8') as f:
            bsoup = BeautifulSoup(f.read(), 'lxml')
    except Exception as e:
        print(str(e)+"读取错误")

    #blurayinfo=bsoup.find(id='movielist')
    #a=blurayinfo.find(text='Game of Thrones: The Compl.')
    try:
        a=bsoup.find(title=fename+' (Blu-ray)')
        print(a)
        b=list(a.parents)[4] #影片的父节点
        print(list(b.previous_siblings)[3].get_text()) #父节点的兄弟节点 找出日期
        print(formate_date(list(b.previous_siblings)[3].get_text()))
    except Exception as e:
        print(str(e)+"未找到")

def formate_date(data):
    month={'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08',
           'September':'09','October':'10','November':'11','December':'12',}
    #data = data.strip(',')
    list= data.split()
    return (list[2]+'-'+month[list[0]]+'-'+list[1].strip(','))

def get_intdFilmname():
    y = ('y', 'Mtimeintroduce.html')
    #self.get_html(MTIMEURL, y)
    ftmpE = []
    ftmp=[]
    fdic={}
        # print(b)
    try:
        with open(y[1], "r", encoding='utf-8') as f:
            bsoup = BeautifulSoup(f.read(), 'lxml')
    except Exception as e:
        print(str(e) + "读取错误")
    # h4=bsoup.find_all('h4')
    '''for h4 in bsoup.find_all('h4'):    # h4 英文标题
        ftmpE.append(h4.string)
    for i in ftmpE:                    # 去重
        if i not in self.fnameE or i==None:
            self.fnameE.append(i)

    for h3 in bsoup.find_all('h3'):    #h3 中文标题
        ftmp.append(h3.string)
    for i in ftmp:
        if i not in self.fname and i!=None:
            self.fname.append(i)'''

    for h4,h3 in zip(bsoup.find_all('h4'),bsoup.find_all('h3')):
        fdic[h3.string]=h4.string
    return fdic
if __name__ == "__main__":
    blurl='http://www.blu-ray.com/movies/releasedates.php?'
    '''filmscoming =('y','coming.txt')

    get_html(URL,filmscoming)
    analyze_filmscoming_indouban()'''
    '''date=get_filmdetail_indouban('https://movie.douban.com/subject/30122633/')
    ix=date.find('(中国大陆)')
    i=date.find(',')
    if ix!=-1:
        print('大陆上映：'+date[0:ix])
        if i!=-1:
            print('国外上映：'+date[i+1:i+11])
    else:
        print('国外上映：')'''
    st='2018-02-01'
    if st.count('-')==1 and st[-2:]=='02':
        st=st+'-28'
    elif st.count('-')==1:
        st=st+'-30'
    print(st)
    '''for y in range(2018,2020):
        for m in range(1,13):
            year='year='+str(y)
            month='&month='+str(m)
            #print(year,month)
            get_html_withphantomjs(blurl+year+month)
    n='I, Tonya'
    get_filmbluray_inbluray(n)'''
    #fd=get_intdFilmname()

    print('d')

    #result = urlsplit('https://movie.douban.com/subject/27605698/')
    #print (result.path)
    '''https://api.douban.com/v2/movie/subject/1764796'''
    '''test'''