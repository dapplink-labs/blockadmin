#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from spiders.block123_helper import Block_124_BaseUrl


Block123BaseUrl = 'https://www.block123.com/zh-hans/feature/awesome-ethereum-defi-decentralized-finance-list/'


class Command(BaseCommand, Block_124_BaseUrl):
    def __init__(self):
        super(Block_124_BaseUrl, self).__init__(connect=Block123BaseUrl)

    def handle(self, *args, **options):
        self.ci_spider_urls()
        self.ci_spider_info()