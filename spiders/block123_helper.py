	#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from common.models import EntityInfo
from spiders.spider_client import BsSpiderClient
from typing import List


BaseUrl = "https://www.block123.com"


class Block_124_BaseUrl(BsSpiderClient):
    entity_url_list: List = []
    base_url: str = BaseUrl

    def __init__(self, connect: str):
        super(BsSpiderClient, self).__init__(connect=connect)

    def ci_spider_urls(self):
        bock123_url = self.bs4_request()
        main_div_item_list = bock123_url.\
            find('div', class_='main-content-container').\
            find_all('div', class_='item')
        for div_item in main_div_item_list:
            url_href = self.base_url + div_item.find('a')['href']
            self.entity_url_list.append(url_href)
        print("create success", self.entity_url_list)

    def ci_spider_info(self):
        for entity_url in self.entity_url_list:
            bock123_info = self.bs4_request(req_url=entity_url)
            name = bock123_info.\
                find('div', class_='category-nav-short-info-wrapper pure-g').\
                find('div', class_='right-item').find('div', class_='name-wrapper').\
                find('h1').get_text()
            website = bock123_info.\
                find('div', class_='web-site-container').\
                find('div', class_='web-site').find('a').get_text()
            p_list = bock123_info.find('div', class_='desc-content item-content').\
                find_all('p')
            introduce_str = ""
            for p in p_list:
                introduce_str = introduce_str + p.get_text()
            EntityInfo.objects.update_or_create(
                name=name,
                introduce=introduce_str,
                website=website,
                tune_up_index=1,
            )
            print("create", name, introduce_str, website, "success")
