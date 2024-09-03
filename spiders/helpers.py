#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import List, Union, Dict, Any
from common.models import AddressTag, Address, DataCahe
from spiders.const import HTTP_HEADER


class DataCacheHelper:
    origin_values: str
    key: str
    values: str

    def __init__(self, origin_values: str, key: str, values: str):
        self.origin_values = origin_values
        self.key = key
        self.values = values

    def dc_logic(self):
        data_cc = DataCahe.objects.filter(key=self.key).first()
        if data_cc is not None:
            ret_value = int(data_cc.values)
            data_cc.values = self.values
            data_cc.save()
        else:
            DataCahe.objects.create(
                key=self.key,
                values=self.origin_values
            )
            ret_value = self.origin_values
        return ret_value


class TagDataHelper:
    asset: str
    tag: str
    threat_level: int
    comment: str
    cate: str
    address_list: List
    is_commit: str
    is_checked: str
    tag_we: str

    def __init__(
            self,
            asset: str,
            tag: str,
            comment: str,
            cate: str,
            address_list: List,
            threat_level: int = 1,
            is_commit: str = "commit",
            is_checked: str = "checked",
            tag_we: str = ""
    ):
        self.asset = asset
        self.tag = tag
        self.comment = comment
        self.cate = cate
        self.address_list = address_list
        self.threat_level = threat_level
        self.is_commit = is_commit
        self.is_checked = is_checked
        self.tag_we = tag_we

    def data_2db(self):
        bt_data = AddressTag.objects.filter(tag=self.tag).first()
        if bt_data is None:
            create_tagd = AddressTag.objects.create(
                tag=self.tag,
                threat_level=self.threat_level,
                comment=self.comment,
                cate=self.cate,
            )
            for address in self.address_list:
                Address.objects.create(
                    tag=create_tagd,
                    asset=self.asset,
                    address=address,
                    is_commit=self.is_commit,
                    is_checked=self.is_checked
                )
            print("create", self.tag, "success")
        else:
            for address in self.address_list:
                t_addr = Address.objects.filter(address=address).first()
                if t_addr is None:
                    Address.objects.create(
                        tag=bt_data,
                        asset=self.asset,
                        address=address,
                        is_commit=self.is_commit,
                        is_checked=self.is_checked
                    )
                    print("create address", address, "success")