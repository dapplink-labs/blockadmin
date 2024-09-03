from pytz import timezone
from django.conf import settings
from django.db import models, transaction
from typing import Dict

from django.db import models
from common.base_model import BaseModel
from django.contrib.postgres.fields import JSONField


CHECKED_CHOICES = [(x, x) for x in ['uncheck', 'checking', 'checked']]
COMMIT_CHOICES = [(x, x) for x in ['uncommit', 'commit']]
COMMON_STATUS = [(x, x) for x in ['ACTIVE', 'DOWN']]
TAG_CATE = [(x, x) for x in ['exchange', 'service', 'pool', 'gambling', 'market', 'contract', 'special', 'hacker', 'dex', 'other']]
SERVICE_TYPE = [(x, x) for x in ['centralization', 'distribution']]
IS_REAL_CHOICES = [(x, x) for x in ['Yes', 'No', 'Unknown']]
MONITOR_CHOICES = [(x, x) for x in ['Yes', 'No']]


class Account(BaseModel):
    SIDE_CHOICES = [(x, x) for x in ['long', 'short']]
    name = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default="", )

    class Meta:
        pass

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
        }


# 实体信息表
class EntityInfo(BaseModel):
    name = models.CharField(max_length=200, default="", unique=True)  # 实体名称
    introduce = models.TextField(default='')                          # 实体介绍
    website = models.TextField(default='')                            # 多个网址用竖线分割
    email = models.TextField(default='')                              # 多个 eamil 用竖线分割
    phone = models.TextField(default='')                              # 多个 phone 用竖线分割
    address = models.TextField(default='')                            # 多个物理地址用竖线分割
    track_des = models.TextField(default='')                          # 追踪描述
    tune_up_index = models.IntegerField(default=0)                    # 可调证指数
    extra_info = JSONField(default=dict)                              # 其他信息
    is_monitor = models.CharField(max_length=100, choices=MONITOR_CHOICES, default='No', db_index=True)

    class Meta:
        pass

    def __str__(self) -> str:
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'introduce': self.introduce,
            'website': self.website,
            'eamil': self.email,
            'phone': self.phone,
            'address': self.address,
            'track_des': self.track_des,
            'tune_up_index': self.tune_up_index,
            'extra_info': self.extra_info,
            'is_monitor': self.is_monitor,
        }


# 组信息表
class GroupInfo(BaseModel):
    gaddr_id = models.CharField(max_length=200, default="")    # 组ID
    address_num = models.IntegerField(default=0)               # 地址数量
    tx_num = models.IntegerField(default=0)                    # 交易数量
    amount = models.CharField(max_length=200, default="")      # 组金额
    first_date = models.CharField(max_length=200, default="")  # 第一次出现时间
    last_date = models.CharField(max_length=200, default="")   # 第一次出现时间

    class Meta:
        pass

    def __str__(self) -> str:
        return self.gaddr_id

    def as_dict(self):
        return {
            'id': self.id,
            'group_number': self.gaddr_id,
            'address_num': self.address_num,
            'tx_num': self.tx_num,
            'amount': self.amount,
            'first_date': self.first_date,
            'last_date': self.last_date
        }


