#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from spiders.chaininfo_helper import ChainInfoSpider


ChainBaseUrl = 'https://chain.info/'


class Command(BaseCommand, ChainInfoSpider):
    def __init__(self):
        super(ChainInfoSpider, self).__init__(connect=ChainBaseUrl)

    def handle(self, *args, **options):
        self.chain_info_spider()