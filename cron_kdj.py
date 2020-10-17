import time, requests
import traceback
import pandas as pd
import numpy as np
import tushare as ts
from bs4 import BeautifulSoup
from database import stock_kdj
from logger.logger import logger
from tools import sample_mail

token = '4158b7cdca566e01b4397a1f3328717043572b65cb5d7ef5bb04678e'
# token = '17d03acaa0df711791055c4dfe59020cc8698598d9f8e54ee87e7a3a'
# token = '897788a7beead59bd1e9077e47b2847e2abd3b4b00247369bba5183a'
# token = 'c9d091f48edf4085343f1ce6eadf51d2c948615681ded943c27a8a6b'
# token = '192cc8bf918fc206e143c5484b43bd668e69a84484d917387b658745'
ts.set_token(token)
pro = ts.pro_api()

def cal_kdj(pro, code, start_date, end_date, code_name):
    try:
        df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
        df.sort_values('trade_date', inplace=True)
        
        low_list = df['low'].rolling(9, min_periods=9).min()
        low_list.fillna(value = df['low'].expanding().min(), inplace = True)
        high_list = df['high'].rolling(9, min_periods=9).max()
        high_list.fillna(value = df['high'].expanding().max(), inplace = True)
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100

        df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
        df['D'] = df['K'].ewm(com=2).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']

        df['KDJ_金叉死叉'] = ''
        kdj_position=df['K']>df['D']
        df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
        df.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'

        if df.empty:
            return

        if '金叉' == df.iloc[-1]['KDJ_金叉死叉']:

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
                    if len(name) <= 3 and ((addSubStore == '新进' or addSubStore == '不变') or (addSubStore != '限售股流通' and float(addSubStore[:-1]) > 0 )):
                        sdluCount += 1

            # 股东人数
            url = 'http://www.yidiancangwei.com/gudong/renshu_' + str(code).split('.')[0] + '.html'
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
            
            # shareholdersFalling = 0
            # if tmp_list:
            #     renShuChange = float(tmp_list[0][1]) - float(tmp_list[-1][1])
            #     renShuChangeRate = 0

            #     for b in tmp_list:
            #         logger.debug(b)
            #         if b[2] and b[2] != '-':
            #             renShuChangeRate += float(b[2][:-1])

            #     if renShuChange < 0 and renShuChangeRate < 0:
            #         shareholdersFalling = 1

            shareholdersFallingCount = 0
            if tmp_list:
                for tmp in tmp_list:
                    if tmp[2] != '-' and float(tmp[2][:-1]) < 0:
                        shareholdersFallingCount += 1

            # 流通市值
            df1 = pro.daily_basic(ts_code=code, trade_date=df.iloc[-1]['trade_date'], fields='float_share')

            # global great_stock_count
            # if shareholdersFallingCount and sdluCount >=6 and float(str(df.values[0][0])) < 1000000:
            #     great_stock_count += 1 

            stock_kdj.insert_code(code, code_name, df.iloc[-1]['trade_date'], 1, shareholdersFallingCount, sdluCount, float(str(df1.values[0][0])))
        # elif '死叉' == df.iloc[-1]['KDJ_金叉死叉']:
        #     stock_kdj.insert_code(code, code_name, df.iloc[-1]['trade_date'], 2)

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

def cron():
    # 获取当前时间
    end_ts =int(time.time())
    start_ts = end_ts - 60*24*3600
    start_date = time.strftime('%Y%m%d', time.localtime(start_ts))
    end_date = time.strftime('%Y%m%d', time.localtime(end_ts))
    # start_date = '20200901'
    end_date = '20201016'
    print(start_date, end_date)

    is_open = pro.trade_cal(exchange='', start_date=end_date, end_date=end_date)
    is_open = is_open.values[0][2]
    if is_open:
        datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
        a = 0
        for data in datas.values:
            # code = '300050.SZ'
            code = data[0]
            code_name = data[1]
            print(code, code_name)
            if a and a % 500 == 0:
                print('开始睡眠1min...')
                time.sleep(60)
            cal_kdj(pro, code, start_date, end_date, code_name)
            a += 1
            # break


if __name__ == "__main__":
    cron()

        
