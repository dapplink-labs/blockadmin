#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from common.models import AddressTag, Address
from spiders.rest_client import RestClient
from spiders.const import HTTP_HEADER


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_url = "https://api2.ethplorer.io/getTokenHistory"
        rc = RestClient()
        params = {
            "apiKey": "ethplorer.widget",
            "type": "transfer",
            "domain": "https%3A%2F%2Fethplorer.io%2Flast",
            "limit": 50
        }
        header = {"user-agent": HTTP_HEADER}
        result = rc.api_get(url=request_url, params=params, headers=header)
        operations = result.get("operations", None)
        for operation in operations:
            opn = operation.get("tokenInfo", None)
            address = opn.get("address")
            symbol = opn.get("symbol")
            bt_data = AddressTag.objects.filter(tag=symbol).first()
            if bt_data is None:
                create_tagd = AddressTag.objects.create(
                    tag=symbol,
                    threat_level=1,
                    comment="etheplore",
                    cate="contract"
                )
                Address.objects.create(
                    tag=create_tagd,
                    asset="ETH",
                    address=address,
                    is_commit="commit",
                    is_checked="checked"
                )
                print("create", symbol, "success")
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
                    print("create address", address, "success")
