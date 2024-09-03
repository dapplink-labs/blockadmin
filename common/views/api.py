#encoding=utf-8

import logging
import json
from django.views.decorators.csrf import csrf_exempt
from common.helpers import check_bearer_auth, ok_json, error_json
from common.models import AddressTag, Address, GroupTag, EntityInfo
from common.const import ThreatLevelList


HuoId = 1
BinanceId = 2
OkexId = 4


@csrf_exempt
@check_bearer_auth
def get_eth_tag_by_addr(request):
    params = json.loads(request.body.decode())
    address = params.get('address')
    tag_addr = Address.objects.filter(address=address).first()
    if tag_addr is not None:
        tag_addr_data = {
            "address": address,
            "tag": tag_addr.tag.tag,
            "threat_level": tag_addr.tag.threat_level,
            "cate": tag_addr.tag.cate,
            "tag_we": tag_addr.tag.tag_we,
            "comment": tag_addr.tag.comment
        }
        return ok_json(tag_addr_data)
    else:
        return error_json("No this Tag", 4000)


@csrf_exempt
@check_bearer_auth
def get_tag_num(request):
    btc_total_tag = GroupTag.objects.filter(g_status='ACTIVE').count()
    eth_total_tag = AddressTag.objects.filter(status='ACTIVE').count()
    ret_data = {
        "btc_tag_num": btc_total_tag,
        "eth_tag_num": eth_total_tag
    }
    return ok_json(ret_data)


@csrf_exempt
@check_bearer_auth
def get_entity_info_by_tag(request):
    params = json.loads(request.body.decode())
    tag_name = params.get('tag_name')
    asset = params.get('asset')
    if asset in ["BTC", 'btc', "Btc"]:
        group_tag = GroupTag.objects.filter(g_tag=tag_name).order_by("-id").first()
        if group_tag is not None:
            entity = group_tag.entity
            return ok_json(entity.as_dict())
        else:
            return error_json("No This Btc Asset", 4000)
    elif asset in ["ETH", 'eth', "Eth"]:
        address_tag = AddressTag.objects.filter(tag=tag_name).order_by("-id").first()
        if address_tag is not None:
            entity = address_tag.entity
            return ok_json(entity.as_dict())
        else:
            return error_json("No This Eth Asset", 4000)
    else:
        return error_json("No This Asset", 4000)


@csrf_exempt
@check_bearer_auth
def get_entity_info_by_address(request):
    params = json.loads(request.body.decode())
    address = params.get('address')
    address = Address.objects.filter(address=address).order_by("-id").first()
    if address is not None:
        return ok_json(address.tag.entity.as_dict())
    else:
        return error_json("No This Address", 4000)


@csrf_exempt
@check_bearer_auth
def get_exchange_address(request):
    params = json.loads(request.body.decode())
    asset = params.get('asset')
    entity_list = EntityInfo.objects.filter(is_monitor='Yes').order_by("-id").first()
    ret_address_list = []
    for entity in entity_list:
        tag_list = AddressTag.objects.filter(entity=entity)
        for tag in tag_list:
            address_list = Address.objects.filter(asset=asset, tag=tag).order_by("-id").all()
            for address in address_list:
                ret_address_list.append(address.address)
    return ok_json(ret_address_list)


