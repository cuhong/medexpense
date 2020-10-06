import uuid

from django.db import models


class UUIDPKMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        null=False, blank=False, default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False
    )


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='최종 수정일자')


class ProtectedFile(UUIDPKMixin, models.Model):
    class Meta:
        verbose_name = '보안 파일'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')
    file = models.FileField(null=False, blank=False, verbose_name='파일')


class OpenFile(UUIDPKMixin, models.Model):
    class Meta:
        verbose_name = '일반 파일'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')
    file = models.FileField(null=False, blank=False, verbose_name='파일')
