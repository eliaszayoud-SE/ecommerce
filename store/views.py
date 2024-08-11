from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from .models import *
from .serializers import *
from .notification import send_notification
from django.db.models import Count
from django.db.models import Sum
from .permissions import IsDeliveryUser

@api_view(['GET'])
def home_data(request):
    categories = Category.objects.all()
    cartegory_serializer = CategorySerializer(categories, many=True)

    top_selling_products = Cart.objects \
        .values('product_id') \
        .annotate(total_qty_sold=Sum('qty')) \
        .order_by('-total_qty_sold')[:10]
        
    top_selling_product_ids = [item['product_id'] for item in top_selling_products]


    items = Item.objects.filter(id__in=top_selling_product_ids)

    item_serializer = ItemsSerializer(items, many=True)

    settings = Settings.objects.all().order_by('-id').first()

    settings_serializer = SettingsSerializer(settings)

    data = {}
    data['categories'] = cartegory_serializer.data
    data['items'] = item_serializer.data
    data['settings'] = settings_serializer.data

    return Response(data)



class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ItemsViewSet(ListModelMixin, GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.request.query_params.get('categoryId')
        return Item.objects.filter(category_id=category_id).all()
    
    def get_serializer_context(self):
        favorite_item_ids = set()
        print(self.request.user)
        if self.request.user.is_authenticated:

            favorite_item_ids = set(Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True))

        return {
            'favorite_item_ids':favorite_item_ids
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'items':serializer.data})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    user_id = request.user.id
    product_id = request.data['product_id']

    favorite = Favorite.objects.filter(user_id=user_id, product_id=product_id)
    if not favorite.exists():
        favorite = Favorite.objects.create(user_id=user_id, product_id=product_id)

    else :
        favorite = favorite.first()

    favorite_serializer = FavoriteSerializer(favorite)
    return Response(favorite_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request):
    user_id = request.user.id
    product_id = request.data['product_id']

    
    favorite = Favorite.objects.filter(user_id=user_id, product_id=product_id)
    favorite.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite(request):
    user_id = request.user.id
    favorite = set(Favorite.objects.filter(user_id=user_id).values_list('product_id',flat=True))

    items = Item.objects.filter(id__in=favorite)
    serializer = FavoriteItemSerializer(items, many=True)
    print(serializer.data)
    return Response({'items':serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user_id = request.user.id
    product_id = request.data['product_id']


    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id, order_id=None)
        cart.qty += 1
        cart.save()
    except:
        cart = Cart.objects.create(user_id=user_id, product_id=product_id)
        
    cart_serializer = CartSerializer(cart)
    return Response(cart_serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_cart(request):
    user_id = request.user.id
    product_id = request.data['product_id']


    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id, order_id=None)
        if(cart.qty> 0):
            cart.qty -= 1
            if(cart.qty==0):
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                cart.save()
                cart_serializer = CartSerializer(cart)
                return Response(cart_serializer.data)

        
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No product with the given id'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])      
def get_count_cart(request):
    user_id = request.user.id
    product_id = request.query_params.get('productId')   

    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id, order_id=None)
        return Response({'qty':cart.qty})
        

    except:
        return Response({'qty':0})

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def view_cart(request):
    user_id = request.user.id
    cart =  Cart.objects.select_related('product__category').filter(user_id=user_id, order_id=None)
    
    cart_serializer = CartViewSerializer(cart, many=True)
    total_price = sum([cart['total_price'] for cart in cart_serializer.data])
    total_quantity = sum([cart['qty'] for cart in cart_serializer.data])
    return Response({
            'cart':cart_serializer.data,
            'total_quantity':total_quantity,
            'total_price':total_price
        })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])     
