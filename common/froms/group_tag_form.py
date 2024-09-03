#encoding=utf-8

import ast
import json
import logging
from django import forms
from common.models import GroupInfo, GroupTag,  EntityInfo


class GroupTagForm(forms.ModelForm):
    entity = forms.CharField(required=True)
    g_tag = forms.CharField(required=True)
    g_threat_level = forms.IntegerField(
        initial=6,
        widget=forms.Select(
            choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
        ),
        required=False
    )
    g_cate = forms.CharField(
        initial=6,
        widget=forms.Select(
            choices=(
                ('exchange', 'exchange'),
                ('service', 'service'),
                ('pool', 'pool'),
                ('gambling', 'gambling'),
                ('market', 'market'),
                ('contract', 'contract'),
                ('special', 'special'),
                ('other', 'other')
            )
        ),
        required=False
    )

    class Meta:
        model = GroupTag
        fields = [
            'entity',
            'g_tag',
            'g_cate',
        ]
        error_messages = {
            'entity': {
                'required': 'entity不能为空'
            },
            'g_tag': {
                'required': '请输入标签'
            },
            'g_cate': {
                'required': '请输入cate'
            }
        }

    def __init__(self, request, *args, **kw):
        self.request = request
        super(GroupTagForm, self).__init__(*args, **kw)

    def clean_entity(self):
        entity = self.cleaned_data.get('entity')
        entity_ = EntityInfo.objects.filter(name=entity).order_by("-id").first()
        return entity_

    def clean_g_tag(self):
        g_tag = self.cleaned_data.get('g_tag')
        if g_tag in ['', None]:
            return self.add_error('g_tag', 'g_tag不能为空')
        return g_tag

    def clean_g_cate(self):
        g_cate = self.cleaned_data.get('g_cate')
        return g_cate

    def save(self):
        super(GroupTagForm, self).save(commit=True)