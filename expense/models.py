from django.contrib.auth import get_user_model
from django.db import models
from sequences import get_next_value

from account.models import Company
from common.models import UUIDPKMixin, TimestampMixin, ProtectedFile

User = get_user_model()


class MedExpenseRelation(models.Model):
    class Meta:
        verbose_name = '진료비 지급 대상'
        verbose_name_plural = verbose_name
        ordering = ('company', 'name')
        unique_together = ('company', 'name')

    company = models.ForeignKey(Company, null=False, blank=False, on_delete=models.PROTECT, verbose_name='회사')
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name='대상명')

    def __str__(self):
        return self.name


class MedExpenseType(models.Model):
    class Meta:
        verbose_name = '진료비 타입'
        verbose_name_plural = verbose_name
        ordering = ('company', 'name')
        unique_together = ('company', 'name')

    company = models.ForeignKey(Company, null=False, blank=False, on_delete=models.PROTECT, verbose_name='회사')
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name='타입명')

    def __str__(self):
        return self.name


class Claim(UUIDPKMixin, TimestampMixin, models.Model):
    class Meta:
        verbose_name = '진료비 청구'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    CLAIM_STATUS = (
        (0, '기타'),
        (1, '작성중'),
        (2, '접수'),
        (3, '처리중'),
        (4, '처리완료')
    )
    serial = models.CharField(max_length=50, null=True, blank=True, verbose_name='일련번호', editable=False)
    status = models.IntegerField(choices=CLAIM_STATUS, default=1, null=False, blank=False, verbose_name='상태')
    user = models.ForeignKey(
        User, null=False, blank=False, verbose_name='임직원', on_delete=models.PROTECT, related_name='company_user'
    )
    manager = models.ForeignKey(
        User, null=True, blank=True, verbose_name='담당자', on_delete=models.PROTECT, related_name='manager'
    )
    relation = models.ForeignKey(MedExpenseRelation, null=False, blank=False, verbose_name='청구인과의 관계',
                                 on_delete=models.PROTECT)
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='청구대상 성명')

    def set_serial(self):
        if self.serial:
            return None
        dt = self.registered_at.strftime('%Y%m%d')
        sequence = get_next_value(dt)
        serial = f"{dt}-{str(sequence).zfill(5)}"
        self.serial = serial
        self.save()


class Expense(UUIDPKMixin, TimestampMixin, models.Model):
    class Meta:
        verbose_name = '진료비'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    CLAIM_STATUS = (
        (0, '기타'),
        (1, '접수'),
        (2, '심사중'),
        (3, '승인'),
        (4, '보정요청'),
        (5, '반려')
    )
    serial = models.CharField(max_length=50, null=True, blank=True, verbose_name='일련번호', editable=False)
    status = models.IntegerField(choices=CLAIM_STATUS, default=1, null=False, blank=False, verbose_name='상태')
    claim = models.ForeignKey(Claim, null=False, blank=False, verbose_name='청구', on_delete=models.PROTECT)
    expense_type = models.ForeignKey(MedExpenseType, null=False, blank=False, verbose_name='진료비타입',
                                     on_delete=models.PROTECT)
    org_name = models.CharField(max_length=512, null=False, blank=False, verbose_name='의료기관명')
    expense_amount = models.PositiveBigIntegerField(null=False, blank=False, verbose_name='진료비총액')
    expense_file = models.OneToOneField(ProtectedFile, null=False, blank=False, verbose_name='진료비파일',
                                        on_delete=models.PROTECT)

    def set_serial(self):
        if self.serial:
            return None
        claim_serial = self.claim.serial
        sequence = get_next_value(claim_serial)
        serial = f"{claim_serial}-{str(sequence).zfill(3)}"
        self.serial = serial
        self.save()
