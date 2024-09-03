#encoding=utf-8

import ast
import json
import logging
from django import forms
from common.models import AddressTag, EntityInfo
from django.forms import widgets


class BlockTagDataForm(forms.ModelForm):
    entity = forms.CharField(required=False, max_length=512)
    tag = forms.CharField(required=True)
    threat_level = forms.IntegerField(
        initial=6,
        widget=forms.Select(
            choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
        )
    )
    cate = forms.CharField(
        initial=6,
        widget=forms.Select(
            choices=(('exchange', 'exchange'), ('service', 'service'), ('pool', 'pool'), ('gambling', 'gambling'), ('market', 'market'), ('contract', 'contract'), ('hacker', 'hacker'), ('dex', 'dex'), ('other', 'other'))
        )
    )
    tag_we = forms.CharField(required=False)
    comment = forms.CharField(max_length=512, required=False)
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

    class Meta:
        model = AddressTag
        fields = [
            'entity', 'tag', 'threat_level',  'cate', 'tag_we', 'comment', 'is_commit', 'is_checked'
        ]
        error_messages = {
            'tag': {
                'required': '请输入标签'
            },
            'threat_level': {
                'required': '请选择风险级别'
            },
            'cate': {
                'required': '请输入cate'
            },
            'comment': {
                'required': '请输入备注'
            },
            'is_commit': {
                'required': '请选择是否提交'
            },
            'is_checked': {
                'required': '请选择是否审核'
            },
        }

    def __init__(self, request, *args, **kw):
        self.request = request
        super(BlockTagDataForm, self).__init__(*args, **kw)

    def clean_entity(self):
        entity = self.cleaned_data.get('entity')
        entity_ = EntityInfo.objects.filter(name=entity).order_by("-id").first()
        print("entity_=", entity_)
        if entity_ is not None:
            return entity_
        else:
            return None

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
        if tag in ['', None]:
            return self.add_error('tag', 'tag不能为空')
        return tag.lower()

    def clean_threat_level(self):
        threat_level = self.cleaned_data.get('threat_level')
        return threat_level

    def clean_cate(self):
        cate = self.cleaned_data.get('cate')
        return cate

    def clean_tag_we(self):
        tag_we = self.cleaned_data.get('tag_we')
        return tag_we

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        return comment

    def clean_is_commit(self):
        is_commit = self.cleaned_data.get('is_commit')
        return is_commit

    def clean_is_checked(self):
        is_checked = self.cleaned_data.get('is_checked')
        if is_checked in ['', None]:
            return self.add_error('is_checked', '需要选择 is_checked')
        return is_checked

    def save(self):
        super(BlockTagDataForm, self).save(commit=True)
