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

if __name__ == "__main__":
    print(get_all_datas())