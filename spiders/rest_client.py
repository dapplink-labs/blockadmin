import logging
import json
import requests
from urllib.parse import urljoin, unquote
from django.conf import settings


class RestClient:
    def api_post(self, url, data, headers=None, timeout=120):
        if headers is None:
            headers = {}
        if not settings.REST_API:
            url = url
        resp = requests.post(url, data=data, headers=headers, timeout=timeout)
        if resp.status_code == 502:
            msg = '{} response status: {} {}'.format(url, resp.status_code, resp.content)
            raise Exception(msg)
        content = resp.content.decode('utf-8')
        try:
            resp_json = json.loads(content)
            if 'ok' not in resp_json or not resp_json['ok']:
                logging.error("send api_post failed: {}".format(content))
            return resp_json
        except ValueError:
            logging.error("api: {} return {} {}".format(url, resp.status_code, content))
            raise Exception('{} response status: {} {}'.format(url, resp.status_code, content))

    def api_get(self, url, params, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if not settings.REST_API:
            url = url
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        if resp.status_code == 502:
            msg = '{} response status: {} {}'.format(url, resp.status_code, resp.content)
            raise Exception(msg)
        content = resp.content.decode('utf-8')
        try:
            resp_json = json.loads(content)
            return resp_json
        except ValueError:
            logging.error("api: {} return {} {}".format(url, resp.status_code, content))
            raise Exception('{} response status: {} {}'.format(url, resp.status_code, content))

