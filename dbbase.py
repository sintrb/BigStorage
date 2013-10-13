# -*- coding: UTF-8 -*
'''
Created on 2013-9-29

@author: RobinTang
'''

import MySQLdb

def get_connect(dbn='dbp'):
    '''获取数据库连接'''
    try:
    #    尝试对SAE的数据库进行连接
        import sae
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST,user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB,port=int(sae.const.MYSQL_PORT))
    except:
    #    连接失败，那么就认为是在本地环境
        conn=MySQLdb.connect(host='127.0.0.1',user='trb',passwd='123',db=dbn,port=3306)
    conn.set_character_set('utf8')
    return conn