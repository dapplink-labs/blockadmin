#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from common.models import AddressTag, TagErrorLog
from bxgrpc.client import BTCGRPCClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        tag_lists = AddressTag.objects.filter(is_commit="uncommit")
        for tag in tag_lists:
            if tag.asset == "BTC":
                client = BTCGRPCClient()
                gaddrid_data = client.get_addr(tag.address)
                if gaddrid_data.code != 0:
                    self.log_create(
                        tag=tag,
                        code=gaddrid_data.error.code,
                        brief=gaddrid_data.error.brief,
                        detail="获取 gaddrid 失败",
                        type="GaddridFail",
                        error_log=gaddrid_data.error.detail,
                    )
                if gaddrid_data.tag == tag.tag:
                    logging.info("remote equal database tag %s", tag.tag)
                    continue
                else:
                    del_ret = client.delete_tag(int(gaddrid_data.gaddrid))
                    if del_ret.code != 0:
                        self.log_create(
                            tag=tag,
                            code=del_ret.error.code,
                            brief=del_ret.error.brief,
                            detail="删除 gaddrid 失败",
                            type="GaddridFail",
                            error_log=del_ret.error.detail,
                        )
                    else:
                        data_create = client.create_tag(
                            threat_level=1,
                            comment="",
                            cate=tag.cate,
                        )
                        if data_create.code != 0:
                            TagErrorLog.objects.create(
                                gaddrid=gaddrid_data.gaddrid,
                                type=gaddrid_data.cate,
                                code=data_create.code,
                                brief=data_create.brief,
                                can_retry=data_create.can_retry,
                                detail=data_create.brief
                            )
                tag.is_commit = "commit"
                tag.save()
            elif tag.asset == "ETH":
                continue
            else:
                logging.error("No support asset %s", tag.asset)


    def log_create(self, tag, code, brief, detail, type, error_log):
        tag_log = TagErrorLog.objects.create(
            tag=tag,
            code=code,
            brief=brief,
            detail=detail,
            type=type,
            error_log=error_log,
        )
        return tag_log
