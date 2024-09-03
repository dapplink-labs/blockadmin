#encoding=utf-8


import logging
from django.shortcuts import redirect, render, reverse
from common.models import AddressTag, Address
from common.helpers import paged_items
from common.froms.tag_address_from import TagAddressForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.const import ThreatLevelList


AssetList = ["BTC", "ETH", "USDT"]


@login_required
def address_list(request):
    tag_id = request.GET.get('tag_id', 0)
    tag = request.GET.get('tag', "")
    asset = request.GET.get('asset', "all")
    page = request.GET.get('page', 1)
    asset_list = AssetList
    tag_address_list = Address.objects.all()
    if tag_id not in [0, "0"]:
        btd = AddressTag.objects.filter(id=tag_id).first()
        if btd is not None:
            tag_address_list = tag_address_list.filter(tag=btd)
    if tag not in [0, "0", "", None]:
        btd = AddressTag.objects.filter(tag=tag).first()
        if btd is not None:
            tag_address_list = tag_address_list.filter(tag=btd)
    if asset not in ["all", None, "None", ""]:
        tag_address_list = tag_address_list.filter(asset=asset)
    tag_address_list = tag_address_list.order_by('-id')
    tag_address_list = paged_items(request, tag_address_list)
    return render(request, 'ltag_manage/address_list.html', locals())


@csrf_exempt
@login_required
def create_address(request):
    if request.method == 'GET':
        tag_address_form = TagAddressForm(request)
        return render(request, 'ltag_manage/address_add.html', locals())
    elif request.method == 'POST':
        tag_address_form = TagAddressForm(request, request.POST)
        if tag_address_form.is_valid():
            tag_address_form.save_a()
            return redirect('address_list')
        else:
            error_msg = '标签库里面没有这个标签，请检查输入的标签是否正确或先去录入'
            href_url = 'address_list'
            return render(request, 'error.html', locals())


@csrf_exempt
@login_required
def upd_tag_address(request, address_id):
    page = request.GET.get('page', 1)
    tag_id = request.GET.get('tag_id', 0)
    tag_address = Address.objects.filter(id=address_id).order_by("-id").first()
    if request.method == 'GET':
        tag_address_form = TagAddressForm(request, instance=tag_address)
        return render(request, 'ltag_manage/address_upd.html', locals())
    elif request.method == 'POST':
        tag_address_form = TagAddressForm(request, request.POST, instance=tag_address)
        if tag_address_form.is_valid():
            tag_address_form.save()
            if tag_id in [0, "all", None]:
                return redirect(reverse('address_list') + '?page='+str(page))
            else:
                return redirect(reverse('address_list') + '?tag_id='+str(tag_id)+'&page='+str(page))
        else:
            return render(request, 'ltag_manage/address_upd.html', locals())


@login_required
def delete_tag_address(request, address_id):
    page = request.GET.get('page', 1)
    Address.objects.filter(id=address_id).delete()
    return redirect(reverse('address_list') + '?page='+str(page))