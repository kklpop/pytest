# coding: utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime
def get_html_withphantomjs(url,year):
    browser = webdriver.PhantomJS()
    browser.get(url)
    browser.delete_all_cookies()
    browser.add_cookie({'domain': '.blu-ray.com','name': 'country', 'value': 'all','path': '/',
      'expires': None})  # 加cookies
    browser.get(url)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.presence_of_element_located((By.ID, 'movielist')))

    #for y in range(year,year+2):
    try:
        with open(year+'bluray.html', "a", encoding='utf-8') as f:
            brsoup = BeautifulSoup(browser.page_source, 'lxml')
            info = brsoup.find(id='movielist')
            f.write(str(info))
    except Exception as e:
        print(str(e) + "写入错误")
    result = info
    browser.close()
    return result

def get_filmbluray_inbluray(fename):
    #bluray = ('y', 'bluray.html')
    #html = self.get_html_withphantomjs(url)
    try:
        with open('bluray.html', "r", encoding='utf-8') as f:
            bsoup = BeautifulSoup(f.read(), 'lxml')
    except Exception as e:
        print(str(e) + "读取错误")

    try:
        a=bsoup.find(title=fename+' (Blu-ray)')
        print(a)
        b=list(a.parents)[4] #影片的父节点
        print(list(b.previous_siblings)[3].get_text()) #父节点的兄弟节点 找出日期
        print(formate_date(list(b.previous_siblings)[3].get_text()))
    except Exception as e:
        print(str(e)+"未找到")

def formate_date(data):
    month = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                 'July': '07', 'August': '08',
                 'September': '09', 'October': '10', 'November': '11', 'December': '12', }
    # data = data.strip(',')
    list = data.split()
    return (list[2] + '-' + month[list[0]] + '-' + list[1].strip(','))

if __name__ == '__main__':
    blurl = 'http://www.blu-ray.com/movies/releasedates.php?'
    year=datetime.datetime.now().strftime('%Y')
    nextyear=int(year)+2
    print(year,nextyear)
    for y in range(int(year), nextyear):
        for m in range(1, 13):
            pyear = 'year=' + str(y)
            pmonth = '&month=' + str(m)
            # print(year,month)
            get_html_withphantomjs(blurl + pyear + pmonth, str(y))