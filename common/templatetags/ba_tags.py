#encoding=utf-8

import json
import time
import pytz
from django import template
from django.conf import settings
from datetime import timedelta
from decimal import Decimal
from urllib.parse import urljoin
from django.contrib.contenttypes.models import ContentType
from common.models import AddressTag


register = template.Library()


@register.filter(name='hdatetime')
def repr_datetime(value) -> str:
    if not value:
        return ''
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')


@register.filter(name='timestamp_data')
def timestamp_data(value):
    timeArray = time.localtime(int(value))
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


@register.filter(name='btc_trans')
def btc_trans(value):
    if not value:
        return "0"
    value = Decimal(value) / Decimal(10e7)
    value = value.quantize(Decimal('0.0000'))
    return value.to_integral() if value == value.to_integral() else value.normalize()


@register.filter(name='is_real_addr')
def is_real_addr(value):
    return {
        'Yes': '是',
        'No': '不是',
        'Unknown': '未知',
    }.get(value, '')


@register.filter(name='tag_name')
def tag_name(value):
    address_tag = AddressTag.objects.filter(id=int(value)).first()
    return address_tag.tag



