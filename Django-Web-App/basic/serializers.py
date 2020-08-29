from rest_framework import serializers
from .models import CustomUser, Product, ProductDetails,ProductDetailsImages, SupplierType,Supplier, SupplierDetails, Pincode, City, State, Country, Pricing, Cart, Booking, CartItem
from rest_framework_json_api.relations import ResourceRelatedField
from django_filters import rest_framework as filters

class PincodeSerializer(serializers.ModelSerializer):
    city=serializers.PrimaryKeyRelatedField(read_only=False, queryset=City.objects.all())

    class Meta:
        model=Pincode
        fields='__all__'
        depth=1

class CitySerializer(serializers.ModelSerializer):
    state=serializers.PrimaryKeyRelatedField(read_only=False, queryset=State.objects.all())

    class Meta:
        model=City
        fields='__all__'
        depth=1

class StateSerializer(serializers.ModelSerializer):
    country=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Country.objects.all())

    class Meta:
        model=State
        fields='__all__'
        depth=1

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model=Country
        fields='__all__'
        depth=1

class SupplierTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model=SupplierType
        fields='__all__'
        depth =1

class SupplierDetailsSerializer(serializers.ModelSerializer):
    supplier_id=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Supplier.objects.all())
    supplier_name=serializers.SerializerMethodField(read_only=True)
    city=serializers.PrimaryKeyRelatedField(read_only=False, queryset=City.objects.all())
    state=serializers.PrimaryKeyRelatedField(read_only=False, queryset=State.objects.all())
    pincode=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Pincode.objects.all())
    ID=serializers.IntegerField(source='id', read_only=True)


    class Meta:
        model=SupplierDetails
        exclude=['id']
        depth =1

    def get_supplier_name(self, obj):
        return obj.supplier_id.first_name+" "+obj.supplier_id.last_name

#Supplier serialzer uses the supplier details, created_by and supplier
class SupplierSerializer(serializers.ModelSerializer):
    Supplier_Details=SupplierDetailsSerializer(source="supplierdetails_set", many=True, required=False)
    ID=serializers.IntegerField(source='id', read_only=True)
    created_by=serializers.PrimaryKeyRelatedField(read_only=False, queryset=CustomUser.objects.filter(is_staff=True))
    supplier_type=serializers.PrimaryKeyRelatedField(queryset=SupplierType.objects.all(),read_only=False)


    class Meta:
        model=Supplier
        exclude=['id']

    """def get_supplier_type_name(self, obj):
        return obj.supplier_type.supplier_type"""




class ProductDetailsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductDetailsImages
        read_only_fields=['image_type']
        fields='__all__'

#Product Details serializer brings in the data of the supplier, price, image and the product associated with it
class PricingSerializer(serializers.ModelSerializer):
    product_details=serializers.PrimaryKeyRelatedField(read_only=False, queryset=ProductDetails.objects.all())

    class Meta:
        model=Pricing
        fields='__all__'
        depth=1
        read_only_fields=['total_price']

#Product Details serializer brings in the data of the supplier, price, image and the product associated with it
class ProductDetailsSerializer(serializers.ModelSerializer):
    product_id=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Product.objects.all())
    supplier_id=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Supplier.objects.all())
    supplier_name=serializers.CharField(source='supplier_id', read_only=True)
    product_name=serializers.CharField(source='product_id.product_name', read_only=True)
    ID=serializers.IntegerField(source='id', read_only=True)
    price=PricingSerializer(source='pricing_set', many=True, read_only=True)
    img=ProductDetailsImagesSerializer(source='productdetailsimages_set', many=True, read_only=True)

    #supplier name being a serializer method field, we define a function  to get the corresponding supplier name
    #serializer method fields are read only fields
    def get_supplier_name(self, obj):

        name=obj.supplier_id
        return name

    #depth function brings in any of the related fields data to which product details is the foreign key
    class Meta:
        model=ProductDetails
        exclude=['id']
        depth=1


#Product Serializer brings in the Product Details api along with the supplier Name
class ProductSerializer(serializers.ModelSerializer):
    Product_Details=ProductDetailsSerializer(source='productdetails_set', many=True, required=False)
    supplier_name=serializers.CharField(source='productdetails_set.supplier_id', read_only=True)
    ID=serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model=Product
        exclude=['id']

class CartItemSerializer(serializers.ModelSerializer):
    product_details_id=serializers.PrimaryKeyRelatedField(read_only=False, queryset=ProductDetails.objects.all())
    cart_id=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Cart.objects.all())

    class Meta:
        model=CartItem
        fields="__all__"



class CartSerializer(serializers.ModelSerializer):
    cart_items=CartItemSerializer(source='cartitem_set', many=True)
    class Meta:
        model=Cart
        read_only_fields=['cart_items']
        fields="__all__"
