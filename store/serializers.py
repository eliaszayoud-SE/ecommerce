from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'image', 'date']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'product_id']


class ItemsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    is_favorite = serializers.SerializerMethodField()
    price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'is_favorite', 'category', 'name', 'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'price_with_discount','discount', 'date']

    def get_is_favorite(self, obj):
        favorite_item_ids = self.context.get('favorite_item_ids', set())
        return obj.id in favorite_item_ids
    
    def get_price_with_discount(self, obj):
        return obj.price - ((obj.price*obj.discount)/100)
        

class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'product_id']

class FavoriteItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'category_id', 'name', 'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'discount', 'date']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'product_id', 'qty']

class CartViewSerializer(serializers.ModelSerializer):
    product = ItemsSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'qty', 'product', 'total_price']

    def get_total_price(self, cart):
        return cart.qty * (cart.product.price - ((cart.product.price*cart.product.discount)/100))

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user_id', 'name', 'city', 'street', 'phone', 'lat', 'long']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'name', 'count', 'discount', 'expire_date']  


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'address', 'type', 'price_delivery', 'price', 'payment_type', 'coupon_id', 'status', 'date_time', 'total_price', 'rating', 'note']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'title', 'body', 'date_time']


class SimpleItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'name_ar']


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = SimpleItemsSerializer()
    class Meta:
        model = Cart
        fields = ['id', 'qty', 'product', 'unit_price']


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'title', 'body']


class CustomItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'active' ,'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'discount', 'date']
