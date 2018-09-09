# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from sql_op import Sqlop
DOUBANURL='https://movie.douban.com/coming'

class FilmInfo:
    def __init__(self):
        self.fname = ''
        self.fdate = ''     # 上映日期
        self.foutdate = ''  # 国外上映日期
        self.findate = ''  # 国内上映日期
        self.ftype = ''
        self.fcountry = ''
        self.fexpect = ''
        self.fstar = ''
        ''' ________detail________    '''
        self.fdirector = ''
        self.fwriter = ''
        self.factor = ''
        self.flong = ''
        self.fnameE = 'null'
        self.fbluraydate=''
        self.fsummary=''
        self.fpicsrc=''
        self.furl=''

class FilmInfoMethod:
    def __init__(self):
        self.furl=[]

    def get_doubanhtml(self, url, writeflag):  # writeflag数组 [是否写入标志] [写入文件名]
        # url = 'https://movie.douban.com/coming'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
        }
        try:
            r = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print(str(e) + "request错误")
            return 'null'
        if writeflag[0] == 'y':
            try:
                with open(writeflag[1], "w", encoding='utf-8') as f:
                    f.write(r.text)
            except Exception as e:
                print(str(e) + "写入错误")
        # elif writeflag[0]=='n':
        return r.text.encode('utf-8')

    def get_html_withphantomjs(url):
        browser = webdriver.PhantomJS()
        # browser.get(url)
        # browser.add_cookie({'name': 'country', 'value': 'all'})  # 加cookies
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'movielist')))
        try:
            with open('bluray.html', "a", encoding='utf-8') as f:
                brsoup = BeautifulSoup(browser.page_source, 'lxml')
                info = brsoup.find(id='movielist')
                f.write(str(info))
        except Exception as e:
            print(str(e) + "写入错误")
        result = info
        browser.close()
        return result

    def analyze_filmscoming(self,fpath):
        temp=''
        try:
            with open(fpath, "r",encoding='utf-8') as f:
                temp=f.read()
        except Exception as e:
            print(str(e) + "读取错误")
        soup = BeautifulSoup(temp, 'lxml')
        wr = ''
        i = 0
        e = 0
        for td in soup.find_all(name='td'):
            # print(td.string)
            if td.string != None and i != 5:
                wr = wr + str(td.string).strip() + ','
            elif i == 5:
                wr = wr + str(td.string).strip() + '\n'
                i = 0
            i = i + 1
            # print(wr)
            for a in td.find_all(name='a'):
                if a.string != None and e != 0:
                    wr = wr + str(a.string).strip() + ','       #+ a.get('href') + ','
                    # print(a.get('href'))
                    self.furl.append(a.get('href'))
                e = e + 1

        try:
            with open('onshow.txt', "w") as f:
                f.write(wr)
        except Exception as e:
            print(e + "写入错误")

    def get_filmdetail_indouban(self,url,finfo):
        filmsdetail = ('n', '')
        html = self.get_doubanhtml(url, filmsdetail)
        html.decode('utf-8')
        fsoup = BeautifulSoup(html, 'lxml')
        # print(fdetail.find('h1',name='span').string)
        fname = ''
        for child in fsoup.h1.children:
            # print(str(child.string).strip())
            fname = fname + str(child.string).strip()

        fename = re.findall('.*[\u4E00-\u9FA5](.*?)\(', fname)
        info = fsoup.find(id='info')
        summary = fsoup.find(property="v:summary")
        mainpic=fsoup.find(id='mainpic')
        picsrc=mainpic.find(rel='v:image')
        '''try:
            print(fname)
            print(fename[0].strip())
            print("导演：" + ','.join(re.findall('rel="v:directedBy">(.*?)</a>', str(info))))
            print("编剧：" + ','.join(re.findall('<a href=".*?\/\">(.*?)</a>', str(info))))
            print("演员：" + ','.join(re.findall('<a.*?rel="v:starring">(.*?)</a>', str(info))))
            print("简介：" + d.text.strip())
        except Exception as e:
            print(str(e) + "字符错误")
        print(picsrc.get('src'))
        print("片长：" + ','.join(re.findall('property="v:runtime".*?>(.*?)</span>', str(info))))
        print("评分：" + ','.join(re.findall('property="v:average">(.*?)</strong>', str(fsoup))))
        print("IMDb：" + ','.join(re.findall('<a href="(.*?)" rel="nofollow"', str(info))))'''
        try:
            finfo.fname=fname
            finfo.fnameE=fename[0].strip()
            finfo.fdirector=','.join(re.findall('rel="v:directedBy">(.*?)</a>', str(info)))
            finfo.fwriter=','.join(re.findall('<a href=".*?\/\">(.*?)</a>', str(info)))
            finfo.factor=','.join(re.findall('<a.*?rel="v:starring">(.*?)</a>', str(info)))
            finfo.flong=','.join(re.findall('property="v:runtime".*?>(.*?)</span>', str(info)))
            finfo.fstar=','.join(re.findall('property="v:average">(.*?)</strong>', str(fsoup)))
            finfo.fsummary=summary.text.strip()
            finfo.fpicsrc=picsrc.get('src')
            finfo.fdate=','.join(re.findall('property="v:initialReleaseDate">(.*?)\(.*\)', str(info)))
            finfo.fdate=add_daytime(finfo.fdate)
            datetmp = ','.join(re.findall('property="v:initialReleaseDate">(.*?)</span>', str(info)))
            ix = datetmp.find('(中国大陆)')      #获得国内外上映时间
            i = datetmp.find(',')
            if ix != -1:
                #print('大陆上映：' + datetmp[0:ix])
                finfo.findate=datetmp[0:ix]
                if i != -1:
                    finfo.foutdate=datetmp[i + 1:i + 11]
                    #print('国外上映：' + datetmp[i + 1:i + 11])
            else:
                finfo.foutdate=finfo.fdate
                #print('国外上映：')
        except Exception as e:
            print(str(e) + "onshow电影信息获取错误")

    def get_filmbluray_inbluray(self,fname,finfo):
        #bluray = ('y', 'bluray.html')
        #html = self.get_html_withphantomjs(url)
        year = datetime.datetime.now().strftime('%Y')
        for y in range(int(year),int(year)+2):
            try:
                with open(str(y)+'bluray.html', "r", encoding='utf-8') as f:
                    bsoup = BeautifulSoup(f.read(), 'lxml')
            except Exception as e:
                print(str(e) + "读取错误")
            try:
                a = bsoup.find(title=fname + ' (Blu-ray)')
                #print(a)
                b = list(a.parents)[4]  # 影片的父节点
                #print(list(b.previous_siblings)[3].get_text())  # 父节点的兄弟节点 找出日期
                print(self.formate_date(list(b.previous_siblings)[3].get_text()))
                finfo.fbluraydate=self.formate_date(list(b.previous_siblings)[3].get_text())
            except Exception as e:
                print(str(e) + "没有蓝光发售日期")

    def formate_date(data):
        month = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                 'July': '07', 'August': '08',
                 'September': '09', 'October': '10', 'November': '11', 'December': '12', }
        # data = data.strip(',')
        list = data.split()
        return (list[2] + '-' + month[list[0]] + '-' + list[1].strip(','))
