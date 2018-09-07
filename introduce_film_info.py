# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import re
import time
MTIMEURL='http://movie.mtime.com/comingsoon/#introduce'
DOUBANAPI='https://api.douban.com/v2/movie/search?q='

class IntdFilmInfo:
    def __init__(self):
        self.fname = ''
        self.fdate = ''  #上映日期
        self.foutdate='' #国外上映日期
        self.fintdate='' #国内上映日期
        self.ftype = ''
        self.fcountry = ''
        self.fexpect = ''
        self.fstar = ''
        ''' ________detail________    '''
        self.fdirector = ''
        self.fwriter = ''
        self.factor = ''
        self.flong =''
        self.fnameE = 'null'
        self.fbluraydate=''
        self.fsummary=''
        self.fpicsrc=''
        self.furl=''

class IntdFilmInfoMethod:
    def __init__(self):
        #self.fnameE=[]
        #self.fname=[]
        self.fnamedic={}
    def get_html(self, url, writeflag):  # writeflag数组 [是否写入标志] [写入文件名]
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
                    brsoup = BeautifulSoup(r.text, 'lxml')
                    info = brsoup.find_all(class_='tab2')
                    f.write(str(info))
                    #f.write(r.text)
            except Exception as e:
                print(str(e) + "写入错误")
        # elif writeflag[0]=='n':
        return r.text.encode('utf-8')
    def get_intdFilmname(self):
        y = ('y', 'Mtimeintroduce.html')
        self.get_html(MTIMEURL, y)
        ftmpE = []
        ftmp=[]
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
        try:
            for h4, h3 in zip(bsoup.find_all('h4'), bsoup.find_all('h3')):
                self.fnamedic[h3.string] = h4.string
        except Exception as e:
            print(str(e) + "读取电影名称错误")

    def get_intdFilminfo_json(self,url,intdfinfo,fname,fnamE):    #通过豆瓣api search得到电影信息
        info=self.get_html(url,('n',''))
        fdic=json.loads(info)
        try:
            subjects=fdic['subjects']
            for sub in subjects:
                #print(sub['original_title'])
                if fname==sub['title'] or fnamE==sub['original_title']:
                    #intdfinfo.fname=sub['title']
                    intdfinfo.fnameE=fnamE
                    intdfinfo.furl = sub['alt']
                    try:
                        for t in sub['directors']:
                            intdfinfo.fdirector=intdfinfo.fdirector+t['name']+' '
                    except Exception as e:
                        print(str(e))
                    try:
                        for t in sub['genres']:
                            intdfinfo.ftype=intdfinfo.ftype+t+' '
                    except Exception as e:
                        print(str(e))
                    try:
                        for t in sub['casts']:
                            intdfinfo.factor = intdfinfo.factor + t['name'] + ' '
                    except Exception as e:
                        print(str(e))
        except Exception as e:
            print(str(e)+'豆瓣api查询失败')

    def get_restof_intdFilminfo(self,url,finfo):     #得到所有电影信息 豆瓣
        filmsdetail = ('n', '')
        html = self.get_html(url, filmsdetail)
        #html.decode('utf-8')
        fsoup = BeautifulSoup(html, 'lxml')
        fname = ''
        for child in fsoup.h1.children:
            # print(str(child.string).strip())
            fname = fname + str(child.string).strip()
        try:
            info = fsoup.find(id='info')
            summary = fsoup.find(property="v:summary")
            mainpic = fsoup.find(id='mainpic')
            picsrc = mainpic.find(rel='v:image')
            finfo.fpicsrc = picsrc.get('src')
            finfo.fname=fname
            #finfo.fdirector = ','.join(re.findall('rel="v:directedBy">(.*?)</a>', str(info)))
            finfo.fwriter = ','.join(re.findall('<a href=".*?\/\">(.*?)</a>', str(info)))
            #finfo.factor = ','.join(re.findall('<a.*?rel="v:starring">(.*?)</a>', str(info)))
            finfo.flong = ','.join(re.findall('property="v:runtime".*?>(.*?)</span>', str(info)))
            finfo.fstar = ','.join(re.findall('property="v:average">(.*?)</strong>', str(fsoup)))
            finfo.fsummary = summary.text.strip()
            #print("上映时间：" + ','.join(re.findall('property="v:initialReleaseDate">(.*?)\(', str(info))))
            finfo.fdate=','.join(re.findall('property="v:initialReleaseDate">(.*?)\(', str(info)))
            datetmp = ','.join(re.findall('property="v:initialReleaseDate">(.*?)</span>', str(info)))
            ix = datetmp.find('(中国大陆)')  # 获得国内外上映时间
            i = datetmp.find(',')
            if ix != -1:
                # print('大陆上映：' + datetmp[0:ix])
                finfo.fintdate = datetmp[0:ix]
                if i != -1:
                    finfo.foutdate = datetmp[i + 1:i + 11]
                    # print('国外上映：' + datetmp[i + 1:i + 11])
            else:
                finfo.foutdate = finfo.fdate
        except Exception as e:
            print(str(e) + "电影信息获取失败")

if __name__ == '__main__':
    fintd=IntdFilmInfoMethod()
    intdfinfolist=[]
    y=('y','test.html')
    n=('n','')
    fintd.get_intdFilmname()

    for fname,fnamE in fintd.fnamedic.items():
        url=DOUBANAPI+fname
        intdfinfo = IntdFilmInfo()
        fintd.get_intdFilminfo_json(url,intdfinfo,fname,fnamE)
        time.sleep(1)
        intdfinfolist.append(intdfinfo)
    '''for intdfinfo in intdfinfolist:
        fintd.get_restof_intdFilminfo(intdfinfo.furl,intdfinfo)
        time.sleep(1)'''

    print('d')
