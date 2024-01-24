from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class TblKaayaLogin(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    username = models.EmailField(
        unique=True, error_messages={'unique': "Email address already exists."}, max_length=50)
    password = models.CharField(
        max_length=100, blank=True, null=True)
    usertype = models.PositiveSmallIntegerField(blank=True, null=True)
    email_verification_start_time = models.DateTimeField(blank=True, null=True)
    is_email_verified = models.BooleanField(blank=True, null=True)
    is_phone_verified = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField()
    modified_date = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id']

    class Meta:
        managed = True
        db_table = 'tbl_kaaya_login'
