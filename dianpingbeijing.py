import requests
import random
import re
import os
import json
import pymongo
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver

class Beijing():
    def __init__(self,url,path):
        self.url = url
        self.path = path

    def get_and_analysis(self, url, headers):
        try:
            client = pymongo.MongoClient('123.56.221.97', 27017)
            mydb = client["dazhong"]
            beijing_col = mydb["beijing"]
            response = requests.get(url, headers=headers)
            if response.content:
                datas = json.loads(response.text)
                print(datas.keys())
                for data in datas['shopBeans']:
                    # print(data)
                    print(data['shopName'])
                    query_exists = beijing_col.find({"shopName": data['shopName']})
                    print(query_exists)
                    if not query_exists:
                        # print('需要插入')
                        beijing_col.insert_one(data)
                    else:
                        print('数据已添加')
            else:
                print('can not open url')
        except Exception as e:
            print ('Error', e)
            # print('Unkonwn Error')      

def getAgent():
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    print (user_agent)
    return headers

if __name__ == '__main__':
    url = 'http://www.dianping.com/mylist/ajax/shoprank?rankId=d5036cf54fcb57e9dceb9fefe3917fff71862f838d1255ea693b953b1d49c7c0'
    path = os.getcwd()
    beijing = Beijing(url, path)
    beijing.get_and_analysis(url, getAgent())
    