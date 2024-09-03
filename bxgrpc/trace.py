#encoding=utf-8

from django.conf import settings

from bxgrpc.client import BTCGRPCClient
from bxgrpc.helpers import is_standard_tag, convert2uint
from bxgrpc.block import get_addr_info, get_txinfo_by_txhash, get_group_by_groupid
from bxgrpc.block import get_tag_by_tagid, get_txids_by_addrid, get_addr_to, get_addr_from

def trace_tx(txhash):
    client = BTCGRPCClient()
    data = get_txinfo_by_txhash(txhash, client=client)
    inputs = []
    outputs = []

    for _input in data['inputs']:
        info = _input
        info['addr_info'] = get_addr_info(_input['addr'], client=client)
        groupid = info['addr_info'].get('gaddrid', None)
        info['group_info'] = get_group_by_groupid(groupid, client=client)
        if info['group_info']['tags']:
            info['prev_txhash'] = ''
        inputs.append(info)

    for _output in data['outputs']:
        info = _output
        info['addr_info'] = get_addr_info(_output['addr'], client=client)
        groupid = info['addr_info'].get('gaddrid', None)
        info['group_info'] = get_group_by_groupid(groupid, client=client)
        if info['group_info']['tags']:
            info['spent_txhash'] = ''
        outputs.append(info)

    data['inputs'] = inputs
    data['outputs'] = outputs
    return data

def trace_addr(addr):
    client = BTCGRPCClient()
    addr_info = get_addr_info(addr, client=client)
    data = {
        'inputs': [],
        'outputs': [],
        'addr_info': addr_info,
        'group_info': get_group_by_groupid(addr_info['gaddrid'], client=client)
    }
    if is_standard_tag(data['group_info']['tags']):
        return data

    for _to in get_addr_to(addr, client=client):
        from_addr_info = get_addr_info(_to['fromid'], client=client)
        # TODO get txhashs
        # to_addr_info = get_addr_info(_to.toid, client=client)
        info = {
            'addr_info': from_addr_info,
            'group_info': get_group_by_groupid(from_addr_info['gaddrid'], client=client)
        }
        data['inputs'].append(info)

    for _from in get_addr_from(addr, client=client):
        # TODO get txhashs
        # from_addr_info = get_addr_info(_from.fromid, client=client)
        to_addr_info = get_addr_info(_from['toid'], client=client)
        info = {
            'addr_info': to_addr_info ,
            'group_info': get_group_by_groupid(to_addr_info['gaddrid'], client=client)
        }
        data['outputs'].append(info)

    return data
