#encoding=utf-8

from django.conf import settings

from bxgrpc.client import BTCGRPCClient
from bxgrpc.helpers import is_standard_tag, convert2uint

def get_latest_height(client=None):
    if not client:
        client = BTCGRPCClient()
    return client.get_latest_height()

def get_addr_info(addr, client=None):
    if not client:
        client = BTCGRPCClient()
    if isinstance(addr, str):
        result = client.get_addr(convert2uint(addr))
    else:
        result = client.get_addr(addr)
    addr_info = result.addr
    return {
        'addrid': addr_info.addrid,
        'addr': addr_info.addr,
        'txs': addr_info.txs,
        'amount': addr_info.in_amount - addr_info.out_amount,
        'in_amount': addr_info.in_amount,
        'out_amount': addr_info.out_amount,
        'in_times': addr_info.in_times,
        'out_times': addr_info.out_times,
        'in_first_date': addr_info.in_first_date,
        'in_last_date': addr_info.in_last_date,
        'out_first_date': addr_info.out_first_date,
        'out_last_date': addr_info.out_last_date,
        'gaddrid': addr_info.gaddrid,
    }

def get_txinfo_by_txhash(txhash: str, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.get_tx(convert2uint(txhash))

    inputs = []
    outputs = []
    tx = result.tx

    for _input in tx.inputs:
        if not _input:
            continue
        info = {
            'seq': _input.seq,
            'addr': _input.addr,
            'amount': _input.amount,
            'prev_txhash': _input.prev_txhash,
            'prev_txseq': _input.prev_txseq,
        }
        inputs.append(info)

    for _output in tx.outputs:
        if not _output:
            continue
        info = {
            'seq': _output.seq,
            'addr': _output.addr,
            'amount': _output.amount,
            'spent_txhash': _output.spent_txhash,
            'spent_txseq': _output.spent_txseq
        }
        outputs.append(info)

    return {
        'txid': tx.txid,
        'txhash': tx.txhash,
        'createdate': tx.createdate,
        'blockheight': tx.blockheight,
        'size': tx.size,
        'weight': tx.weight,
        'inputs_amount': tx.inputs_amount,
        'outputs_amount': tx.outputs_amount,
        'inputs': inputs,
        'outputs': outputs
    }

def get_group_by_groupid(groupid, client=None):
    if not client:
        client = BTCGRPCClient()
    info = {
        'gaddrid': 0,
        'txs': 0,
        'amount': 0,
        'first_date': 0,
        'last_date': 0,
        'tags': []
    }
    if not groupid:
        return info

    result = client.get_group(groupid)
    if result.error.code == 0:
        group = result.group
        info = {
            'gaddrid': group.gaddrid,
            'txs': group.txs,
            'amount': group.amount,
            'first_date': group.first_date,
            'last_date': group.last_date,
            'tags': []
        }
        for tag in group.tags:
            info['tags'].append({
                'tagid': tag.tagid,
                'tagname': tag.tagname,
                'take_evidence_exp': tag.take_evidence_exp,
                'threat_level': tag.threat_level,
                'cate': tag.cate,
                'comment': tag.comment
            })

    return info

def get_tag_by_tagid(tagid, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.get_tag(tagid)
    tag = result.tag
    return {
        'tagid': tag.tagid,
        'tagname': tag.tagname,
        'take_evidence_exp': tag.take_evidence_exp,
        'threat_level': tag.threat_level,
        'cate': tag.cate,
        'comment': tag.comment,
    }

def get_txids_by_addrid(addr: str, page=0, page_size=100, client=None):
    if not clinet:
        client = BTCGRPCClient()
    result = client.get_txids_by_addrid(convert2uint(addr), page, page_size)
    _ids = []
    for _id in result.ids:
        _ids.append(_id)
    return _ids

def get_addr_to(addr, page=0, page_size=100, client=None):
    if not client:
        client = BTCGRPCClient()
    if isinstance(addr, str):
        result = client.get_addr_to(convert2uint(addr), page, page_size)
    else:
        result = client.get_addr_to(addr, page, page_size)

    addr_tos = []
    for addr_to in result.from_tos:
        info = {
            'fromid': addr_to.fromid,
            'toid': addr_to.toid,
            'rank': addr_to.rank
        }
        addr_tos.append(info)
    return addr_tos

def get_addr_from(addr: str, page=0, page_size=100, client=None):
    if not client:
        client = BTCGRPCClient()
    if isinstance(addr, str):
        result = client.get_addr_from(convert2uint(addr), page, page_size)
    else:
        result = client.get_addr_from(addr, page, page_size)

    addr_froms = []
    for addr_from in result.from_tos:
        info = {
            'fromid': addr_from.fromid,
            'toid': addr_from.toid,
            'rank': addr_from.rank
        }
        addr_froms.append(info)
    return addr_froms

def get_addrids_by_gaddrid(group_id, page=0, page_size=100, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.get_addrids_by_gaddrid(group_id, page, page_size)
    _ids = []
    for _id in result.ids:
        _ids.append(_id)
    return _ids

def get_tags(page=0, page_size=100, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.get_tags(page, page_size)
    _ids = []
    for _id in result.ids:
        _ids.append(_id)
    return _ids

def create_tag(tagid, tagname, take_evidence_exp, threat_level, cate, comment, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.create_tag(tagid, tagname, take_evidence_exp,
                               threat_level, cate, comment)
    return result.id

def update_tag(tagid, tagname, take_evidence_exp, threat_level, cate, comment, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.update_tag(tagid, tagname, take_evidence_exp,
                               threat_level, cate, comment)
    return {
        'code': result.code,
        'brief': result.brief,
        'detail': result.detail,
        'can_retry': result.can_retry
    }

def delete_tag(tagid, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.delete_tag(tagid)
    return {
        'code': result.code,
        'brief': result.brief,
        'detail': result.detail,
        'can_retry': result.can_retry
    }

def create_group(gaddrid, addrs=0, txs=0, amount=0, tags=[], first_date=0, last_date=0, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.create_group(gaddrid,  addrs,
                                 txs, amount,
                                 tags, first_date, last_date)
    return {
        'code': result.code,
        'brief': result.brief,
        'detail': result.detail,
        'can_retry': result.can_retry
    }

def count(tablename: str, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.count(tablename)
    return result.id

def assoc_group_tag(gaddrid, addr: str, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.assoc_group_tag(gaddrid, convert2uint(addr))
    return {
        'code': result.code,
        'brief': result.brief,
        'detail': result.detail,
        'can_retry': result.can_retry
    }

def disassoc_group_tag(gaddrid, addr: str, client=None):
    if not client:
        client = BTCGRPCClient()
    result = client.disassoc_group_tag(gaddrid, convert2uint(addr))
    return {
        'code': result.code,
        'brief': result.brief,
        'detail': result.detail,
        'can_retry': result.can_retry
    }
