#encoding=utf-8

from urllib import parse

from django.shortcuts import redirect, render, reverse
from common.models import GroupInfo, GroupTag, Address, EntityInfo
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.froms.group_tag_form import GroupTagForm
from common.const import ExchangeTypeList
from bxgrpc.client import BTCGRPCClient
from bxgrpc.helpers import convert2uint
from django import forms
from common.const import ThreatLevelList


class CreateBtcTagForm(forms.Form):
    tag_name = forms.CharField(required=True)
    take_evidence_exp = forms.IntegerField(
        initial=3,
        widget=forms.Select(
            choices=((1, 1), (2, 2), (3, 3),)
        )
    )
    threat_level = forms.IntegerField(
        initial=6,
        widget=forms.Select(
            choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
        )
    )
    cate = forms.CharField(
        initial=6,
        widget=forms.Select(
            choices=(('exchange', 'exchange'), ('service', 'service'), ('pool', 'pool'), ('gambling', 'gambling'),
                     ('market', 'market'), ('contract', 'contract'), ('other', 'other'))
        )
    )
    comment = forms.CharField(required=False)


    def __init__(self, request, *args, **kw):
        self.request = request
        super(CreateBtcTagForm, self).__init__(*args, **kw)

    def clean_tag_name(self):
        tag_name = self.cleaned_data.get('tag_name')
        return tag_name

    def clean_take_evidence_exp(self):
        take_evidence_exp = self.cleaned_data.get('take_evidence_exp')
        return take_evidence_exp

    def clean_threat_level(self):
        threat_level = self.cleaned_data.get('threat_level')
        return threat_level

    def clean_cate(self):
        cate = self.cleaned_data.get('cate')
        return cate

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        return comment


@login_required
def btc_group_list(request):
    gaddr_id = request.GET.get('gaddr_id', "")
    page = request.GET.get('page', 1)
    group_lists = GroupInfo.objects.all()
    if gaddr_id not in ["", "None", None]:
        group_lists = group_lists.filter(gaddr_id__icontains=gaddr_id)
    group_lists = group_lists.order_by('-id')
    group_lists = paged_items(request, group_lists)
    return render(request, 'group/group_list.html', locals())


@login_required
def group_tag_list(request):
    gaddr_id = request.GET.get('gaddr_id', "")
    page = request.GET.get('page', 1)
    tag = request.GET.get('tag', "")
    cate = request.GET.get('cate', "all")
    cate_list = ExchangeTypeList
    group_tag_list = GroupTag.objects.all()
    if gaddr_id not in ["", "None", None]:
        group = GroupInfo.objects.filter(gaddr_id=gaddr_id).order_by("-id").first()
        group_tag_list = group_tag_list.fiter(group=group)
    if tag not in ["all", "", "None", None]:
        group_tag_list = group_tag_list.filter(g_tag__icontains=tag)
    if cate not in ["all", "", "None", None]:
        group_tag_list = group_tag_list.filter(g_cate=cate)
    group_tag_list = group_tag_list.order_by('-id')
    group_tag_list = paged_items(request, group_tag_list)
    return render(request, 'group/group_tag_list.html', locals())


@login_required
def group_address_list(request):
    gaddr_id = request.GET.get('gaddr_id', "")
    page = request.GET.get('page', 1)
    address_list = Address.objects.filter(asset='BTC').order_by("-id")
    if gaddr_id not in ["", "None", None]:
        group = GroupInfo.objects.filter(gaddr_id=gaddr_id).order_by("-id").first()
        address_list = address_list.fiter(group=group)
    address_list = address_list.order_by('-id')
    address_list = paged_items(request, address_list)
    return render(request, 'group/group_address_list.html', locals())


@csrf_exempt
@login_required
def edit_group_tag(request):
    tag_id = request.GET.get('tag_id', 0)
    page = request.GET.get('page', 1)
    entity_list = EntityInfo.objects.all()
    group_tag = GroupTag.objects.get(id=tag_id)
    if request.method == 'GET':
        group_tag_form = GroupTagForm(request, instance=group_tag)
        return render(request, 'group/group_tag_edit.html', locals())
    elif request.method == 'POST':
        group_tag_form = GroupTagForm(request, request.POST, instance=group_tag)
        if group_tag_form.is_valid():
            group_tag_form.save()
            return redirect(reverse('group_tag_list') + '?page=' + str(page))
        else:
            return render(request, 'group/group_tag_edit.html', locals())


