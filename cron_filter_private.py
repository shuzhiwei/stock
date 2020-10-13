import web, requests, time
from bs4 import BeautifulSoup
from database import stock_private, stock_private1

def filter_private():
    private_names = stock_private.get_all_private_names()
    base_url = 'http://www.yidiancangwei.com/searchResult.php?ID=1&Val='
    for private_name in private_names:
        if ', ' in private_name:
            names = private_name.split(', ')
            for name in names:
                print('name: ' + name)
                full_url = base_url + name
                requestUrl(full_url, name)
        else:
            print('private_name: ' + private_name)
            full_url = base_url + private_name
            requestUrl(full_url, private_name)

def requestUrl(url, private_name):
    # time.sleep(1)
    con = requests.get(url).text
    obj = BeautifulSoup(con, 'html.parser')
    trs = obj.find_all('tr')

    duplicate_stock_names = []
    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            stock_name = tds[1].get_text().strip()
            duplicate_stock_names.append(stock_name)

    if len(duplicate_stock_names) == 1 or (len(duplicate_stock_names) > 1 \
                and len(set(duplicate_stock_names)) == 1):
                # and len(set(duplicate_stock_names)) != len(duplicate_stock_names)):
        update_time_list = []
        add_sub_store_list = []
        for tr in trs:
            tds = tr.find_all('td')
            if tds:
                stock_name = tds[1].get_text().strip()
                add_sub_store = str(tds[3].get_text().strip())
                update_time = str(tds[5].get_text().strip())
                add_sub_store_list.append(add_sub_store)
                update_time_list.append(update_time)

        _stock_name = trs[1].find_all('td')[1].get_text().strip()
        _add_sub_store = ', '.join('%s' %id for id in add_sub_store_list)
        _update_time = ', '.join(update_time_list)

        if stock_private1.existData(private_name):
            stock_private1.updateData(private_name, _stock_name, _add_sub_store, _update_time)
            print('更新成功')
        else:
            stock_private1.insert_data(private_name, _stock_name, _add_sub_store, _update_time)
            print('写入成功')


if __name__ == "__main__":
    filter_private()

                


