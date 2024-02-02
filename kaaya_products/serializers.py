from rest_framework import serializers
from .models import KaayaProduct,KaayaaProductsCategory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = KaayaProduct
        fields = ['id','ean','title','description','qty','mrp','mop','category','brand','color','images','gallery','slug',
                  'HSNDetails','is_approved','approved_by','approved_date','classification','size']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KaayaaProductsCategory
        fields = ['id','category_name','is_approved','approved_by','approved_date','is_deleted']
