#encoding=utf-8

import json
from django.shortcuts import render
from common.models import TagErrorLog, GroupTag
from bxgrpc.client import BTCGRPCClient
from django.contrib.auth.decorators import login_required
from bxgrpc.helpers import convert2uint
from django.shortcuts import redirect, render, reverse
from common.const import ExchangeTypeList
from common.const import ThreatLevelList


@login_required
def rget_tags(request):
    asset = request.GET.get('asset', 'BTC')
    up_down = request.GET.get('up_down', 'next')
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 100))
    if asset == "BTC":
        client = BTCGRPCClient()
        tag_data_list = []
        result = client.get_tags(page, page_size)
        for id in result.ids:
            ret_tag = client.get_tag(id)
            tag_data = {
                "id": id,
                "tagid": ret_tag.tag.tagid,
                "tag": ret_tag.tag.tagname,
                "cate": ret_tag.tag.cate,
            }
            tag_data_list.append(tag_data)
        tag_data_list.sort(key=lambda x: x["id"])
    if asset == "ETH":
        pass
    if up_down == "next":
        page += 1
    elif up_down == "prev":
        page -= 1
    else:
        page = 0
    return render(request, 'rtag_manage/tag_list.html', locals())


@login_required
def get_addrs_by_tagid(request):
    asset = request.GET.get('asset', 'BTC')
    tag_id = request.GET.get('tag_id', 0)
    up_down = request.GET.get('up_down', 'next')
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 30))
    if asset == "BTC":
        client = BTCGRPCClient()
        ret_tag = client.get_tag(int(tag_id))
        addr_list = []
        for gaddrid in ret_tag.tag.gaddrids:
            g_result = client.get_addrids_by_gaddrid(int(gaddrid), page=page, page_size=page_size)
            id_list = g_result.ids
            for id in id_list:
                result = client.get_addr(addrid=id)
                addr_data = {
                    "addr": result.addr.addr,
                    "txs": result.addr.txs,
                    "in_amount": result.addr.in_amount,
                    "in_times": result.addr.in_times,
                    "in_first_date": result.addr.in_first_date,
                    "in_last_date": result.addr.in_last_date,
                    "out_amount": result.addr.out_amount,
                    "out_times": result.addr.out_times,
                    "out_first_date": result.addr.out_first_date,
                    "out_last_date": result.addr.out_last_date,
                    "gaddrid": result.addr.gaddrid
                }
                addr_list.append(addr_data)
    else:
        error_msg = '不支持这个币种'
        href_url = 'rget_tags'
        return render(request, 'error.html', locals())
    if up_down == "next":
        page += 1
    elif up_down == "prev":
        page -= 1
    else:
        page = 0
    total_count = len(addr_list)
    return render(request, 'rtag_manage/address_list.html', locals())


def get_group_tag_by_addr(request):
    ex_type_list = ExchangeTypeList
    tl_lst = ThreatLevelList
    address = request.GET.get('address')
    msg = "请输入地址查询相关组信息，请确认数据是否需要更新，不需要更新直接跳过"
    local_tag_list = GroupTag.objects.filter(g_status='ACTIVE')
    if address not in ["", None, "None"]:
        client = BTCGRPCClient()
        addr_data = client.get_addr(convert2uint(address))
        if addr_data.addr.gaddrid != 0:
            group_data = client.get_group(addr_data.addr.gaddrid)
            addrs = group_data.group.addrs
            gaddrid = group_data.group.gaddrid
            ret_tag_list = []
            tag_list = group_data.group.tags
            for tag in tag_list:
                tag_dict = {
                    "tagid":tag.tagid,
                    "tagname":tag.tagname,
                    "take_evidence_exp":tag.take_evidence_exp,
                    "cate":tag.cate,
                    "comment":tag.comment
                }
                ret_tag_list.append(tag_dict)
            ret_tag_list = json.dumps(ret_tag_list)
            msg = "获信息成功，有问题可以点击去修改,没有问题请忽略"
    return render(request, 'rtag_manage/single_tag.html', locals())


@login_required
def rcreate_tag(request):
    address = request.GET.get('address')
    tag = request.GET.get('tag')
    client = BTCGRPCClient()
    gt = GroupTag.objects.filter(g_tag=tag).order_by("-id").first()
    if gt is not None:
        addr_data = client.get_addr(convert2uint(address))
        data_create = client.assoc_group_tag(
            gaddrid=addr_data.addr.gaddrid,
            tagid=gt.romute_id,
        )
        if data_create.code != 0:
            TagErrorLog.objects.create(
                gaddrid=convert2uint(address),
                type=gt.g_cate,
                code=data_create.code,
                brief=data_create.brief,
                can_retry=data_create.can_retry,
                detail=data_create.brief
            )
    return redirect(reverse("get_group_tag_by_addr") + "?address=" + address)


@login_required
def rdelete_tag(request):
    address = request.GET.get('address')
    tag = request.GET.get('tag')
    client = BTCGRPCClient()
    gt = GroupTag.objects.filter(g_tag=tag).order_by("-id").first()
    if gt is not None:
        addr_data = client.get_addr(convert2uint(address))
        data_create = client.disassoc_group_tag(
            gaddrid=addr_data.addr.gaddrid,
            tagid=gt.romute_id,
        )
        if data_create.code != 0:
            TagErrorLog.objects.create(
                gaddrid=convert2uint(address),
                type=gt.g_cate,
                code=data_create.code,
                brief=data_create.brief,
                can_retry=data_create.can_retry,
                detail=data_create.brief
            )
    return redirect(reverse("get_group_tag_by_addr") + "?address=" + address)


