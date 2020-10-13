import time, requests
import traceback
import pandas as pd
import numpy as np
import tushare as ts
from bs4 import BeautifulSoup
from logger.logger import logger
from database import stock_private

token = '4158b7cdca566e01b4397a1f3328717043572b65cb5d7ef5bb04678e'
# token = '17d03acaa0df711791055c4dfe59020cc8698598d9f8e54ee87e7a3a'
# token = '897788a7beead59bd1e9077e47b2847e2abd3b4b00247369bba5183a'
# token = 'c9d091f48edf4085343f1ce6eadf51d2c948615681ded943c27a8a6b'
# token = '192cc8bf918fc206e143c5484b43bd668e69a84484d917387b658745'
ts.set_token(token)
pro = ts.pro_api()

def ifPrivate(code, code_name):
    try:
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
        private_list = []
        for tr in trs:
            tds = tr.find_all('td')
            if tds:
                private_name = tds[0].find_all('a')[0].get_text().strip()
                addSubStore = tds[3].get_text().strip()
                if '私募' in private_name:
                    private_list.append((private_name, addSubStore))

        if private_list:
            tmp_names = []
            tmp_addSubStores = []
            for private_s in private_list:
                tmp_names.append(private_s[0])
                tmp_addSubStores.append(private_s[1])

            if len(tmp_names) > 1:
                tmp_names = ', '.join(tmp_names)
            else:
                tmp_names = tmp_names[0]

            if len(tmp_addSubStores) > 1:
                tmp_addSubStores = ', '.join(tmp_addSubStores)
            else:
                tmp_addSubStores = tmp_addSubStores[0]

            stock_private.insert_code(code, code_name, d, tmp_names, tmp_addSubStores)
            logger.debug(code + ", " + code_name + ", " + d + ", " + tmp_names + ", " + tmp_addSubStores)
            logger.debug('write success')

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

def cron():
        datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
        a = 0
        for data in datas.values:
            # code = '000010.SH'
            code = data[0]
            code_name = data[1]
            logger.debug(code + ": " + code_name)
            if a and a % 100 == 0:
                print('开始睡眠1min...')
                time.sleep(60)
            ifPrivate(code, code_name)
            a += 1
            # break


if __name__ == "__main__":
    cron()
        
