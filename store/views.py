from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {
        'products': products
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
    else:
        items = []
        # replicating dictionary used if user is not logged in
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
    context = {
        'items': items,
        'order': order
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
    context = {
        'items': items,
        'order': order
    }
    return render(request, "store/checkout.html", context)


def updateItem(request):
    return JsonResponse('Item was added', safe=False)