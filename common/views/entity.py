#encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.models import EntityInfo, AddressTag
from common.helpers import paged_items
from common.froms.entity_form import EntityInfoForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.const import ThreatLevelList


@login_required
def entity_list(request):
    name = request.GET.get('name', "")
    page = request.GET.get('page', 1)
    entity_lists = EntityInfo.objects.all()
    if name not in ["", "None", None]:
        entity_lists = entity_lists.filter(name__icontains=name)
    entity_lists = entity_lists.order_by('-id')
    entity_lists = paged_items(request, entity_lists)
    return render(request, 'entity/entity_list.html', locals())


@csrf_exempt
@login_required
def add_entity(request):
    if request.method == 'GET':
        entity_form = EntityInfoForm(request)
        return render(request, 'entity/add_entity.html', locals())
    elif request.method == 'POST':
        entity_form = EntityInfoForm(request, request.POST)
        if entity_form.is_valid():
            entity_form.save()
            return redirect('entity_list')
        else:
            error_msg = '数据输入错误'
            href_url = 'entity_list'
            return render(request, 'error.html', locals())


@csrf_exempt
@login_required
def upd_entity(request, entity_id):
    page = request.GET.get('page', 1)
    entity = EntityInfo.objects.get(id=entity_id)
    if request.method == 'GET':
        entity_form = EntityInfoForm(request,  instance=entity)
        return render(request, 'entity/upd_entity.html', locals())
    elif request.method == 'POST':
        entity_form = EntityInfoForm(request, request.POST, instance=entity)
        if entity_form.is_valid():
            entity_form.save()
            return redirect(reverse('entity_list') + '?page='+str(page))
        else:
            return render(request, 'entity/upd_entity.html', locals())


@login_required
def delete_entity(request, entity_id):
    page = request.GET.get('page', 1)
    EntityInfo.objects.filter(id=entity_id).delete()
    return redirect(reverse('entity_list') + '?page='+str(page))


@login_required
def get_entity_tag(request, entity_id):
    entity_info = EntityInfo.objects.filter(id=entity_id).order_by("-id").first()
    if entity_info is not None:
        tag_list = AddressTag.objects.filter(entity=entity_info)
        tag_list = tag_list.order_by('-id')
        tag_list = paged_items(request, tag_list)
        return render(request, 'entity/entity_tag.html', locals())
    else:
        error_msg = '没有这个实体信息'
        href_url = 'entity_list'
        return render(request, 'error.html', locals())
