#encoding=utf-8

import ast
import json
import logging
from django import forms
from common.models import EntityInfo


class EntityInfoForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=1024)
    introduce = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )
    website = forms.CharField(required=False, max_length=1024)
    email = forms.CharField(required=False, max_length=1024)
    phone = forms.CharField(required=False, max_length=1024)
    address = forms.CharField(required=False, max_length=1024)
    track_des = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )
    tune_up_index = forms.IntegerField(
        initial=3,
        widget=forms.Select(
            choices=((1, 1), (2, 2), (3, 3),)
        )
    )
    extra_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )
    is_monitor = forms.CharField(
        initial=2,
        widget=forms.Select(
            choices=(('Yes', 'Yes'), ('No', 'No'),)
        )
    ),

    class Meta:
            model = EntityInfo
            fields = [
                'name', 'introduce',  'website', 'email', 'phone', 'address', 'track_des', 'tune_up_index', 'extra_info', 'is_monitor'
            ]
            error_messages = {
                'name': {
                    'required': '请输入实体名称'
                },
                'threat_level': {
                    'introduce': '请输入实体介绍'
                },
                'cate': {
                    'website': '请输入实体网站信息'
                },
                'eamil': {
                    'required': '请输入实体的邮箱'
                },
                'phone': {
                    'required': '请输入手机号码'
                },
                'address': {
                    'required': '请输入地址'
                },
                'track_des': {
                    'required': '请输入追踪信息'
                },
                'tune_up_index': {
                    'required': '请输选择调证指数'
                },
                'extra_info': {
                    'required': '其他信息'
                },
                'is_monitor': {
                    'required': '监控'
                }
            }

    def __init__(self, request, *args, **kw):
        self.request = request
        super(EntityInfoForm, self).__init__(*args, **kw)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            return self.add_error('name', 'name不能为空')
        return name

    def clean_introduce(self):
        introduce = self.cleaned_data.get('introduce')
        return introduce

    def clean_website(self):
        website = self.cleaned_data.get('website')
        return website

    def clean_eamil(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        return address

    def clean_track_des(self):
        track_des = self.cleaned_data.get('track_des')
        return track_des

    def clean_extra_info(self):
        extra_info = self.cleaned_data.get('extra_info')
        return extra_info

    def clean_is_monitor(self):
        is_monitor = self.cleaned_data.get('is_monitor')
        return is_monitor

    def save(self):
        super(EntityInfoForm, self).save(commit=True)
