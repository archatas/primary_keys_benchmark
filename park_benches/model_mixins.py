# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import shortuuid
import string
import random

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


RANDOM_UNIQUE_ID_LENGTH = getattr(settings, "RANDOM_UNIQUE_ID_LENGTH", 12)


def get_new_id():
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return "".join(random.choices(alphabet, k=RANDOM_UNIQUE_ID_LENGTH))
    # return shortuuid.ShortUUID().random(length=RANDOM_UNIQUE_ID_LENGTH)


class RandomUniqueIdMixin(models.Model):
    id = models.CharField(
        _("ID"),
        primary_key=True,
        db_index=True,
        max_length=RANDOM_UNIQUE_ID_LENGTH,
        default=get_new_id,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            # ensure that the id is unique
            while self.__class__.objects.filter(id=self.id).exists():
                self.id = get_new_id()
        # finally save the object
        super(RandomUniqueIdMixin, self).save(*args, **kwargs)