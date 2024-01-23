from django.db import models
import uuid

class KaayaProduct(models.Model):
    CLASSIFICATION_CHOICES = [
        ('NORMAL', 'Normal'),
        ('TEMP_HIDDEN', 'Temporialy Hidden'),
        ('COMING_SOON', 'Comming Soon'),
        ('OUT_OF_STOCK', 'Out Of Stock'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ean = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.JSONField()
    qty = models.FloatField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    mop = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    images = models.JSONField()
    gallery = models.JSONField()
    slug = models.CharField(max_length=255, blank=True, null=True)
    HSNDetails = models.JSONField()
    
    # classification contains "TEMP_HIDDEN", "COMING SOON", "OUT_OF_STOCK", "NORMAL"
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default="NORMAL")
    
    # size values can be :
    # "XS","XS/S","S","S/M","M","M/L","L","L/XL","XL","5XL","30","36","Onesize","0.5","1","2","2.1","2.2","2.25","2.3","2.4","2.5","2.6","2.8","2.9","3","3.5","4","4.5","5","5.5","6","6.5","7","7.5","8","8.5","9","9.5","10","11","12","13","14","15","16","16.5","17","17.5","18","19","20","21","22","23","25","27","12\"X12\"","Pack","300-320 ML","400 ML & Above","1inch","FREESIZE","ONESIZE"
    size = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        managed = True
        db_table = 'tbl_kaaya_products'
