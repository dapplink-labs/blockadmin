#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from django.conf import settings
from django.core.management.base import BaseCommand


# 将远程的 BTC 标签地址拉到本地做规则匹配
class Command(BaseCommand):
    def handle(self, *args, **options):
        pass