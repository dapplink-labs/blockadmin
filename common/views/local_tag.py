#encoding=utf-8

import xlrd
import logging
from django.shortcuts import redirect, render, reverse
from common.models import AddressTag, TagErrorLog, Address, EntityInfo
from common.helpers import paged_items
from common.froms.block_data_from import BlockTagDataForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from common.const import ExchangeTypeList
from common.const import ThreatLevelList


def validate_excel(value):
    if value.name.split('.')[-1] not in ['xls', 'xlsx', 'csv']:
        raise ValidationError(_('Invalid File Type: %(value)s'),params={'value': value},)


class UploadExcelForm(forms.Form):
    excel = forms.FileField(validators=[validate_excel])


@csrf_exempt
@login_required
def create_tag(request):
    if request.method == 'GET':
        block_form = BlockTagDataForm(request)
        return render(request, 'ltag_manage/tag_add.html', locals())
    elif request.method == 'POST':
        block_form = BlockTagDataForm(request, request.POST)
        if block_form.is_valid():
            block_form.save()
            return redirect('get_tag_list')
        else:
            error_msg = '数据输入错误，请检查之后再输入'
            href_url = 'get_tag_list'
            return render(request, 'error.html', locals())


@login_required
def get_tag_list(request):
    tag = request.GET.get('tag', '')
    cate = request.GET.get('cate', 'all')
    tag_all = request.GET.get('tag_all', '')
    is_commit = request.GET.get('is_commit', 'all')
    is_checked = request.GET.get('is_checked', 'all')
    page = request.GET.get('page', 1)
    cate_list = ExchangeTypeList
    tags_list = AddressTag.objects.all()
    if tag not in ['all', None, '']:
        tags_list = tags_list.filter(tag__icontains=tag)
    if tag_all not in ['all', None, '']:
        tags_list = tags_list.filter(tag=tag_all)
    if is_checked not in ['all', None]:
        tags_list = tags_list.filter(is_checked=is_checked)
    tags_list = tags_list.order_by('-id')
    tags_list = paged_items(request, tags_list)
    return render(request, 'ltag_manage/tag_list.html', locals())


@csrf_exempt
@login_required
def edit_tag(request):
    tag_id = request.GET.get('tag_id', 0)
    page = request.GET.get('page', 1)
    entity_list = EntityInfo.objects.all()
    block_tag = AddressTag.objects.get(id=tag_id)
    if request.method == 'GET':
        block_form = BlockTagDataForm(request,  instance=block_tag)
        return render(request, 'ltag_manage/tag_edit.html', locals())
    elif request.method == 'POST':
        block_form = BlockTagDataForm(request, request.POST, instance=block_tag)
        if block_form.is_valid():
            block_form.save()
            query = '?page=%s&tag=%s' % (page, block_tag.tag)
            return redirect(reverse('get_tag_list') + query)
        else:
            return render(request, 'ltag_manage/tag_edit.html', locals())


@login_required
def delete_tag(request):
    tag_id = request.GET.get('tag_id', 0)
    page = request.GET.get('page', 1)
    AddressTag.objects.filter(id=tag_id).delete()
    return redirect(reverse('get_tag_list') + '?page=' + str(page))


@login_required
def log_list(request):
    address = request.GET.get('address', '')
    tag = request.GET.get('tag', '')
    tag_log_list = TagErrorLog.objects.all()
    if address not in ["", '', None]:
        block_tag = AddressTag.objects.filter(address=address).first()
        tag_list = tag_log_list.filter(tag=block_tag)
    if tag not in ["", '', None]:
        block_tag = AddressTag.objects.filter(tag=tag).order_by('-id').first()
        tag_list = tag_log_list.filter(tag=block_tag)
    tag_log_list = tag_log_list.order_by('-id')
    tag_log_list = paged_items(request, tag_log_list)
    return render(request, 'ltag_manage/log_list.html', locals())


@login_required
def file_import(request):
    if request.method == "GET":
        return render(request, 'ltag_manage/import_file.html', locals())
    if request.method == "POST":
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = wb.sheets()[0]
            row = table.nrows
            for i in range(1, row):
                col = table.row_values(i)
                create_tag = AddressTag.objects.create(
                    tag=col[0],
                    cate="other",
                    is_commit='commit',
                    is_checked='checked'
                )
                # 处理 BTC 充币
                output_1 = col[1].split('\n')
                for addr_1 in output_1:
                    Address.objects.create(
                        tag=create_tag,
                        asset="BTC",
                        address=addr_1,
                        is_commit='commit',
                        is_checked='checked'
                    )
                # # 处理 BTC 提币
                output_2 = col[2].split('\n')
                for addr_2 in output_2:
                    Address.objects.create(
                        tag=create_tag,
                        asset="BTC",
                        address=addr_2,
                        is_commit='commit',
                        is_checked='checked'
                    )
                # 处理 ETH 充币
                output_3 = col[3].split('\n')
                for addr_3 in output_3:
                    Address.objects.create(
                        tag=create_tag,
                        asset="ETH",
                        address=addr_3,
                        is_commit='commit',
                        is_checked='checked'
                    )
                # 处理 ETH 提币
                output_4 = col[4].split('\n')
                for addr_4 in output_4:
                    Address.objects.create(
                        tag=create_tag,
                        asset="ETH",
                        address=addr_4,
                        is_commit='commit',
                        is_checked='checked'
                    )
        return redirect(get_tag_list)


@login_required
def contract_import(request):
    if request.method == "GET":
        return render(request, 'ltag_manage/import_file.html', locals())
    if request.method == "POST":
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = wb.sheets()[0]
            row = table.nrows
            for i in range(1, row):
                col = table.row_values(i)
                create_tag = AddressTag.objects.create(
                    tag=col[0],
                    is_commit='commit',
                    is_checked='checked'
                )
                output = col[1].split('\n')
                for addr in output:
                    Address.objects.create(
                        tag=create_tag,
                        asset="ETH",
                        address=addr,
                        is_commit='commit',
                        is_checked='checked'
                    )
        return redirect(get_tag_list)


@login_required
def loginout(request):
    logout(request)
    return redirect('/admin/login')
