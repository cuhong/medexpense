import random
import uuid

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)

from common.models import UUIDPKMixin, TimestampMixin
from medexpense.commons import normalize_cellphone


class UserManager(BaseUserManager):
    def create_user(self, email, name, cellphone=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            cellphone=normalize_cellphone(cellphone),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, cellphone=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            cellphone=cellphone,
            password=password,
            name=name
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, unique=True, primary_key=True, editable=False)
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')
    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='이름')
    cellphone = models.CharField(max_length=15, null=True, blank=True, verbose_name='휴대전화')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return "{}({})".format(self.name, self.email)

    @property
    def is_staff(self):
        return self.is_admin


class Company(UUIDPKMixin, TimestampMixin, models.Model):
    class Meta:
        verbose_name = '회사'
        verbose_name_plural = verbose_name
        ordering = ('name',)

    name = models.CharField(max_length=300, null=False, blank=False, unique=True, verbose_name='회사명')

    def __str__(self):
        return self.name


class Manager(TimestampMixin, models.Model):
    class Meta:
        verbose_name = '아이올 담당자'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    user = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.PROTECT, verbose_name='사용자', related_name='manager_account'
    )


class CompanyUser(TimestampMixin, models.Model):
    class Meta:
        verbose_name = '임직원'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at', 'company')

    company = models.ForeignKey(Company, null=False, blank=False, on_delete=models.PROTECT, verbose_name='회사')
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.PROTECT, verbose_name='사용자')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
