#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from spiders.beekuaibao_helper import BeekuaibaoSpider


BeeKuaiBaoUrl = "https://www.beekuaibao.com/article/727722045612208128"


class Command(BaseCommand, BeekuaibaoSpider):
    def __init__(self):
        super(BeekuaibaoSpider, self).__init__(connect=BeeKuaiBaoUrl)

    def handle(self, *args, **options):
        self.bkb_spider_info()
