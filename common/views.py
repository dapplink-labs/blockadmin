#encoding=utf-8

import logging
import re
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings

from common.helpers import ok_json, error_json
from common.forms import TagForm
from common.decorators import access_token_required
from bxgrpc.btc.client import BTCGRPCClient
from bxgrpc.eth.client import ETHGRPCClient


# @access_token_required
# def get_tags(request):
#     coin = reqeust.GET.get('coin', 'btc')
#     page = request.GET.get('page')
#     page_size = request.GET.get('page_size')
#
#     if coin == 'btc':
#         client = BTCGRPCClient()
#     elif coin == 'eth':
#         client = ETHGRPCClient()
#     else:
#         return HttpResponse('coin is not supported!')
#     tags = client.get_tags(page, page_size)
#     return render(request, '', locals())
#
# @access_token_required
# def create_tag(request):
#     if coin == 'btc':
#         client = BTCGRPCClient()
#     elif coin == 'eth':
#         client = ETHGRPCClient()
#     else:
#         return HttpResponse('coin is not supported!')
#
#     result = client.create_tag()
#     return render(request, '', locals())
#
# @access_token_required
# def delete_tag(request):
#     pass

