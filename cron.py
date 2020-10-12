import time, requests
import pandas as pd
import numpy as np
import tushare as ts
from bs4 import BeautifulSoup
from database import stock_great_retail
from logger.logger import logger

token = '4158b7cdca566e01b4397a1f3328717043572b65cb5d7ef5bb04678e'
# token = '17d03acaa0df711791055c4dfe59020cc8698598d9f8e54ee87e7a3a'
# token = '897788a7beead59bd1e9077e47b2847e2abd3b4b00247369bba5183a'
# token = 'c9d091f48edf4085343f1ce6eadf51d2c948615681ded943c27a8a6b'
# token = '192cc8bf918fc206e143c5484b43bd668e69a84484d917387b658745'
ts.set_token(token)
pro = ts.pro_api()

def ifFirstHardenBoard(pro, code, start_date, end_date, name):
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    # print(df)
    if df.empty:
        return
    df['harden_price'] = round(df.pre_close * 1.2, 2)
    df['harden_board'] =  np.where(df.high == df.close, np.where(df.close == df.harden_price, 1, 0), 0)

    cur_data = df.loc[0]
    cur_flag = df.loc[0].harden_board == 1
    if cur_flag:
        if len(df[df.harden_board == 1]) == 1:
            logger.info(cur_data.ts_code)

            # 股东人数
            url = 'http://www.yidiancangwei.com/gudong/renshu_' + str(cur_data.ts_code).split('.')[0] + '.html'
            con = requests.get(url).text
            obj=BeautifulSoup(con,'html.parser')
            tbody = obj.find_all('tbody', class_='Tbody')[0]
            trs = tbody.find_all('tr')
            shareholdersFallingCount = 0
            for tr in trs:
                tds = tr.find_all('td')
                _date = tds[0].text.strip()
                _renShu = tds[1].text.strip()
                _renShuChange = tds[2].text.strip()
                if _renShuChange != '-':
                    if float(_renShuChange[:-1]) < 0:
                        shareholdersFallingCount += 1

            # 十大流通股东
            url_liutong = 'http://www.yidiancangwei.com/gudong/sdlt_' + code.split('.')[0] + '.html'
            con = requests.get(url_liutong).text
            obj=BeautifulSoup(con,'html.parser')
            div = obj.find_all('div', class_='TabBox')[0]
            trs = div.find_all('tr')
            sdluCount = 0
            for tr in trs:
                tds = tr.find_all('td')
                if tds:
                    name = tds[0].find_all('a')[0].get_text().strip()
                    addSubStore = tds[3].get_text().strip()
                    if len(name) <= 3 and (addSubStore == '新进' or addSubStore == '不变' or float(addSubStore[:-1]) > 0 ):
                        # print(name, addSubStore)
                        sdluCount += 1

            # 流通市值
            df = pro.daily_basic(ts_code=code, trade_date=cur_data.trade_date, fields='float_share')

            if shareholdersFallingCount > 0 and sdluCount >= 6 and df.values[0][0] < 1000000:
                stock_great_retail.insert_code(code, name, cur_data.trade_date, shareholdersFallingCount, sdluCount, df.values[0][0])
                print('写入成功')


if __name__ == "__main__":
    # 获取当前时间
    end_ts =int(time.time())
    start_ts = end_ts - 30*24*3600
    start_date = time.strftime('%Y%m%d', time.localtime(start_ts))
    end_date = time.strftime('%Y%m%d', time.localtime(end_ts))
    # start_date = '20200901'
    end_date = '20201009'

    is_open = pro.trade_cal(exchange='', start_date=end_date, end_date=end_date)
    is_open = is_open.values[0][2]
    if is_open:
        datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        a = 0
        for data in datas.values:
            # code = '688005.SH'
            code = data[0]
            name = data[2]
            print(code, name)
            if a and a % 500 == 0:
                print('开始睡眠1min...')
                time.sleep(60)
            ifFirstHardenBoard(pro, code, start_date, end_date, name)
            a += 1
            # break
        