@csrf_exempt
@login_required
def create_btc_group(request):
    if request.method == 'GET':
        msg = "请输入要创建组的地址，点击提交"
        return render(request, 'group/create_group.html', locals())
    else:
        address = request.POST.get('address', "")
        btc_rpc_client = BTCGRPCClient()
        ret = btc_rpc_client.create_group(convert2uint(address))
        if ret.code != 0:
            msg = "该组已经存在,请不要重复创建" + ret.brief
        else:
            msg = "创建组成功，请去做相应的操作"
        return render(request, 'group/create_group.html', locals())


@csrf_exempt
@login_required
def create_btc_tag(request):
    if request.method == 'GET':
        msg = "请输入要创建Tag的的信息，点击提交"
        cb_form = CreateBtcTagForm(request)
        return render(request, 'group/create_tag.html', locals())
    else:
        btc_rpc_client = BTCGRPCClient()
        cb_form = CreateBtcTagForm(request, request.POST)
        if cb_form.is_valid():
            create_tag = btc_rpc_client.create_tag(
                tagname=cb_form.clean_tag_name(),
                take_evidence_exp=int(cb_form.clean_take_evidence_exp()),
                threat_level=int(cb_form.clean_threat_level()),
                cate=cb_form.clean_cate(),
                comment=cb_form.clean_comment()
            )
            GroupTag.objects.create(
                g_tag=cb_form.clean_tag_name(),
                romute_id=create_tag.id,
                g_threat_level=int(cb_form.clean_threat_level()),
                take_evidence_exp=int(cb_form.clean_take_evidence_exp()),
                g_cate=cb_form.clean_cate(),
            )
            msg = "创建标签成功, 请去做相应的操作, 返回ID为: " + str(create_tag.id)
        return render(request, 'group/create_tag.html', locals())



@login_required
def delete_group_tag(request):
    asset = request.GET.get('asset', 'BTC')
    tag_id = request.GET.get('tag_id', 0)
    up_down = request.GET.get('up_down', 'next')
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 100))
    client = BTCGRPCClient()
    client.delete_tag(tagid=int(tag_id))
    return redirect(
        reverse("rget_tags")
        + "?asset=" + asset
        +"&up_down=" + up_down
        + "&page=" + str(page-1)
        + "&page_size" + str(page_size)
    )


class UpdateBtcTagForm(CreateBtcTagForm):
    tag_id = forms.IntegerField(required=True)

    def __init__(self, request, *args, **kw):
        super().__init__(request, *args, **kw)

    def clean_tag_id(self):
        tag_id = self.cleaned_data.get('tag_id')
        return tag_id


@csrf_exempt
@login_required
def update_group_tag(request, tag_id):
    btc_rpc_client = BTCGRPCClient()
    if request.method == 'GET':
        msg = "请输入要创建Tag的的信息，点击提交"
        ret_tag_info = btc_rpc_client.get_tag(int(tag_id))
        upd_form = UpdateBtcTagForm(
            request,
            initial={
                'tag_id': ret_tag_info.tag.tagid,
                'tag_name': ret_tag_info.tag.tagname,
                'cate':  ret_tag_info.tag.cate
            }
        )
        return render(request, 'group/update_rgroup_tag.html', locals())
    elif request.method == 'POST':
        upd_form = UpdateBtcTagForm(request, request.POST)
        if upd_form.is_valid():
            data_ret = btc_rpc_client.update_tag(
                tagid=upd_form.clean_tag_id(),
                tagname=upd_form.clean_tag_name(),
                take_evidence_exp=int(upd_form.clean_take_evidence_exp()),
                threat_level=int(upd_form.clean_threat_level()),
                cate=upd_form.clean_cate(),
                comment=upd_form.clean_comment()
            )
            if data_ret.code != 0:
                error_msg = data_ret.brief
                href_url = 'rget_tags'
                return render(request, 'error.html', locals())
            else:
                refer = request.META.get('HTTP_REFERER')
                if not refer:
                    return redirect(reverse("rget_tags"))
                query = parse.urlparse(refer).query
                return redirect(reverse("rget_tags") + '?%s' % query)
