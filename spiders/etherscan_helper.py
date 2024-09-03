#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import re
import requests
from bs4 import BeautifulSoup
from spiders.const import HTTP_HEADER
from spiders.models import SpiderUrl
from django.conf import settings


SpiderName = "etherscan"
AccountCommet = "account"
TokenComment = "token"
LimitSize = str(25)
RegMatch = re.compile(r'[(](.*?)[)]')
BaseUrl = "https://cn.etherscan.com"
LabelCloadUrl = "https://cn.etherscan.com/labelcloud"
TokenValidCheckUrl = "https://cn.etherscan.com/address/%s"

# Etherscan 爬虫类
class EtherScanTagSipder:
    account_url_list = []
    token_url_list =[]
    headers = {}
    base_url: str
    label_cload_url: str
    token_valid_check_url: str

    def __init__(self):
        self.headers = {
            'user-agent': HTTP_HEADER,
            'cookie': settings.ACCOUNT_COOKIE
        }
        self.base_url = BaseUrl
        self.label_cload_url = LabelCloadUrl
        self.token_valid_check_url = TokenValidCheckUrl

    def bs4_request(self, request_url):
        label_response = requests.get(
            url=request_url,
            headers=self.headers,
            timeout=10
        )
        return BeautifulSoup(
            label_response.text,
            'html.parser'
        )

    # 获取Base url链接
    def get_url_list(self):
        label_cload = self.bs4_request(self.label_cload_url)
        link_node_list = label_cload.find_all('div', class_='col-md-4 col-lg-3 mb-3 secondary-container')
        for link_node in link_node_list:
            a_href = str(link_node.find('a')['href'])
            a_text = str(link_node.find('a').get_text())
            record_num = re.findall(RegMatch, a_text)[0]
            if a_href.startswith("/account"):
                account_url_dict = {
                    "url": self.base_url + a_href,
                    "records": record_num
                }
                self.account_url_list.append(account_url_dict)
            elif a_href.startswith("/tokens"):
                token_url_dict = {
                    "url": self.base_url + a_href,
                    "records": record_num
                }
                self.token_url_list.append(token_url_dict)
            else:
                logging.info("暂时不解析此类型的 URL 链接")

    # 数据入库
    def create_db_url(self):
        self.get_url_list()
        SpiderUrl.objects.create_spider_url(
            name=SpiderName,
            comment=AccountCommet,
            url_list=self.account_url_list,
            status='UnCrawl'
        )
        SpiderUrl.objects.create_spider_url(
            name=SpiderName,
            comment=TokenComment,
            url_list=self.token_url_list,
            status='UnCrawl'
        )

    # 获取 tab 页面链接
    def tab_pages(self, base_url):
        tab_content = self.bs4_request(base_url)
        try:
            tab_url_list = []
            card_header = tab_content.find("div", class_='card-header sticky-card-header d-flex justify-content-between p-0')
            tab_ul = card_header.find("ul", class_='nav nav-custom nav-borderless nav_tabs')
            li_list = tab_ul.find_all('li')
            for li in li_list:
                tab_name = li.find('a').attrs['name']
                val = li.find('a').attrs['val']
                records = re.findall(RegMatch, li.find('a').get_text())[0]
                li_item = {
                    "name": tab_name,
                    "val": val,
                    "records": records
                }
                tab_url_list.append(li_item)
            return tab_url_list
        except:
            logging.info("该页面没有 TagContent 数据, 链接为 %s", base_url)
            return None

    # 获取 Account 详情信息
    def get_accounts_detail(self, url):
        account_list = []
        accout_detail = self.bs4_request(url)
        try:
            tbody_list = accout_detail.find_all("tbody")
            for tbody in tbody_list:
                tr_list = []
                tr_old_list = tbody.find_all('tr', class_='odd')
                for tr_old in tr_old_list:
                    tr_list.append(tr_old)
                tr_even_list = tbody.find_all('tr', class_='even')
                for tr_even in tr_even_list:
                    tr_list.append(tr_even)
                for tr_item in tr_list:
                    td_list = tr_item.find_all('td')
                    address = td_list[0].find("a").get_text()
                    account_name = td_list[1].get_text()
                    print(account_name, address)
                    account_dict = {
                        "account_name": account_name,
                        "address": address
                    }
                    account_list.append(account_dict)
        except:
            logging.info("该Account请求界面没有数据, 链接为 %s", url)
        return account_list

    # 获取 Token 详情信息
    def get_token_detail(self, url):
        token_list = []
        token_detail = self.bs4_request(url)
        try:
            tbody_list = token_detail.find_all("tbody")
            for tbody in tbody_list:
                tr_list = []
                tr_old_list = tbody.find_all('tr', class_='odd')
                for tr_old in tr_old_list:
                    tr_list.append(tr_old)
                tr_even_list = tbody.find_all('tr', class_='even')
                for tr_even in tr_even_list:
                    tr_list.append(tr_even)
                for tr_item in tr_list:
                    td_list = tr_item.find_all('td')
                    token_full_name = td_list[2].find("a").get_text()
                    token_name = re.findall(RegMatch, token_full_name)
                    address = td_list[1].find("div", class_="d-block").find("a").get_text()
                    account_dict = {
                        "token_name": token_name[0],
                        "address": address
                    }
                    token_list.append(account_dict)
        except:
            logging.info("该Token请求界面没有数据, 链接为 %s", url)
        return token_list

    def check_token_valid(self, address):
        token_detail = self.bs4_request(self.token_valid_check_url % address)

        img_list = token_detail.find_all('img', src="/images/main/empty-token.png", width="20", style="margin-left: -5px")
        if img_list:
            return False
        return True
