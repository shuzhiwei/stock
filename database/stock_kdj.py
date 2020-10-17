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


def insert_code(code, code_name, update_date, if_gold_cross, shareholdersFallingCount, sdluCount, float_share):
    db.insert('stock_kdj', code=code, code_name=code_name, update_date=update_date,
               if_gold_cross=if_gold_cross, shareholder_falling_count=shareholdersFallingCount,
               sdlu_great_retail_count=sdluCount, float_share=float_share)

def get_datas(date_data):
    res = db.select('stock_kdj', where='update_date=$date_data', vars=locals())
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def get_all_datas():
    res = db.select('stock_kdj', order="update_date desc")
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def get_all_datas_on_page(pageSize, pageNo):
    a = (int(pageNo) - 1) * int(pageSize)
    # sql = 'select * from stock_kdj order by update_date desc limit ' + str(a) + ', ' + str(pageSize)
    sql = 'select * from stock_kdj order by update_date desc, id asc limit ' + str(pageSize) + ' OFFSET ' + str(a)
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def get_posts_count():
    sql = 'select count(*) aa from stock_kdj'
    res = db.query(sql)
    value = res[0].aa
    return value

def delete_code(id):
    db.delete('stock_kdj', where="id=$id", vars=locals())


if __name__ == "__main__":
    print(get_all_datas_on_page(8, 2))