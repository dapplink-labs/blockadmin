#encoding=utf-8

import ast
import json
import logging
from django import forms
from common.models import Address, AddressTag


class TagAddressForm(forms.ModelForm):
    tag = forms.CharField(required=True)
    asset = forms.CharField(required=True)
    address = forms.CharField(required=True)
    is_commit = forms.CharField(
        initial=2,
        widget=forms.Select(
            choices=(('uncommit', 'uncommit'), ('commit', 'commit'),)
        )
    )
    is_checked = forms.CharField(
        initial=3,
        widget=forms.Select(
            choices=(('uncheck', 'uncheck'), ('checking', 'checking'), ('checked', 'checked'),)
        )
    )
    is_real_addr = forms.CharField(
        initial=3,
        widget=forms.Select(
            choices=(('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown'),)
        )
    )

    class Meta:
        model = Address
        fields = [
            'tag', 'asset', 'address', 'is_commit', 'is_checked', 'is_real_addr'
        ]
        error_messages = {
            'tag': {
                'required': '请选择Tag'
            },
            'asset': {
                'required': '请输入资产名称'
            },
            'address': {
                'required': '请输入地址'
            },
            'is_commit': {
                'required': '请选择是否提交'
            },
            'is_checked': {
                'required': '请选择是否审核'
            },
            'is_real_addr': {
                'required': '请选择是否是真实地址'
            },
        }

    def __init__(self, request, *args, **kw):
        self.request = request
        super(TagAddressForm, self).__init__(*args, **kw)

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        tag_s = AddressTag.objects.filter(tag=tag).order_by("-id").first()
        if tag_s is None:
            return self.add_error('tag', '没有这个Tag, 请先去创建')
        return tag_s

    def clean_asset(self):
        asset = self.cleaned_data.get('asset')
        if asset in ['', None]:
            return self.add_error('asset', 'asset不能为空')
        return asset

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address in ['', None]:
            return self.add_error('address', 'address不能为空')
        return address

    def clean_is_commit(self):
        is_commit = self.cleaned_data.get('is_commit')
        return is_commit

    def clean_is_checked(self):
        is_checked = self.cleaned_data.get('is_checked')
        if is_checked in ['', None]:
            return self.add_error('is_checked', '需要选择 is_checked')
        return is_checked

    def clean_is_real_addr(self):
        is_real_addr = self.cleaned_data.get('is_real_addr')
        return is_real_addr

    def save_a(self):
        super(TagAddressForm, self).save(commit=True)
