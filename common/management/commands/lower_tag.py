#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import AddressTag
from bxgrpc.client import BTCGRPCClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        for tag in AddressTag.objects.all():
            if tag.tag:
                lower_tag = tag.tag.lower()
                if not AddressTag.objects.filter(tag=lower_tag).exists():
                    tag.tag = tag.tag.lower()
                    tag.save()
        print('lower tag success')
