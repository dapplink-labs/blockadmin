import logging
from django.db import models, transaction
from common.base_model import BaseModel
from django.contrib.postgres.fields import JSONField


SPIDERED_STATUS_CHOICES = [(x, x) for x in ['UnCrawl', 'Crawled']]


class SpiderUrlManager(models.Manager):
    def create_spider_url(self, name, comment, url_list, status):
        for url in url_list:
            spu = self.filter(url=url).first()
            if spu is None:
                create_url = self.create(
                    name=name,
                    url=url.get("url", ""),
                    comment=comment,
                    records=url.get("records", 0),
                    status=status
                )
                logging.info("create %s success", create_url)
            else:
                logging.info("%s is exist", url)
                continue


class SpiderUrl(BaseModel):
    name = models.CharField(max_length=500, default="")
    url = models.CharField(max_length=500, default="", unique=True)
    comment = models.CharField(max_length=200, default="")
    records = models.IntegerField(default=0)
    status = models.CharField(max_length=16, choices=SPIDERED_STATUS_CHOICES, default="UnCrawl")
    info = JSONField(default=dict)
    objects = SpiderUrlManager()

    class Meta:
        pass

    def __str__(self) -> str:
        return "{}:{} {}".format(self.name, self.url, self.status)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'status': self.status,
            'info': self.info,
        }


