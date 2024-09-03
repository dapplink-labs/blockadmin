#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import math
from django.conf import settings
from django.core.management.base import BaseCommand
from common.models import GroupTag, GroupInfo, EntityInfo
from bxgrpc.client import BTCGRPCClient


PageSize = 100


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = BTCGRPCClient()
        count = client.count("tag")
        total_page = math.ceil(int(count.id) / PageSize)
        for page in range(total_page):
            result = client.get_tags(page=(page + 1), page_size=PageSize)
            for id in result.ids:
                ret_tag = client.get_tag(id)
                gt = GroupTag.objects.filter(g_tag=ret_tag.tag.tagname).order_by("-id").first()
                db_entity = EntityInfo.objects.filter(name__iexact=ret_tag.tag.tagname).order_by("-id").first()
                if gt is None:
                    GroupTag.objects.create(
                        romute_id=ret_tag.tag.tagid,
                        entity=db_entity if db_entity is not None else None,
                        g_tag=ret_tag.tag.tagname,
                        g_cate=ret_tag.tag.cate,
                        take_evidence_exp=ret_tag.tag.take_evidence_exp,
                    )
                else:
                    if db_entity is None:
                        gt.entity = gt.entity
                    else:
                        gt.entity = db_entity
                    gt.group = gt.group
                    gt.g_tag=ret_tag.tag.tagname
                    gt.g_cate=ret_tag.tag.cate
                    gt.take_evidence_exp=ret_tag.tag.take_evidence_exp
                    gt.save()