def search(request):
    search = request.query_params.get('search')
    print(search)
    item = Item.objects.filter(Q(name__icontains=search)|Q(name_ar__icontains=search))
    item_serializer = ItemsSerializer(item, many=True)
    return Response({'items':item_serializer.data})

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def add_address(request):
    user_id = request.user.id
    city = request.data['city']
    name = request.data['name']
    street = request.data['street']
    lat = request.data['lat']
    print(type(lat))
    long = request.data['long']
    phone = request.data['phone']

    address = Address.objects.create(
        user_id=user_id,
        city=city,
        name = name,
        street=street,
        lat=lat,
        long=long,
        phone=phone
    )

    address_serializer = AddressSerializer(address)
    return Response(address_serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address(request):
    user_id = request.user.id
    address_id = request.data['address_id']

    try:
        address = Address.objects.get(id=address_id,user_id=user_id)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No address with the given id'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_address(request):
    user_id = request.user.id
    address = Address.objects.filter(user_id=user_id)
    address_serializer = AddressSerializer(address, many=True)
    return Response({'address':address_serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_coupon(request):
    coupon_name = request.query_params.get('coupon_name')
    try:
        coupon = Coupon.objects.get(name=coupon_name, expire_date__gt=datetime.now(), count__gt=0)
        coupon_serializer = CouponSerializer(coupon)
        return Response(coupon_serializer.data)
       
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No Coupon with the given name'
        })
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    user_id = request.user.id
    address_id = request.data.get('address_id')
    type = request.data.get('type')
    price_delivery = float(request.data.get('price_delivery'))
    price = float(request.data.get('price'))
    payment_type = request.data['payment_type']
    coupon_id = request.data.get('coupon_id') 
    discount_price = float(request.data.get('discount_price'))

    if type == '1':
        price_delivery = 0

    total_price = price + price_delivery

    coupon = Coupon.objects.filter(id=coupon_id, expire_date__gt=datetime.now(), count__gt=0)


    if coupon_id == '0' or not coupon.exists():
        coupon_id = None

    else :
        
        total_price = total_price - (price * discount_price / 100)   
        print(total_price)
        coupon = coupon.first()
        if(coupon.count > 0):
            coupon.count -= 1
            coupon.save() 


    if address_id == "0":
        address_id = None    

    try:
        order = Order.objects.create(user_id=user_id, price_delivery=price_delivery,address_id=address_id, type=type, price=price, payment_type=payment_type, coupon_id=coupon_id, total_price=total_price)

        carts_update_list = []

        carts = Cart.objects.filter(user_id=user_id, order_id=None)
        
        for cart in carts :
            cart.unit_price  = cart.product.price
            cart.order_id = order.id
            carts_update_list.append(cart)
        
        Cart.objects.bulk_update(carts_update_list, ['unit_price', 'order_id'])

        # Cart.objects.filter(user_id=user_id, order_id=None).update(order_id=order.id)
    
        return Response(status=status.HTTP_204_NO_CONTENT)

    except :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_pending_order(request):
    user_id = request.user.id
    order = Order.objects.filter(user_id=user_id, status__lt=3)
    order_serializer = OrderSerializer(order, many=True)

    return Response({'order':order_serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_archive_order(request):
    user_id = request.user.id
    order = Order.objects.filter(user_id=user_id, status=3)
    order_serializer = OrderSerializer(order, many=True)

    return Response({'order':order_serializer.data})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def approved_order(request):
    user_id = request.data['user_id']
    order_id = request.data['order_id']

    try:
        order = Order.objects.get(id=order_id, status=0)
        order.status = 1
        order.save()
        send_notification('success', 'The order has been Approved', topic=f'users{user_id}', pageid='', pagename='refreshorderpending')
        Notification.objects.create(user_id=user_id, title='success', body='The order has been Approved')
        return Response({'success':'The Notification is send'})
    
    except :
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No order with the given id'
        }) 

@api_view(['POST'])
@permission_classes([IsAdminUser])
def order_prepared(request):
    user_id = request.data['user_id']
    order_id = request.data['order_id']
    order_type = request.data['order_type']

    try:
        order = Order.objects.get(id=order_id, status=1)
        if order_type == 0:       
            order.status = 2
            order.save()
            send_notification('success', 'The order has been prepare', topic=f'users{user_id}', pageid='', pagename='refreshorderpending')
            send_notification('warning', 'there is orders awating approval', 'delivery', '', 'refreshorderpending')
        
        else :
            order.status = 4
            order.save()
            send_notification('success', 'The order has been deliverd', topic=f'users{user_id}', pageid='', pagename='refreshorderpending')

        return Response({'success':'The Notification is send'})
    
    except Exception as error :
        print(error)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No order with the given id'
        }) 
    
