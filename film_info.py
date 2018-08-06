# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import json

URL='https://movie.douban.com/coming'
DOUBANAPI='https://api.douban.com/v2/movie'

class FilmInfo:
    def __init__(self):
        self.fname=''
        self.fdate=''
        self.ftype=''
        self.fcountry=''
        self.fexpect=''
        self.fstar=''
        ''' ________detail________    '''
        self.fdirector=''
        self.fwriter=''
        self.factor=''
        self.flong=''
        self.fnameE=''
        self.furl=[]

    def get_html(self, url, writeflag):  # writeflag数组 [是否写入标志] [写入文件名]
        # url = 'https://movie.douban.com/coming'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept - Language': 'zh - CN, zh;q = 0.8, en - US;q = 0.5, en;q = 0.3'
        }
        try:
            r = requests.get(url, headers=headers,timeout=10,allow_redirects=False)
        except Exception as e:
            print(e)
        if writeflag[0] == 'y':
            try:
                with open(writeflag[1], "w") as f:
                    f.write(r.text)
            except Exception as e:
                print(e + "写入错误")
        elif writeflag[0] == 'n':
            return r.text

    def analyze_filmscoming(self,fpath):
        try:
            with open(fpath, "r") as f:
                soup = BeautifulSoup(f.read(), 'lxml')
        except Exception as e:
            print(e + "读取错误")

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
                    wr = wr + str(a.string).strip() + ',' + a.get('href') + ','
                    # print(a.get('href'))
                    self.furl.append(a.get('href'))
                e = e + 1

        try:
            with open('onshow.txt', "w") as f:
                f.write(wr)
        except Exception as e:
            print(e + "写入错误")

    def get_filmdetail(self,url):
        temp=(urlsplit(url).path)
        fdouban_api_url= str(DOUBANAPI + temp)
        fdetail_html=self.get_html(fdouban_api_url, ('n', ''))
        json_html=json.dumps(fdetail_html)
        # 将 JSON 对象转换为 Python 字典
        fdetail=json.loads(json_html)
        print(fdetail_html)
if __name__ == "__main__":
    filmscoming = ('y', 'coming.txt')
    info=FilmInfo()
    info.get_html(URL,filmscoming)
    info.analyze_filmscoming(filmscoming[1])
    #print(info.furl)
    info.get_filmdetail(info.furl[1])