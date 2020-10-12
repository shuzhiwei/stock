import web, json, os
import configparser
import traceback
import jwt, time
import casbin, threading
from collections import OrderedDict
from logger.logger import logger
from database import stock_great_retail
from tools.sync_policy import syncPolicy
from cron import cron

urls = (
    '/view', 'View',
)

app = web.application(urls, globals())
parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/confs/config.ini'
config.read(full_path)
dom = config.get('acs', 'domain')
obj = 'stock'

class View:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            # date_data = web.input().date_data
            # date_ts = int(time.time())
            # date_data = time.strftime('%Y%m%d', time.localtime(date_ts))
    
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})
                
            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'read'
            if e.enforce(sub, dom, obj, act):
                posts = stock_great_retail.get_all_datas()
                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['code'] = i.code
                        d_dict['update_date'] = i.update_date
                        d_dict['shareholder_falling_count'] = i.shareholder_falling_count
                        d_dict['sdlu_great_retail_count'] = i.sdlu_great_retail_count
                        d_dict['float_share'] = i.float_share
                        d_dict['name'] = i.name
                        d_list.append(d_dict)
                    return json.dumps({'status': 'success', 'code': 200, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
                # while True:
                #     posts = stock_great_retail.get_datas(date_data)
                #     if posts:
                #         d_list = []
                #         for i in posts:
                #             d_dict = OrderedDict()
                #             d_dict['code'] = i.code
                #             d_dict['update_date'] = i.update_date
                #             d_dict['shareholder_falling_count'] = i.shareholder_falling_count
                #             d_dict['sdlu_great_retail_count'] = i.sdlu_great_retail_count
                #             d_dict['float_share'] = i.float_share
                #             d_list.append(d_dict)
                #         return json.dumps({'status': 'success', 'code': 200, 'data': d_list})
                #     else:
                #         date_ts = date_ts - 24*3600
                #         date_data = time.strftime('%Y%m%d', time.localtime(date_ts))
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})


if __name__ == "__main__":
    t1 = threading.Thread(target=syncPolicy, args=(dom,))
    logger.debug('start thread sync policy ...')
    t1.start()

    t2 = threading.Thread(target=cron)
    logger.debug('start thread cron ...')
    t2.start()
    
    logger.debug('start run ...')
    app.run()