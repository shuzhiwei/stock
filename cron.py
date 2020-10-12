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

def ifFirstHardenBoard(pro, code, start_date, end_date, code_name):
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

            # 十大流通股东
            url_liutong = 'http://www.yidiancangwei.com/gudong/sdlt_' + code.split('.')[0] + '.html'
            con = requests.get(url_liutong).text
            obj=BeautifulSoup(con,'html.parser')
            # 获取最新日期
            try:
                d = obj.find_all('div', class_='RankingListDate')[0]
                d = d.find_all('a')[0].get_text()
                if d < '2020-01-01':
                    return
            except Exception:
                return

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

            # 股东人数
            url = 'http://www.yidiancangwei.com/gudong/renshu_' + str(cur_data.ts_code).split('.')[0] + '.html'
            con = requests.get(url).text
            obj=BeautifulSoup(con,'html.parser')
            tbody = obj.find_all('tbody', class_='Tbody')[0]
            trs = tbody.find_all('tr')
            tmp_list = []
            for tr in trs:
                tds = tr.find_all('td')
                _date = tds[0].text.strip()
                if _date < d:
                    break
                _renShu = tds[1].text.strip()
                _renShuChange = tds[2].text.strip()
                tmp_list.append((_date, _renShu, _renShuChange))
            
            shareholdersFalling = 0
            if tmp_list:
                renShuChange = float(tmp_list[0][1]) - float(tmp_list[-1][1])
                renShuChangeRate = 0

                for b in tmp_list:
                    print(b)
                    if b[2] and b[2] != '-':
                        renShuChangeRate += float(b[2][:-1])

                if renShuChange < 0 and renShuChangeRate < 0:
                    shareholdersFalling = 1

            # 流通市值
            df = pro.daily_basic(ts_code=code, trade_date=cur_data.trade_date, fields='float_share')

            if shareholdersFalling == 1 and sdluCount >= 6 and df.values[0][0] < 1000000:
                stock_great_retail.insert_code(code, code_name, cur_data.trade_date, shareholdersFalling, sdluCount, df.values[0][0])
                print('写入成功')


if __name__ == "__main__":
    # 获取当前时间
    end_ts =int(time.time())
    start_ts = end_ts - 30*24*3600
    start_date = time.strftime('%Y%m%d', time.localtime(start_ts))
    end_date = time.strftime('%Y%m%d', time.localtime(end_ts))
    # start_date = '20200901'
    # end_date = '20201009'

    is_open = pro.trade_cal(exchange='', start_date=end_date, end_date=end_date)
    is_open = is_open.values[0][2]
    if is_open:
        logger.debug('start run...')
        datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
        a = 0
        for data in datas.values:
            # code = '688005.SH'
            code = data[0]
            code_name = data[1]
            if a and a % 500 == 0:
                print('开始睡眠1min...')
                time.sleep(60)
            ifFirstHardenBoard(pro, code, start_date, end_date, code_name)
            a += 1
            # break
        
