#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from spiders.const import HTTP_HEADER


class BsSpiderClient:
    connect: str
    headers: Dict

    def __init__(self, connect: str, headers: Dict = None):
        self.connect = connect
        self.headers = headers

    def spider_header(self):
        if self.headers is None:
            return {
                'user-agent': HTTP_HEADER,
            }
        else:
            return self.headers

    def bs4_request(self, req_url: str = ""):
        url = self.connect if req_url in ["", None] else req_url
        label_response = requests.get(
            url=url,
            headers=self.spider_header()
        )
        return BeautifulSoup(
            label_response.text,
            'html.parser'
        )
