#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from common.models import AddressTag, Address
from common.models import DataCahe
from spiders.rest_client import RestClient
from spiders.const import HTTP_HEADER, BTC_COM_PAGE_KEY


PageSize = 25


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_url = "https://explorer-web.api.btc.com/contract-api/v1/verified-contracts"
        rc = RestClient()
        params = {"pageNumber": 1, "pageSize": PageSize}
        header = {"user-agent": HTTP_HEADER}
        result = rc.api_get(url=request_url, params=params, headers=header)
        data = result.get("data", None)
        if data is not None:
            records = data.get("count", 0)
            total_page_number = records / PageSize
            base_page = DataCahe.objects.filter(key=BTC_COM_PAGE_KEY).first()
            base_page_index = 0
            if base_page is not None:
                base_page_index = int(base_page.values)
            else:
                DataCahe.objects.create(
                    key=BTC_COM_PAGE_KEY,
                    values=str(base_page_index),
                )
            for index_p in range(int(total_page_number)):
                page_number = base_page_index + index_p
                params = {"pageNumber": page_number, "pageSize": PageSize}
                header = {"user-agent": HTTP_HEADER}
                result = rc.api_get(url=request_url, params=params, headers=header)
                data = result.get("data", None)
                if data is not None:
                    items_list = data.get("items", [])
                    for item in items_list:
                        address = item.get("address", "")
                        name = item.get("name", "")
                        bt_data = AddressTag.objects.filter(tag=name).first()
                        if bt_data is None:
                            create_tagd = AddressTag.objects.create(
                                tag=name,
                                threat_level=1,
                                comment="btc.eth.com",
                                cate="contract"
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
                            t_addr = Address.objects.filter(address=address).first()
                            if t_addr is None:
                                Address.objects.create(
                                    tag=bt_data,
                                    asset="ETH",
                                    address=address,
                                    is_commit="commit",
                                    is_checked="checked"
                                )
                                logging.info("create address", address, "success")
                DataCahe.objects.filter(key=BTC_COM_PAGE_KEY).update(values=str(page_number))