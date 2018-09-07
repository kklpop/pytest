# coding: utf-8

import pymysql
#from film_info import FilmInfo
HOST='127.0.0.1'
USER='root'
PSW='123456'
PORT=3306
DB='films_info'
class Sqlop:
    def __init__(self):
        try:
            self.db=pymysql.connect(host=HOST,user=USER,password=PSW,port=PORT,db=DB)
            self.cursor=self.db.cursor()
        except Exception as e:
            print(str(e) + "数据库链接错误")

    def save_onshow(self,filmsinfo):
        '''procedure pr_update_onshow_table(
        IN p_fname varchar(100),
        IN p_fdate varchar(10),
        IN p_foutdate varchar(12),
        IN p_findate varchar(12),
        IN p_ftype varchar(40),
        IN p_fcountry varchar(40),
        IN p_fexpect varchar(10),
        IN p_fstar varchar(10),
        IN p_fdirector varchar(40),
        IN p_fwriter varchar(40),
        IN p_factor varchar(100),
        IN p_flong varchar(10),
        IN p_fnameE varchar(100),
        IN p_fblueraydate varchar(12),
        IN p_fsummary varchar(1000),
        IN p_fpicsrc varchar(200))'''
        sql='call pr_update_filminfo_table(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql,(filmsinfo.fname,filmsinfo.fdate,filmsinfo.foutdate,filmsinfo.findate,filmsinfo.ftype,filmsinfo.fcountry,filmsinfo.fexpect,
                                     filmsinfo.fstar,filmsinfo.fdirector,filmsinfo.fwriter,filmsinfo.factor,filmsinfo.flong,
                                     filmsinfo.fnameE,filmsinfo.fbluraydate,filmsinfo.fsummary,filmsinfo.fpicsrc))
            self.db.commit()
        except Exception as e:
            print(str(e) + "onshow存储过程错误")
            self.db.rollback()
    def close_db(self):
        self.db.close()
if __name__ == '__main__':
    '''fi=FilmInfo()
    fi.fname='ttt'
    fi.fexpect='4many'
    fi.fshowdate='02-13'
    fi.factor='jkl'''''
    s=Sqlop()
    #s.save_onshow(fi)
    print('d')