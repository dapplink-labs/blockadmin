#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from django.core.management.base import BaseCommand
from django.db import transaction

from common.models import DataCahe, Address
from spiders.etherscan_helper import EtherScanTagSipder

class Command(BaseCommand):

    # must always restart
    def handle(self, *args, **options):
        ests = EtherScanTagSipder()

        key = 'etherscan_token_valid_since_id'
        data, _ = DataCahe.objects.get_or_create(key=key, defaults={'values': '0'})
        since_id = int(data.values)

        for address in Address.objects.filter(asset='ETH', id__gte=since_id).order_by('id'):
            try:
                result = ests.check_token_valid(address.address)
            except:
                logging.error('EtherScan Error when since_id is %s, address is %s', since_id, address)
                time.sleep(5)
                break

            with transaction.atomic():
                since_id = address.id
                data.values = str(since_id)
                if result:
                    address.is_real_addr = 'Yes'
                else:
                    address.is_real_addr = 'No'

                data.save()
                address.save()

        print('current since_id is %s', since_id)
