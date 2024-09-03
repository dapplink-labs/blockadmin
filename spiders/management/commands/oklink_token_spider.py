#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from common.models import DataCahe
from spiders.rest_client import RestClient
from spiders.const import HTTP_HEADER, BLOCKDIR_OFFSET
from spiders.helpers import TagDataHelper


RecordLimit = 100
Token = "1617873685534"
ApiKey = "LWIzMWUtNDU0Ny05Mjk5LWI2ZDA3Yjc2MzFhYmEyYzkwM2NjfDI3Mjg5ODQ3OTY2NDU0MjE="


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_url = "https://www.oklink.com/api/explorer/v1/eth/tokens"
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
        params = {
            "t": Token,
            "limit": RecordLimit,
            "offset": offset
        }
        header = {"user-agent": HTTP_HEADER, "x-api-key": ApiKey}
        result = rc.api_get(url=request_url, params=params, headers=header)
        logging.info(result)
        ret_result = result.get("data", None)
        logging.info(ret_result)
        # for data in data_list:
        #     address_list = []
        #     address_list.append(data.get("tokenContractAddress", ""))
        #     symbol = data.get("symbol", "")
        #     TagDataHelper(
        #         asset="ETH",
        #         tag=symbol,
        #         comment="blockchair",
        #         cate="contract",
        #         address_list=address_list,
        #         threat_level=1
        #     ).data_2db()
        # offset_new = offset + RecordLimit
        # DataCahe.objects.filter(key=BLOCKDIR_OFFSET).update(values=offset_new)



