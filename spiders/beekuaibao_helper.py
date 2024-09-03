#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.models import EntityInfo
from spiders.spider_client import BsSpiderClient


class BeekuaibaoSpider(BsSpiderClient):
    def __init__(self, connect: str):
        super(BsSpiderClient, self).__init__(connect=connect)

    def bkb_spider_info(self):
        beekuaibao_info = self.bs4_request()
        artcle = beekuaibao_info.find('article', class_='content')
        ul_list = artcle.find_all('ul', class_='list-paddingleft-2', style='list-style-type: square;')
        for ul in ul_list:
            li_list = ul.find_all('li')
            for li in li_list:
                entity_pr_i = li.find('p').get_text()
                if "：" in entity_pr_i:
                    split_str_lst = entity_pr_i.split("：")
                elif ":" in entity_pr_i:
                    split_str_lst = entity_pr_i.split(":")
                entity_name = split_str_lst[0]
                entity_introduce = split_str_lst[1]
                entity_info = EntityInfo.objects.filter(name=entity_name).order_by("-id").first()
                if entity_info is None:
                    EntityInfo.objects.update_or_create(
                        name=entity_name,
                        introduce=entity_introduce,
                        tune_up_index=1,
                    )
                else:
                    print(entity_name, "已经存在数据库")
