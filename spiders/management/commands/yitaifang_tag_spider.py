#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from common.models import AddressTag, Address
from spiders.rest_client import RestClient
from spiders.const import HTTP_HEADER, YITAIFANG_TAG_PAGE


# token 爬虫
def token_spider(request_url):
    rc = RestClient()
    params = {"page": 1, "limit": 30}
    header = {"user-agent": HTTP_HEADER}
    result = rc.api_get(url=request_url, params=params, headers=header)
    data = result.get("data", None)
    total_page = data.get("totalPage", 0)
    for index_p in range(int(total_page)):
        params_p = {"page": index_p, "limit": 30}
        result = rc.api_get(url=request_url, params=params_p, headers=header)
        data = result.get("data", None)
        if data is not None:
            data_list = data.get("result", 0)
            for item in data_list:
                name = item.get("name", "")
                address = item.get("address", "")
                bt_data = AddressTag.objects.filter(tag=name).first()
                if bt_data is None:
                    create_tagd = AddressTag.objects.create(
                        tag=name,
                        threat_level=1,
                        cate="contract",
                        comment="yitaifang",
                    )
                    Address.objects.create(
                        tag=create_tagd,
                        asset="ETH",
                        address=address,
                        is_commit="commit",
                        is_checked="checked"
                    )
                    print("create", name, "success")
                else:
                    continue


# account 爬虫
def account_spider(request_url):
    rc = RestClient()
    params = {"page": 1, "limit": 30}
    header = {"user-agent": HTTP_HEADER}
    result = rc.api_get(url=request_url, params=params, headers=header)
    data = result.get("data", None)
    total_page = data.get("totalPage", 0)
    for index_p in range(int(total_page)):
        params_p = {"page": index_p, "limit": 30}
        result = rc.api_get(url=request_url, params=params_p, headers=header)
        data = result.get("data", None)
        if data is not None:
            data_list = data.get("result", 0)
            for item in data_list:
                comment = item.get("comment", "")
                if comment != "":
                    address = item.get("address", "")
                    bt_data = AddressTag.objects.filter(tag=comment).first()
                    if bt_data is None:
                        create_tagd = AddressTag.objects.create(
                            tag=comment,
                            threat_level=1,
                            cate="contract",
                            comment="yitaifang",
                        )
                        Address.objects.create(
                            tag=create_tagd,
                            asset="ETH",
                            address=address,
                            is_commit="commit",
                            is_checked="checked"
                        )
                        print("create", comment, "success")
                    else:
                        continue


class Command(BaseCommand):
    def handle(self, *args, **options):
        account_url = "https://api.yitaifang.com/index/accounts/"
        token_url = "https://api.yitaifang.com/index/tokens/"
        account_spider(account_url)
        token_spider(token_url)

