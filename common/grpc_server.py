#encoding=utf-8

import logging
import json
from common.models import AddressTag, Address, GroupTag, EntityInfo
from bixinrpc import tag_pb2_grpc
from bixinrpc import tag_pb2
from bixinrpc import common_pb2
from common.helpers import check_bearer_auth


class TagCate:
    all: int
    exchange: int
    service: int
    pool: int
    gambling: int
    market: int
    contract: int
    special: int
    hacker: int
    dex: int
    other: int

    def __init__(self):
        self.all = 0
        self.exchange = 1
        self.service = 2
        self.pool = 3
        self.gambling = 4
        self.market = 5
        self.contract = 6
        self.special = 7
        self.hacker = 8
        self.dex = 9
        self.other = 10

    def get_tag_cate(self, cate: int) -> str:
        if cate == self.exchange:
            return 'exchange'
        elif cate == self.service:
            return 'service'
        elif cate == self.pool:
            return 'pool'
        elif cate == self.gambling:
            return 'gambling'
        elif cate == self.market:
            return 'market'
        elif cate == self.contract:
            return 'contract'
        elif cate == self.special:
            return 'special'
        elif cate == self.hacker:
            return 'hacker'
        elif cate == self.dex:
            return 'dex'
        elif cate == self.other:
            return 'other'
        else:
            return 'all'


def grpc_error(error_msg='', response=None):
    error = common_pb2.Error(
        code=1,
        brief=error_msg,
        detail=error_msg,
        can_retry=True)
    if response:
        return response(error=error)
    return error


class TagServer(tag_pb2_grpc.TagServicer):
    def getEthTagByAddr(self, request, context):
        address = request.address
        tag_addr = Address.objects.get(address__iexact=address)
        if not tag_addr:
            return grpc_error('No this Tag', tag_pb2.EthTagResponse)
        else:
            tag=tag_addr.tag
            tag_response = tag_pb2.EthTag(
                address=address,
                tagname=tag.tag,
                threat_level=tag.threat_level,
                cate=tag.cate,
                tag_we=tag.tag_we,
                comment=tag.comment,
                is_true=tag_addr.is_real_addr,
            )
            return tag_pb2.EthTagResponse(tag=tag_response)

    def getEthTagByTagName(self, request, context):
        tag_name = request.tag_name
        tag_cate = request.tag_cate
        tag = AddressTag.objects.filter(tag__iexact=tag_name, cate=tag_cate).order_by("-id").first()
        if not tag:
            return grpc_error('No this Tag', tag_pb2.EthTagResponse)
        else:
            addr = Address.objects.filter(tag=tag).order_by("-id").first()
            tag_response = tag_pb2.EthTag(
                address=addr.address,
                tagname=tag.tag,
                threat_level=tag.threat_level,
                cate=tag.cate,
                tag_we=tag.tag_we,
                comment=tag.comment,
                is_true=addr.is_real_addr,
            )
            return tag_pb2.EthTagResponse(tag=tag_response)

    def getTagCount(self, request, context):
        btc_total_tag = GroupTag.objects.filter(g_status='ACTIVE').count()
        eth_total_tag = AddressTag.objects.filter(status='ACTIVE').count()
        return tag_pb2.TagCountResponse(
                btc_tag_count=btc_total_tag,
                eth_tag_count=eth_total_tag)

    def getEntityInfoByTag(self, request, context):
        tagname = request.tagname
        asset = request.asset.lower()
        if asset not in ('btc', 'eth'):
            return grpc_error('No This Asset', tag_pb2.EntityInfoResponse)
        if asset == 'btc':
            tag = GroupTag.objects.filter(g_tag=tagname).order_by("-id").first()
            if not tag:
                return grpc_error('No This Btc Asset', tag_pb2.EntityInfoResponse)
        else:
            tag = AddressTag.objects.filter(tag=tagname).order_by("-id").first()
            if not tag:
                return grpc_error('No This Eth Asset', tag_pb2.EntityInfoResponse)
        entity = tag.entity
        if not entity:
            return grpc_error('No This Entity Asset', tag_pb2.EntityInfoResponse)
        return tag_pb2.EntityInfoResponse(
                name=entity.name,
                introduce=entity.introduce,
                website=entity.website,
                email=entity.email,
                phone=entity.phone,
                address=entity.address,
                track_des=entity.track_des,
                tune_up_index=entity.tune_up_index
        )


    def getEntityInfoByAddress(self, request, context):
        address = request.address
        address = Address.objects.filter(address__iexact=address).order_by("-id").first()
        if not address:
            return grpc_error('No This Address', tag_pb2.EntityInfoResponse)
        entity = address.tag.entity
        if not entity:
            return grpc_error('No This Entity Asset', tag_pb2.EntityInfoResponse)
        return tag_pb2.EntityInfoResponse(
                name=entity.name,
                introduce=entity.introduce,
                website=entity.website,
                email=entity.email,
                phone=entity.phone,
                address=entity.address,
                track_des=entity.track_des,
                tune_up_index=entity.tune_up_index
        )

    def getMonitorTagAddress(self, request, context):
        asset = request.asset
        page = request.page
        pagesize = request.pagesize
        cate = request.cate
        start = page * pagesize
        end = start + pagesize
        tc = TagCate()
        tag_cate = tc.get_tag_cate(cate)
        entity_list = EntityInfo.objects.filter(is_monitor='Yes').order_by("-id")[start:end]
        addrs = []
        for entity in entity_list:
            if tag_cate == 'all':
                addr_tag_list = AddressTag.objects.filter(entity=entity)
            else:
                addr_tag_list = AddressTag.objects.filter(entity=entity, cate=tag_cate)
            for tag in addr_tag_list:
                address_list = Address.objects.filter(asset=asset, tag=tag, is_real_addr='Yes').order_by("-id").all()
                for address in address_list:
                    addrs.append(address.address)
        return tag_pb2.MonitorTagAddressResponse(addrs=addrs)

    def getTagAddress(self, request, context):
        asset = request.asset
        page = request.page
        pagesize = request.pagesize
        cate = request.cate
        start = page * pagesize
        end = start + pagesize
        tc = TagCate()
        tag_cate = tc.get_tag_cate(cate)
        if tag_cate == 'all':
            addr_tag_list = AddressTag.objects.filter(status='ACTIVE').order_by("-id")[start:end]
        else:
            addr_tag_list = AddressTag.objects.filter(status='ACTIVE', cate=tag_cate).order_by("-id")[start:end]
        exchange_addr_list = []
        for addr_tag in addr_tag_list:
            addr_list = []
            for address in Address.objects.filter(tag=addr_tag, asset=asset, is_real_addr='Yes').order_by("-id").all():
                addr_list.append(address.address)
            exchange_address = tag_pb2.TagAddress(
                tag_id=addr_tag.id,
                tag=addr_tag.tag,
                tag_cate=addr_tag.cate,
                address=addr_list,
            )
            exchange_addr_list.append(exchange_address)
        return tag_pb2.TagAddressResponse(
            tag_addr=exchange_addr_list
        )
