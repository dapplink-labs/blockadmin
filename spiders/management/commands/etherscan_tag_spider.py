#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from spiders.models import SpiderUrl
from spiders.etherscan_helper import (
    EtherScanTagSipder, SpiderName, AccountCommet, TokenComment, LimitSize
)
from spiders.helpers import TagDataHelper


def more_page_url(base_url, value, records):
    request_url_list = []
    start = 0
    while int(records) > start:
        lastest_url = base_url + \
                      '?subcatid=' + str(value) + \
                      "&size=" + LimitSize + \
                      "&start=" + str(start) \
                      + "&order=asc"
        request_url_list.append(lastest_url)
        start = start + int(LimitSize)
    return request_url_list


def tk_tab_url(ests, tk_url, tk_records):
    at_url_r_list = []
    tab_url_list = ests.tab_pages(tk_url)
    print("tab_url_list=", tab_url_list)
    if tab_url_list is not None:
        for tab_url in tab_url_list:
            mp_url_list = more_page_url(
                tk_url,
                tab_url.get("val", str(1)),
                tab_url.get("records", 0)
            )
            for mp_url in mp_url_list:
                at_url_r_list.append(mp_url)
    else:
        at_url_r_list = more_page_url(tk_url, 1, tk_records)
    return at_url_r_list


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "exec_task",
            type=str,
            default="spider",
            help="init | crawl, init:create spider url; crawl: crawl data"
        )

        parser.add_argument(
            "--at",
            type=str,
            default="",
            help="account | token, account:crawl account data; token: crawl token data"
        )

    def handle(self, *args, **options):
        exec_task = options['exec_task']
        at = options['at']
        ests = EtherScanTagSipder()
        if exec_task == "init":        # 生成基本的抓取页面
            ests.create_db_url()
        elif exec_task == "crawl":     # 抓取数据
            url_list = SpiderUrl.objects.filter(name=SpiderName, status="UnCrawl").order_by("-id").all()
            url_list = url_list if at == "" else url_list.filter(comment=at)
            if url_list is None:
                raise ValueError("spider url is None, please create spider url at first")
            for at_url in url_list:
                if at_url.url not in ["", None]:
                    if at_url.comment == AccountCommet:
                        print("database account url and records", at_url.url, at_url.records)
                        account_url_list = tk_tab_url(ests, at_url.url, at_url.records)
                        print("account_url_list=", account_url_list)
                        for re_url in account_url_list:
                            print("account request url is ", re_url)
                            account_list = ests.get_accounts_detail(url=re_url)
                            for acct in account_list:
                                address_list = []
                                address_list.append(acct.get("address", ""))
                                TagDataHelper(
                                    asset="ETH",
                                    tag=acct.get("account_name", ""),
                                    comment="etherscan",
                                    cate="contract",
                                    address_list=address_list,
                                    threat_level=1
                                ).data_2db()
                                print("create", acct.get("account_name", ""), "success")
                    elif at_url.comment == TokenComment:
                        logging.info("database token url = %s and records = %s", at_url.url, at_url.records)
                        token_url_list = tk_tab_url(ests, at_url.url, at_url.records)
                        print("token_url_list=", token_url_list)
                        for re_url in token_url_list:
                            token_list = ests.get_token_detail(re_url)
                            for token in token_list:
                                address_list = []
                                address_list.append(token.get("address", ""))
                                TagDataHelper(
                                    asset="ETH",
                                    tag=token.get("token_name", ""),
                                    comment="etherscan",
                                    cate="contract",
                                    address_list=address_list,
                                    threat_level=1
                                ).data_2db()
                                print("create", token.get("address", ""), "success")
                    else:
                        raise ValueError("No this type url %s", at_url.comment)
                else:
                    continue
                at_url.status = 'Crawled'
                at_url.save()
        else:
            raise Exception("invalid command, please choose init or crawl, init:create spider url; crawl: crawl data")