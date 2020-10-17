import web, datetime
import configparser
import os, sys

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

def insert_code(code, code_name, update_date, private_name, add_sub_store):
    db.insert('stock_private', code=code, code_name=code_name, update_date=update_date, private_name=private_name, add_sub_store=add_sub_store)

def get_all_datas():
    res = db.select('stock_private', order="update_date desc")
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def get_all_private_names():
    sql = 'select private_name from stock_private'
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i.private_name)
    return list(set(d_list))

def get_all_datas_on_page(pageSize, pageNo):
    a = (int(pageNo) - 1) * int(pageSize)
    sql = 'select * from stock_private order by update_date desc ,code asc limit ' + str(a) + ', ' + str(pageSize)
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def get_posts_count():
    sql = 'select count(*) aa from stock_private'
    res = db.query(sql)
    value = res[0].aa
    return value

def search(code):
    res = db.select('stock_private', where="code=$code", vars=locals())
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def search_from_name(name):
    sql = 'select * from stock_private where code_name like "%' + name + '%"'
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list


if __name__ == "__main__":
    print(get_all_private_names())