@api_view(['POST'])
@permission_classes([IsDeliveryUser])
def order_approved_by_delivery(request):
    user_id = request.data['user_id']
    order_id = request.data['order_id']

    try:
        order = Order.objects.get(id=order_id, status=2)
        order.status = 3
        order.delivery = request.user.id
        order.save()
        send_notification('success', 'The order is on the way', topic=f'users{user_id}', pageid='', pagename='refreshorderpending')
        send_notification('warning', f'The order has been Approved by delivery {request.user.username}', 'delivery', '', 'refreshorderpending')
        send_notification('warning', 'The order has been Approved by delivery', 'services', '', '')
        return Response({'success':'The Notification is send'})
    
    except Exception as error :
        print(error)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No order with the given id'
        })   

@api_view(['POST'])
@permission_classes([IsDeliveryUser])  
def order_delivery(request):
    user_id = request.data['user_id']
    order_id = request.data['order_id']

    try:
        order = Order.objects.get(id=order_id, status=3)
        order.status = 4
        order.save()
        send_notification('success', 'The order has been deliverd', topic=f'users{user_id}', pageid='', pagename='refreshorderpending')
        send_notification('warning', 'The order has been deliverd to The customer', 'services', '', '')
        return Response({'success':'The Notification is send'})
    
    except :
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No order with the given id'
        })  
    


@api_view(['GET'])
@permission_classes([IsDeliveryUser]) 
def view_bending_order_for_delivery(request):
    order = Order.objects.filter(status=2)
    order_serializer = OrderSerializer(order, many=True)
    return Response({'order':order_serializer.data})


@api_view(['GET'])
@permission_classes([IsDeliveryUser]) 
def view_accepted_order_for_delivery(request):
    user_id = request.user.id
    order = Order.objects.filter(status=3, user_id=user_id)
    order_serializer = OrderSerializer(order, many=True)
    return Response({'order':order_serializer.data})



@api_view(['GET'])
@permission_classes([IsDeliveryUser]) 
def view_archive_order_for_delivery(request):
    user_id = request.user.id
    order = Order.objects.filter(status=4, delivery= user_id)
    order_serializer = OrderSerializer(order, many=True)
    return Response({'order':order_serializer.data})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def view_order_for_admin(request):
    order = Order.objects.filter(status__lt=4)
    order_serializer = OrderSerializer(order, many=True)
    return Response({'order':order_serializer.data})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def view_archive_order_for_admin(request):
    order = Order.objects.filter(status=4)
    order_serializer = OrderSerializer(order, many=True)
    return Response({'order':order_serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_notification(request):
    user_id = request.user.id
    notification = Notification.objects.filter(user_id=user_id).order_by('id')
    notification_serializer = NotificationSerializer(notification, many=True)
    return Response({'notification':notification_serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_details(request):
    order_id = request.query_params.get('order_id')
    order_details = Cart.objects.filter(order_id=order_id)
    if order_details.exists():
        order_details_serializer = OrderDetailsSerializer(order_details, many=True)
        return Response({'order_details':order_details_serializer.data})
    
    return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No orderDetails with the given id'
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request):
    
    user_id = request.user.id
    order_id = request.data['order_id']

    try:
        order = Order.objects.get(id=order_id, user_id=user_id)
        if order.status > 0:
              return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'error':'you can not delete this order'
                 })
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No Order with the given id'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offers_item(request):
    items = Item.objects.exclude(discount=0)
    item_serializer = ItemsSerializer(items, many=True)
    return Response({'items':item_serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_rating_to_archive_order(request):
    user_id = request.user.id
    order_id = request.data['order_id']
    rating = request.data['rating']
    note = request.data['note']

    try:
        order = Order.objects.get(user_id=user_id, id=order_id, status=3)
        if order.rating is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'error':'You can not edit the rating'
        }) 

        order.rating = rating
        order.note = note
        order.save()

        
        return Response()

    except Exception as error:
        print(error)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No Order with the given id'
        })   

@api_view(['GET'])
def notification_test(request):
    send_notification(title='Hi', message='Hi from fierbase', topic='users', pageid='', pagename='')
    return Response({'send':'send success'})