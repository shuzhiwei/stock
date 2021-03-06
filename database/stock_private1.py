import web, datetime
import configparser
import os, sys, time

# 解析配置
parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/../confs/config.ini'
config.read(full_path)

host = config.get('mysql', 'host')
port = config.getint('mysql', 'port')
user = config.get('mysql', 'user')
db = config.get('mysql', 'db')
password = config.get('mysql', 'password')

db = web.database(dbn='mysql',host=host, port=port, user=user, pw=password, db=db)

def insert_data(private_name, code_name, add_sub_store, update_date):
    create_date = str(int(time.time() * 1000))
    db.insert('stock_private1', private_name=private_name, code_name=code_name,
                                add_sub_store=add_sub_store, update_date=update_date, create_date=create_date)
                            

def existData(private_name):
    sql = 'select * from stock_private1 where private_name="' + private_name + '"' 
    res = db.query(sql)
    if res:
        return True
    else:
        return False

def updateData(private_name, code_name, add_sub_store, update_date):
    sql = 'update stock_private1 set code_name="' + code_name + \
          '" , add_sub_store="' + add_sub_store + '" , update_date="' + update_date + '" where private_name="' + \
          private_name + '"'
    db.query(sql)

def get_all_datas_on_page(pageSize, pageNo):
    a = (int(pageNo) - 1) * int(pageSize)
    sql = 'select * from stock_private1 where type=0 limit ' + str(a) + ', ' + str(pageSize)
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def get_one_data(private_name):
    sql = 'select * from stock_private1 where private_name="' + private_name + '"'
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def get_all_datas_on_page_on_favorites(pageSize, pageNo):
    a = (int(pageNo) - 1) * int(pageSize)
    sql = 'select * from stock_private1 where type=1 limit ' + str(a) + ', ' + str(pageSize)
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def update_favorites(private_name, _type):
    sql = 'update stock_private1 set type=' + str(_type) + ' where private_name="' + private_name + '"'
    db.query(sql)

def get_posts_count():
    sql = 'select count(*) aa from stock_private1'
    res = db.query(sql)
    value = res[0].aa
    return value

def get_posts_count_on_favorites():
    sql = 'select count(*) aa from stock_private1 where type=1'
    res = db.query(sql)
    value = res[0].aa
    return value

def search_from_name(name):
    sql = 'select * from stock_private1 where private_name like "%' + name + '%"'
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

if __name__ == "__main__":
    print(existData('深圳市和沣资产管理有限公司-和沣共赢私募证券投资基金'))
