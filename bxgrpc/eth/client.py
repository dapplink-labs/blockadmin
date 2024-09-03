#encoding=utf-8

import grpc
# from bixinrpc.blockindexer import ethindexer_pb2_grpc
# from bixinrpc.blockindexer import ethindexer_pb2
# from bixinrpc.common_pb2 import Empty
# from django.conf import settings

class ETHGRPCClient:
    pass
    # def __init__(self):
    #     channel = grpc.insecure_channel(settings.ETH_GRPC_CHANNEL_URL)
    #     self.stub = ethindexer_pb2_grpc.EthIndexerStub(channel)
    #
    # def get_tag_by_addr(self, addr: str, consumer_token: str = None):
    #     return self.stub.GetTagByAddr(
    #             ethindexer_pb2.AddrRequest(
    #                 consumer_token=consumer_token,
    #                 addr=addr)
    #             )
    #
    # def get_block_height(self, hash: str, consumer_token: str = None):
    #     return self.stub.GetBlockHeight(
    #             ethindexer_pb2.BlockHashRequest(
    #                 hash=hash,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def get_max_height(self):
    #     return self.stub.GetMaxHeight(Empty())
    #
    # def get_block_by_height(self, height: int, consumer_token: str = None):
    #     return self.stub.GetBlockByHeight(
    #             ethindexer_pb2.BlockHeightRequest(
    #                 height=height,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def get_tx_by_txid(self, txid: str, consumer_token: str = None):
    #     unit64_txid = convert_txid_to_uint64(txid)
    #     return self.stub.GetTxByTxid(
    #             ethindexer_pb2.TxidRequest(
    #                 txid=unit64_txid,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def get_txs_by_addr(self, addr: str, page: int = 0, page_size: int = 100, only_unspent: bool = False, consumer_token: str = None):
    #     return self.stub.GetTxsByAddr(
    #             ethindexer_pb2.AddrPageRequest(
    #                 consumer_token=consumer_token,
    #                 addr=addr,
    #                 page=page,
    #                 page_size=page_size,
    #                 only_unspent=only_unspent)
    #             )
    #
    # def get_txs_by_height(self, height: int, page: int = 0, page_size: int = 100, consumer_token: str = None):
    #     return self.stub.GetTxsByHeight(
    #             ethindexer_pb2.HeightPageRequest(
    #                 height=height,
    #                 page=page,
    #                 page_size=page_size,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def get_addr(self, addr: str, consumer_token: str = None):
    #     return self.stub.GetAddr(
    #             ethindexer_pb2.AddrRequest(
    #                 consumer_token=consumer_token,
    #                 addr=addr)
    #             )
    #
    # def create_tag(self, addr: str, threat_level: int, tag: str, comment: str, cate: str, consumer_token: str = None):
    #     return self.stub.CreateTag(
    #             btcindexer_pb2.CreateTagRequest(
    #                 addr=addr,
    #                 threat_level=threat_level,
    #                 tag=tag,
    #                 comment=comment,
    #                 cate=cate,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def delete_tag(self, gaddrid: int, consumer_token: str = None):
    #     return self.stub.DeleteTag(
    #             btcindexer_pb2.DeleteTagRequest(
    #                 gaddrid=gaddrid,
    #                 consumer_token=consumer_token)
    #             )
    #
    # def get_tags(self, page: int = 0, page_size: int = 100, consumer_token: str = None):
    #     return self.stub.GetTags(
    #             btcindexer_pb2.GetTagsRequest(
    #                 page=page,
    #                 page_size=page_size,
    #                 consumer_token=consumer_token)
    #             )
