#encoding=utf-8

import logging
import time
import math
from django.conf import settings
from django.core.management.base import BaseCommand
import grpc
from concurrent import futures

from bixinrpc import tag_pb2_grpc
from common.grpc_server import TagServer

class Command(BaseCommand):
    def handle(self, *args, **options):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        tag_pb2_grpc.add_TagServicer_to_server(
              TagServer(), server)
        server.add_insecure_port('[::]:50250')
        server.start()
        server.wait_for_termination()
