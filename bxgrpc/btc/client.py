#encoding=utf-8

import grpc
from bixinrpc import btc_pb2_grpc
from bixinrpc import btc_pb2
from django.conf import settings
from bxgrpc.helpers import convert2uint


class BTCGRPCClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.BTC_GRPC_CHANNEL_URL, options=options)
        self.stub = btc_pb2_grpc.BtcStub(channel)

    def get_group_tag_by_addr(self, addr: str, consumer_token: str = None):
        return self.stub.GetGroupTagByAddr(
                btc_pb2.AddrRequest(
                    consumer_token=consumer_token,
                    addr=addr)
                )

    def get_group_tag_by_txhash_and_seq(self, txhash: str, seq: int, consumer_token: str = None):
        return self.stub.GetGrouptagByTxhashAndSeq(
                btc_pb2.TxhashSeqRequest(
                    txhash=txhash,
                    seq=seq,
                    consumer_token=consumer_token)
                )

    def get_tx_by_txid(self, txid, consumer_token: str = None):
        if isinstance(txid, str):
            unit64_txid = convert2uint(txid)
        else:
            unit64_txid = txid

        return self.stub.GetTxByTxid(
                btc_pb2.TxidRequest(
                    txid=unit64_txid,
                    consumer_token=consumer_token)
                )

    def get_txids_by_addr(self, addr: str, only_unspent: bool = False, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetTxidsByAddr(
                btc_pb2.AddrPageRequest(
                    addr=addr,
                    only_unspent=only_unspent,
                    page=page,
                    page_size=page_size,
                    consumer_token=consumer_token)
                )

    def get_addr(self, addr: str, consumer_token: str = None):
        return self.stub.GetAddr(
                btc_pb2.AddrRequest(
                    consumer_token=consumer_token,
                    addr=addr)
                )

    def create_addr_group(self, addrid: int, gaddrid: int, consumer_token: str = None):
        return self.stub.CreateAddrGroup(
                btc_pb2.CreateAddrGroupRequest(
                    addrid=addrid,
                    gaddrid=gaddrid,
                    consumer_token=consumer_token)
                )

    def create_tag(self, gaddrid: int, threat_level: int, tag: str, tag_we: str, comment: str, cate: str, consumer_token: str = None):
        return self.stub.CreateTag(
                btc_pb2.CreateTagRequest(
                    gaddrid=gaddrid,
                    threat_level=threat_level,
                    tag=tag,
                    comment=comment,
                    cate=cate,
                    tag_we=tag_we,
                    consumer_token=consumer_token)
                )

    def delete_tag(self, gaddrid: int, consumer_token: str = None):
        return self.stub.DeleteTag(
                btc_pb2.DeleteTagRequest(
                    gaddrid=gaddrid,
                    consumer_token=consumer_token)
                )

    def get_tags(self, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetTags(
                btc_pb2.GetTagsRequest(
                    page=page,
                    page_size=page_size,
                    consumer_token=consumer_token)
                )

    def get_tag(self, gaddrid: int, consumer_token: str = None):
        return self.stub.GetTag(
                btc_pb2.GetTagRequest(
                       gaddrid=gaddrid,
                       consumer_token=consumer_token)
                )

    def get_addrs_by_gaddrid(self, gaddrid: int, page: int = 0, page_size: int = 100, consumer_token: str = None):
        return self.stub.GetAddrsByGaddrid(
                btc_pb2.AddrsByGaddridRequest(
                    gaddrid=gaddrid,
                    page=page,
                    page_size=page_size,
                    consumer_token=consumer_token)
                )
