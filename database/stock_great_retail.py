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


def insert_code(code, name, update_date, shareholder_falling_count, sdlu_great_retail_count, float_share):
    create_date = str(int(time.time() * 1000))
    db.insert('stock_great_retail', code=code, name=name, update_date=update_date, shareholder_falling_count=shareholder_falling_count, sdlu_great_retail_count=sdlu_great_retail_count, float_share=float_share, create_date=create_date)

def delete_code(code, update_date):
    db.delete('stock_great_retail', where="id=$id", vars=locals())

def get_datas(date_data):
    res = db.select('stock_great_retail', where='update_date=$date_data', vars=locals())
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def get_all_datas():
    res = db.select('stock_great_retail', order="update_date desc")
    res_list = []
    for i in res:
        res_list.append(i)
    return res_list

def get_all_datas_on_page(pageSize, pageNo):
    a = (int(pageNo) - 1) * int(pageSize)
    sql = 'select * from stock_great_retail order by update_date desc , code asc limit ' + str(a) + ', ' + str(pageSize)
    res = db.query(sql)
    d_list = []
    for i in res:
        d_list.append(i)
    return d_list

def get_posts_count():
    sql = 'select count(*) aa from stock_great_retail'
    res = db.query(sql)
    value = res[0].aa
    return value


if __name__ == "__main__":
    # insert_code('a', '2020-10-10', 2, 2, 1.999)
    print(get_datas('20201009'))