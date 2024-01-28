from django.db import models
from kaaya_login.models import TblKaayaLogin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from kaaya_products.models import KaayaProduct
from django.utils import timezone

def lenth_of_phone_mobile(value):
    if len(value) != 10:
        raise ValidationError("Field length should be 10")
    
class TblKaayaUserDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(TblKaayaLogin, models.DO_NOTHING)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^[a-zA-Z0-9 ]*$',
        message='First name must be alphanumeric only.',
        code='invalid_first_name'
    )])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(
        regex='^[a-zA-Z0-9 ]*$',
        message='Last name must be alphanumeric only.',
        code='invalid_last_name'
    )])

    phone = models.CharField(max_length=12, validators=[RegexValidator(
        regex='^[0-9]*$',
        message='Phone must be numeric only.',
        code='invalid_last_name'
    ), lenth_of_phone_mobile])

    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_kaaya_user_details'
        
        
class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(KaayaProduct, on_delete=models.CASCADE)
    qty = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(TblKaayaUserDetails, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = 'tbl_kaaya_cart_details'
        

class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, verbose_name="Customer Name", validators=[RegexValidator(
        regex='^[a-zA-Z]+(?: [a-zA-Z]+)*$',
        message='Customer Name must be alphanumeric only.',
        code='invalid_first_name'
    )])
    phone = models.CharField(max_length=15, verbose_name="Phone", validators=[RegexValidator(
        regex='^[0-9]*$',
        message='Phone must be numeric only.',
        code='invalid_last_name'
    ), lenth_of_phone_mobile])
    user = models.ForeignKey('TblKaayaUserDetails', on_delete=models.CASCADE, verbose_name="User")
    address_line1 = models.CharField(max_length=255, verbose_name="Address Line 1")
    city = models.CharField(max_length=100, verbose_name="City")
    zip_code = models.CharField(max_length=20, verbose_name="ZIP Code")
    state = models.CharField(max_length=100, verbose_name="State")
    country = models.CharField(max_length=100, default="India", verbose_name="Country")
    landmark = models.CharField(max_length=255, blank=True, null=True, verbose_name="Landmark")
    is_default = models.BooleanField(default=False, verbose_name="Is Default")

    class Meta:
        verbose_name_plural = "Addresses"
        managed = True
        db_table = 'tbl_kaaya_user_address_details'