def add_daytime(st):
    if st.count('-')==1 and st[-2:]=='02':
        st=st+'-28'
    elif st.count('-')==1:
        st=st+'-30'
    return st
def get_fonshow_info(finfo):
    try:
        with open('onshow.txt', "r") as f:
            lines=f.readlines()
            i=0
            for line in lines:
                info=line.split(',')
                #finfo[i].fshowdate=info[0]
                finfo[i].ftype=info[2]
                finfo[i].fcountry=info[3]
                finfo[i].fexpect=info[4].rstrip()
                i=i+1

    except Exception as e:
        print(e + "onshow读取错误")
if __name__ == "__main__":
    coming = ('y', 'coming.txt')
    method=FilmInfoMethod()

    flist=[]
    method.get_doubanhtml(DOUBANURL,coming)
    method.analyze_filmscoming(coming[1])
    #print(info.furl)
    for url in method.furl:
        finfos = FilmInfo()
        method.get_filmdetail_indouban(url,finfos)
        finfos.furl=url
        #method.get_filmbluray_inbluray(finfos.fnameE,finfos)
        flist.append(finfos)
    get_fonshow_info(flist)

    print(flist[1])
    sqlop=Sqlop()
    for ftmp in flist:
        sqlop.save_onshow(ftmp)
    sqlop.close_db()
    print('down')
