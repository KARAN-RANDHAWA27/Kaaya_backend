from django.db import models
from kaaya_login.models import TblKaayaLogin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def lenth_of_phone_mobile(value):
    if len(value) != 10:
        raise ValidationError("Field length should be 10")
    
class TblKaayaUserDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(TblKaayaLogin, models.DO_NOTHING)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^[a-zA-Z0-9]*$',
        message='First name must be alphanumeric only.',
        code='invalid_first_name'
    )])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^[a-zA-Z0-9]*$',
        message='Last name must be alphanumeric only.',
        code='invalid_last_name'
    )])

    phone = models.CharField(max_length=12, validators=[RegexValidator(
        regex='^[0-9]*$',
        message='Phone must be numeric only.',
        code='invalid_last_name'
    ), lenth_of_phone_mobile])

    created_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_kaaya_user_details'