from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from common.views.group import (
    btc_group_list, group_tag_list, edit_group_tag, group_address_list,
    create_btc_group, create_btc_tag, delete_group_tag, update_group_tag
)
from common.views.local_tag import (
    create_tag, get_tag_list, edit_tag, delete_tag, log_list, loginout, file_import, contract_import
)
from common.views.local_address import (
    address_list, create_address, upd_tag_address, delete_tag_address
)
from common.views.remote_tag import (
    rget_tags, rcreate_tag, get_addrs_by_tagid, get_group_tag_by_addr, rdelete_tag
)
from common.views.api import (
    get_eth_tag_by_addr, get_tag_num, get_entity_info_by_tag, get_entity_info_by_address, get_exchange_address
)
from common.views.entity import (
    entity_list, add_entity, upd_entity, delete_entity,
    get_entity_tag
)


urlpatterns: List[Any] = [
    path(r'', get_tag_list, name='index'),

    # 标签组
    path(r'btc_group_list', btc_group_list, name='btc_group_list'),
    path(r'group_tag_list', group_tag_list, name='group_tag_list'),
    path(r'edit_group_tag', edit_group_tag, name='edit_group_tag'),
    path(r'group_address_list', group_address_list, name='group_address_list'),
    path(r'create_btc_group', create_btc_group, name='create_btc_group'),
    path(r'create_btc_tag', create_btc_tag, name='create_btc_tag'),
    path(r'update_group_tag/<int:tag_id>', update_group_tag, name='update_group_tag'),

    path(r'create_tag', create_tag, name='create_tag'),
    path(r'edit_tag', edit_tag, name='edit_tag'),
    path(r'delete_tag', delete_tag, name='delete_tag'),
    path(r'get_tag_list', get_tag_list, name='get_tag_list'),
    path(r'log_list', log_list, name='log_list'),
    path(r'file_import', file_import, name='file_import'),
    path(r'contract_import', contract_import, name='contract_import'),
    path(r'loginout', loginout, name='loginout'),

    path(r'address_list', address_list, name='address_list'),
    path(r'create_address', create_address, name='create_address'),
    path(r'upd_tag_address/<int:address_id>', upd_tag_address, name='upd_tag_address'),
    path(r'delete_tag_address/<int:address_id>', delete_tag_address, name='delete_tag_address'),

    # 远程标签
    path(r'rget_tags', rget_tags, name='rget_tags'),
    path(r'rcreate_tag', rcreate_tag, name='rcreate_tag'),
    path(r'rdelete_tag', rdelete_tag, name='rdelete_tag'),
    path(r'delete_group_tag', delete_group_tag, name='delete_group_tag'),
    path(r'get_addrs_by_tagid', get_addrs_by_tagid, name='get_addrs_by_tagid'),
    path(r'get_group_tag_by_addr', get_group_tag_by_addr, name='get_group_tag_by_addr'),

    # 实体信息
    path(r'entity_list', entity_list, name='entity_list'),
    path(r'add_entity', add_entity, name='add_entity'),
    path(r'upd_entity/<int:entity_id>', upd_entity, name='upd_entity'),
    path(r'delete_entity/<int:entity_id>', delete_entity, name='delete_entity'),
    path(r'get_entity_tag/<int:entity_id>', get_entity_tag, name='get_entity_tag'),

    # api
    path(r'get_eth_tag_by_addr', get_eth_tag_by_addr, name='get_eth_tag_by_addr'),
    path(r'get_tag_num', get_tag_num, name='get_tag_num'),
    path(r'get_entity_info_by_tag', get_entity_info_by_tag, name='get_entity_info_by_tag'),
    path(r'get_entity_info_by_address', get_entity_info_by_address, name='get_entity_info_by_address'),
    path(r'get_exchange_address', get_exchange_address, name='get_exchange_address'),
]
