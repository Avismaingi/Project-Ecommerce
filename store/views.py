from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # For rendering cart logo
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, "store/store.html", context)


def cart(request):
    # if user is signed or anonymous user
    if request.user.is_authenticated:
        customer = request.user.customer
        # This will create object or query one
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # all the order items object with order as parents, refer to attributes of items in terms of order items and
        # for reset use parent class
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # replicating dictionary used if user is not logged in
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)  # Getting data from cart.js
    productId = data['productId']
    action = data['action']
    print('Action ', action)
    print('ProductId ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # because we need to change value of order if it already exists
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'sub':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item quantity was updated', safe=False)
