#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from common.models import DataCahe
from spiders.rest_client import RestClient
from spiders.const import HTTP_HEADER, BLOCKDIR_OFFSET
from spiders.helpers import TagDataHelper


RecordLimit = 100


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_url = "https://api.blockchair.com/ethereum/erc-20/tokens"
        rc = RestClient()
        data_cc = DataCahe.objects.filter(key=BLOCKDIR_OFFSET).first()
        offset = 0
        if data_cc is not None:
            offset = int(data_cc.values)
        else:
            DataCahe.objects.create(
                key=BLOCKDIR_OFFSET,
                values=offset
            )
        params = {"limit": RecordLimit, "offset": offset}
        header = {"user-agent": HTTP_HEADER}
        result = rc.api_get(url=request_url, params=params, headers=header)
        data_list = result.get("data", None)
        for data in data_list:
            address_list = []
            address_list.append(data.get("address", ""))
            symbol = data.get("symbol", "")
            TagDataHelper(
                asset="ETH",
                tag=symbol,
                comment="blockchair",
                cate="contract",
                address_list=address_list,
                threat_level=1
            ).data_2db()
        offset_new = offset + RecordLimit
        DataCahe.objects.filter(key=BLOCKDIR_OFFSET).update(values=offset_new)