# 组标签表
class GroupTag(BaseModel):
    entity = models.ForeignKey(EntityInfo, related_name='group_entity', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(GroupInfo, related_name='group_tag', on_delete=models.CASCADE, null=True)
    romute_id = models.IntegerField(default=0)
    g_tag = models.CharField(max_length=200, default="", unique=True)
    g_threat_level = models.IntegerField(default=0)
    take_evidence_exp = models.IntegerField(default=0)
    g_cate = models.CharField(max_length=200, choices=TAG_CATE, default="exchange")
    g_service_type = models.CharField(max_length=200, choices=SERVICE_TYPE, default="centralization")
    g_tag_we = models.CharField(max_length=200, default="")
    g_comment = models.CharField(max_length=200, default="")
    g_is_commit = models.CharField(max_length=100, choices=COMMIT_CHOICES, default="uncommit", db_index=True)
    g_is_checked = models.CharField(max_length=100, choices=CHECKED_CHOICES, default="uncheck", db_index=True)
    g_status = models.CharField(max_length=100, choices=COMMON_STATUS, default='ACTIVE', db_index=True)

    class Meta:
        pass

    def __str__(self) -> str:
        return self.g_tag

    def as_dict(self):
        return {
            'id': self.id,
            'g_tag': self.g_tag,
            'g_cate': self.g_cate,
            'g_tag_we': self.g_tag_we,
            'g_comment': self.g_comment,
            'g_is_commit': self.g_is_commit,
            'g_is_checked': self.g_is_checked,
            'g_status': self.g_status
        }


# 地址标签
class AddressTag(BaseModel):
    entity = models.ForeignKey(EntityInfo, related_name='tag_entity', on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=200, default="", unique=True, db_index=True)
    threat_level = models.IntegerField(default=0)
    cate = models.CharField(max_length=200, choices=TAG_CATE, default="exchange")
    service_type = models.CharField(max_length=200, choices=SERVICE_TYPE, default="centralization")
    tag_we = models.CharField(max_length=200, default="")
    comment = models.CharField(max_length=200, default="")
    is_commit = models.CharField(max_length=100, choices=COMMIT_CHOICES, default="uncommit", db_index=True)
    is_checked = models.CharField(max_length=100, choices=CHECKED_CHOICES, default="uncheck", db_index=True)
    status = models.CharField(max_length=100, choices=COMMON_STATUS, default='ACTIVE', db_index=True)

    class Meta:
        pass

    def __str__(self) -> str:
        return self.tag

    def get_tag(self, tag_id):
        tag = self.objects.filter(id=tag_id).order_by("-id").first()
        return tag.tag

    def as_dict(self):
        return {
            'id': self.id,
            'tag': self.tag,
            'cate': self.cate,
            'tag_we': self.tag_we,
            'comment': self.comment,
            'is_commit': self.is_commit,
            'is_checked': self.is_checked,
            'status': self.status
        }


# 地址
class Address(BaseModel):
    tag = models.ForeignKey(AddressTag, related_name='tag_address', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(GroupInfo, related_name='group_address', on_delete=models.CASCADE, null=True)
    asset = models.CharField(max_length=200, default='', db_index=True)
    address = models.CharField(max_length=200, default='', db_index=True)
    tx_num = models.IntegerField(default=0)
    unspent_tx_num = models.IntegerField(default=0)
    amount = models.CharField(max_length=200, default='')
    in_amount = models.CharField(max_length=200, default='')       # 转入金额
    out_amount = models.CharField(max_length=200, default='')      # 转出金额
    in_times = models.CharField(max_length=200, default='')        # 转入中出现的次数
    out_times = models.CharField(max_length=200, default='')       # 转出中出现的次数
    in_first_date = models.CharField(max_length=200, default='')   # 转入首次出现时间
    out_first_date = models.CharField(max_length=200, default='')  # 转出首次出现时间
    in_last_date = models.CharField(max_length=200, default='')    # 转入末次出现时间
    out_last_date = models.CharField(max_length=200, default='')   # 转出末次出现时间
    is_real_addr = models.CharField(max_length=100, choices=IS_REAL_CHOICES, default="Unknown", db_index=True)
    is_commit = models.CharField(max_length=100, choices=COMMIT_CHOICES, default="uncommit", db_index=True)
    is_checked = models.CharField(max_length=100, choices=CHECKED_CHOICES, default="uncheck", db_index=True)
    status = models.CharField(max_length=100, choices=COMMON_STATUS, default='ACTIVE')

    class Meta:
        pass

    def __str__(self) -> str:
        return self.address

    def as_dict(self):
        return {
            'id': self.id,
            'asset': self.asset,
            'address': self.address,
            'tx_num': self.tx_num,
            'unspent_tx_num': self.unspent_tx_num,
            'amount': self.amount,
            'in_amount': self.in_amount,
            'out_amount': self.out_amount,
            'in_times': self.in_times,
            'out_times': self.out_times,
            'in_first_date': self.in_first_date,
            'out_first_date': self.out_first_date,
            'in_last_date': self.in_last_date,
            'out_last_date': self.out_last_date,
            'is_commit': self.is_commit,
            'is_checked': self.is_checked,
            'status': self.status
        }


# tag 实体错误日志表
class TagErrorLog(BaseModel):
    LOG_TYPE_CHOICES = [(x, x) for x in ['GaddridFail', 'CreateFail', 'OtherFail']]
    gaddrid = models.CharField(max_length=200, default='')
    grp_tag = models.ForeignKey(GroupTag, related_name='g_tag_log',on_delete=models.CASCADE, null=True)
    addr_tag = models.ForeignKey(AddressTag, related_name='a_tag_log', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, choices=LOG_TYPE_CHOICES, default="GaddridFail", db_index=True)
    code = models.CharField(max_length=200, default='404', db_index=True)
    can_retry = models.CharField(max_length=200, default='true', db_index=True)
    brief = models.CharField(max_length=200, default='', db_index=True)
    detail = models.CharField(max_length=800, default="")

    class Meta:
        pass

    def as_dict(self):
        return {
            'id': self.id,
            'grp_tag': self.grp_tag,
            'addr_tag': self.addr_tag,
            'type': self.type,
            'code': self.code,
            'brief': self.brief,
            'detail': self.detail,
        }


class DataCahe(BaseModel):
    key = models.CharField(max_length=64, default='', primary_key=True)
    values = models.CharField(max_length=128, default='')

    class Meta:
        pass

    def as_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'values': self.values,
        }
