import web, json, os
import configparser
import traceback
import jwt, time, re
import casbin, threading
from collections import OrderedDict
from logger.logger import logger
from database import stock_great_retail, stock_private, stock_private1, stock_kdj
from tools.sync_policy import syncPolicy

urls = (
    '/view', 'View',
    '/viewPrivate', 'ViewPrivate',
    '/searchPrivate', 'SearchPrivate',
    '/viewPrivate1', 'ViewPrivate1',
    '/searchPrivate1', 'SearchPrivate1',
    '/viewPrivate1Favorites', 'ViewPrivate1Favorites',
    '/updatePrivate1Favorites', 'UpdatePrivate1Favorites',
    '/viewKdj', 'ViewKdj',
)

app = web.application(urls, globals())
parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/confs/config.ini'
config.read(full_path)
dom = config.get('acs', 'domain')
obj = 'stock'

class ViewKdj:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            pageSize = web.input().pageSize
            pageNo = web.input().pageNo
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
                posts = stock_kdj.get_all_datas_on_page(pageSize, pageNo)
                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['code'] = i.code
                        d_dict['code_name'] = i.code_name
                        d_dict['update_date'] = i.update_date
                        d_dict['if_gold_cross'] = i.if_gold_cross
                        d_dict['shareholder_falling_count'] = i.shareholder_falling_count
                        d_dict['sdlu_great_retail_count'] = i.sdlu_great_retail_count
                        d_dict['float_share'] = i.float_share
                        d_list.append(d_dict)
                    totalCount = stock_kdj.get_posts_count()
                    totalPage = int(totalCount / int(pageSize))
                    totalPage_yu = totalCount % int(pageSize)
                    if totalPage_yu:
                        totalPage = totalPage + 1
                    return json.dumps({'status': 'success', 'code': 200, 'totalCount': totalCount, 'totalPage': totalPage, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})


class SearchPrivate1:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            stock = web.input().stock
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
                posts = stock_private1.search_from_name(stock)

                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['private_name'] = i.private_name
                        d_dict['code_name'] = i.code_name
                        d_dict['add_sub_store'] = i.add_sub_store
                        d_dict['update_date'] = i.update_date
                        d_dict['type'] = i.type
                        d_list.append(d_dict)
                    return json.dumps({'status': 'success', 'code': 200, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class SearchPrivate:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            stock = web.input().stock
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
                if re.search(r'\d', stock):
                    if 'S' in stock:
                        posts = stock_private.search(stock)
                    else:
                        _code = stock + '.SZ'
                        posts = stock_private.search(_code)
                        if not posts:
                            _code = stock + '.SH'
                            posts = stock_private.search(_code)
                else:
                    posts = stock_private.search_from_name(stock)

                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['code'] = i.code
                        d_dict['update_date'] = i.update_date
                        d_dict['private_name'] = i.private_name
                        d_dict['add_sub_store'] = i.add_sub_store
                        d_dict['code_name'] = i.code_name
                        d_list.append(d_dict)
                    return json.dumps({'status': 'success', 'code': 200, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class ViewPrivate1Favorites:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            pageSize = web.input().pageSize
            pageNo = web.input().pageNo
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
                posts = stock_private1.get_all_datas_on_page_on_favorites(pageSize, pageNo)
                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['private_name'] = i.private_name
                        d_dict['code_name'] = i.code_name
                        d_dict['add_sub_store'] = i.add_sub_store
                        d_dict['update_date'] = i.update_date
                        d_dict['type'] = i.type
                        d_list.append(d_dict)
                    totalCount = stock_private1.get_posts_count_on_favorites()
                    totalPage = int(totalCount / int(pageSize))
                    totalPage_yu = totalCount % int(pageSize)
                    if totalPage_yu:
                        totalPage = totalPage + 1
                    return json.dumps({'status': 'success', 'code': 200, 'totalCount': totalCount, 'totalPage': totalPage, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class UpdatePrivate1Favorites:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            private_name = web.input().private_name
            _type = web.input().type
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
                stock_private1.update_favorites(private_name, _type)
                return json.dumps({'status': 'success', 'code': 200})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class ViewPrivate1:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            pageSize = web.input().pageSize
            pageNo = web.input().pageNo
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
                posts = stock_private1.get_all_datas_on_page(pageSize, pageNo)
                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['private_name'] = i.private_name
                        d_dict['code_name'] = i.code_name
                        d_dict['add_sub_store'] = i.add_sub_store
                        d_dict['update_date'] = i.update_date
                        d_list.append(d_dict)
                    totalCount = stock_private1.get_posts_count()
                    totalPage = int(totalCount / int(pageSize))
                    totalPage_yu = totalCount % int(pageSize)
                    if totalPage_yu:
                        totalPage = totalPage + 1
                    return json.dumps({'status': 'success', 'code': 200, 'totalCount': totalCount, 'totalPage': totalPage, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class ViewPrivate:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            pageSize = web.input().pageSize
            pageNo = web.input().pageNo
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
                posts = stock_private.get_all_datas_on_page(pageSize, pageNo)
                if posts:
                    d_list = []
                    for i in posts:
                        d_dict = OrderedDict()
                        d_dict['code'] = i.code
                        d_dict['update_date'] = i.update_date
                        d_dict['private_name'] = i.private_name
                        d_dict['add_sub_store'] = i.add_sub_store
                        d_dict['code_name'] = i.code_name
                        d_list.append(d_dict)
                    totalCount = stock_private.get_posts_count()
                    totalPage = int(totalCount / int(pageSize))
                    totalPage_yu = totalCount % int(pageSize)
                    if totalPage_yu:
                        totalPage = totalPage + 1
                    return json.dumps({'status': 'success', 'code': 200, 'totalCount': totalCount, 'totalPage': totalPage, 'data': d_list})
                else:
                    return json.dumps({'status': 'fail', 'code': 15})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class View:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            pageSize = web.input().pageSize
            pageNo = web.input().pageNo
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
                posts = stock_great_retail.get_all_datas_on_page(pageSize, pageNo)
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
                    totalCount = stock_great_retail.get_posts_count()
                    totalPage = int(totalCount / int(pageSize))
                    totalPage_yu = totalCount % int(pageSize)
                    if totalPage_yu:
                        totalPage = totalPage + 1
                    return json.dumps({'status': 'success', 'code': 200, 'totalCount': totalCount, 'totalPage': totalPage, 'data': d_list})
                    # return json.dumps({'status': 'success', 'code': 200, 'data': d_list})
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

    logger.debug('start run ...')
    app.run()