import os
import re
import requests
import sys
import string
import pymongo
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import html

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy():
    requests.get("https://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    
def save_info(list_info):
    print('save信息开始')
    client = pymongo.MongoClient('123.56.221.97', 27017)
    mydb = client['dazhong']
    details_col = mydb['details']
    details_col.insert_many(list_info)
    print('save data success')

def create_dict_collection(shopname, names, comments):
    print('嗲用create_dict_collection')
    #for name in names:
    #    dict_info = dict(shop_name=shopname, user_name = name.text.strip(), flavour = ranks[])
    list_names = to_list(names)
    print('name转换成功')
    list_coments = to_list(comments)
    print('comments转换成功')
    list_info_all = []
    for i in len(list_names):   # 也不能用0,15有的不足15  range(0,15)
        #for star in ranks_result:    因为有的显示的不是一样的东西服务口味技师环境
        #    list_rank = to_list(star)
        #    print(list_rank)
        print('create dict开始')
        dict_one = {'shopname':shopname, 'user_name': list_names[i], 
                    #'fla':list_rank[0], 'env':list_rank[1],
                    #'ser':list_rank[2], 'food':list_rank[3],
                    #'rank': ranks_result[i],
                    'comment':list_coments[i].get_text().replace("收起评论","").replace('\n', '').replace('\t', '').strip()}
        print(dict_one)
        list_info_all.append(dict_one)
    print(list_info_all)
    save_info(list_info_all)
    
def to_list(targets):
    list = []
    for target in targets:
        list.append(target)
    return list

if __name__ == '__main__':
    url = 'http://www.dianping.com/shop/26940351/review_all'
    # http://www.dianping.com/shop/3451996/review_all    http://www.dianping.com/shop/2091475/review_all  https://www.dianping.com/shop/5227397/review_all
    # https://www.dianping.com/shop/67746735/review_all
    # http://www.dianping.com/shop/27249316/review_all
    user_agent = UserAgent().random
    print(user_agent)
    proxy  = get_proxy().get("proxy")
    print(proxy)
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
    try:
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        # f = open("text.log", 'a', encoding='utf-8')
        # f.write(soup)
        # sys.stdout = f   # 111.34.233.87
        # sys.stderr = f
        # print(soup.select('.dper-info a'))
        # print (soup.find_all("div", class_="dper-info"))
        shop_name = soup.find_all("h1", class_="shop-name")
        print(shop_name)
        shopname = shop_name[0].text.strip()
        if not shopname:
            print('IP被封禁')
            sys.exit()
            sys.exit(0)
            sys.exit(1)
        print(shop_name[0].text.strip())
        names = soup.find_all("div", class_="dper-info")  #name.text.strip()
        namelist = []
        for name in names:
            print("----", name.text.strip()) 
            namelist.append(name.text.strip())
        #print(soup) 
        review_ranks = soup.find_all("div", class_="review-rank")        #next_sibling
        if review_ranks:
            list_result = []
            for i in review_ranks:
                #print("---------",i.get_text().replace(" ","")) # split('-')
                #ranks = i.get_text().replace(" ","").split(':')
                rank = i.get_text().replace(" ","")
                #result = re.findall(r'\d+\.?\d*', rank)
                print(rank)
                list_result.append(rank.replace("\n", ""))             
                #print(pattern1.findall(pattern1))
            print(list_result)
        else:
            print("获取为空")
        
        comments = soup.find_all("div", class_="review-words")
        create_dict_collection(shopname, namelist, comments)   # list_result,
        #for comment in comments:
        #    print("----", comment.get_text().replace("收起评论","")) 
        # print(soup)       
    except Exception as e:
        print("Error", e)