#encoding=utf-8

import grpc
from bixinrpc import btc_pb2_grpc
from bixinrpc import btc_pb2
from bixinrpc.common_pb2 import Empty
from django.conf import settings

class BTCGRPCClient:

    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.BTC_GRPC_CHANNEL_URL, options=options)
        self.stub = btc_pb2_grpc.BtcStub(channel)

    def get_latest_height(self):
        return self.stub.GetLatestHeight(Empty())

    def get_addr(self, addrid, consumer_token: str = None):
        return self.stub.GetAddr(
                btc_pb2.IdRequest(
                    id=addrid,
                    consumer_token=consumer_token)
                )

    def get_block_tx(self, blockid, page:int = 0, pagesize:int = 10000, consumer_token:str = None):
        return self.stub.GetBlockTx(
                btc_pb2.IdPageRequest(
                    id=blockid,
                    consumer_token=consumer_token,
                    page=page,
                    pagesize=pagesize)
                )

    def get_tx(self, txid, consumer_token: str = None):
        return self.stub.GetTx(
                btc_pb2.IdRequest(
                    id=txid,
                    consumer_token=consumer_token)
                )

    def get_group(self, groupid, consumer_token: str = None):
        return self.stub.GetGroup(
                btc_pb2.IdRequest(
                    id=groupid,
                    consumer_token=consumer_token)
                )

    def get_tag(self, tagid, consumer_token: str = None):
        return self.stub.GetTag(
                btc_pb2.IdRequest(
                    id=tagid,
                    consumer_token=consumer_token)
                )

    def get_txids_by_addrid(self, addrid, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetTxidsByAddrid(
                btc_pb2.IdPageRequest(
                    id=addrid,
                    page=page,
                    pagesize=page_size,
                    consumer_token=consumer_token)
                )

    def get_addr_to(self, addrid, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetAddrTo(
                btc_pb2.IdPageRequest(
                    id=addrid,
                    page=page,
                    pagesize=page_size,
                    consumer_token=consumer_token)
                )

    def get_addr_from(self, addrid, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetAddrFrom(
                btc_pb2.IdPageRequest(
                    id=addrid,
                    page=page,
                    pagesize=page_size,
                    consumer_token=consumer_token)
                )

    def get_addrids_by_gaddrid(self, group_id, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetAddridsByGaddrid(
                btc_pb2.IdPageRequest(
                    id=group_id,
                    page=page,
                    pagesize=page_size,
                    consumer_token=consumer_token)
                )

    def create_tag(self, tagname: str, take_evidence_exp: int,
                    threat_level: int, cate: str, comment: str,
                   consumer_token: str = None):
        return self.stub.CreateTag(
                btc_pb2.CreateTagRequest(
                    tag=btc_pb2.Tag(
                            tagname=tagname,
                            take_evidence_exp=take_evidence_exp,
                            threat_level=threat_level,
                            cate=cate,
                            comment=comment),
                    consumer_token=consumer_token)
                )

    def delete_tag(self, tagid: int, consumer_token: str = None):
        return self.stub.DeleteTag(
                btc_pb2.IdRequest(
                    id=tagid,
                    consumer_token=consumer_token)
                )

    def update_tag(self, tagid, tagname, take_evidence_exp,
                   threat_level, cate, comment,
                   consumer_token: str = None):
        return self.stub.UpdateTag(
                btc_pb2.UpdateTagRequest(
                    consumer_token=consumer_token,
                    tag=btc_pb2.Tag(
                        tagid=tagid,
                        tagname=tagname,
                        take_evidence_exp=take_evidence_exp,
                        threat_level=threat_level,
                        cate=cate,
                        comment=comment)
                    )
                )

    def get_tags(self, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetTags(
                btc_pb2.PageRequest(
                    page=page,
                    pagesize=page_size,
                    consumer_token=consumer_token)
                )

    def create_group(self, gaddrid,
                    addrs = 0, txs = 0,
                    amount = 0, tags = [],
                    first_date = 0, last_date = 0,
                    consumer_token: str = None):
        return self.stub.CreateGroup(
                btc_pb2.CreateGroupRequest(
                    group=btc_pb2.Group(
                        gaddrid=gaddrid,
                        addrs=addrs,
                        txs=txs,
                        amount=amount,
                        first_date=first_date,
                        last_date=last_date),
                    consumer_token=consumer_token)
                )

    def count(self, tablename: str, consumer_token: str = None):
        return self.stub.Count(
                btc_pb2.CountRequest(
                    consumer_token=consumer_token,
                    tablename=tablename)
                )

    def assoc_group_tag(self, gaddrid, tagid, consumer_token: str = None):
        return self.stub.AssocGroupTag(
                btc_pb2.WriteGroupTagRequest(
                    gaddrid=gaddrid,
                    tagid=tagid,
                    consumer_token=consumer_token)
                )

    def disassoc_group_tag(self, gaddrid, tagid, consumer_token: str = None):
        return self.stub.DisassocGroupTag(
                btc_pb2.WriteGroupTagRequest(
                    gaddrid=gaddrid,
                    tagid=tagid,
                    consumer_token=consumer_token)
                )
