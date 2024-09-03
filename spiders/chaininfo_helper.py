	#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spiders.spider_client import BsSpiderClient


class ChainInfoSpider(BsSpiderClient):
    def __init__(self, connect: str):
        super(BsSpiderClient, self).__init__(connect=connect)

    def chain_info_spider(self):
        chain_info = self.bs4_request()
        print(chain_info)