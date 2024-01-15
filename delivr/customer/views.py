from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail

from urllib.parse import urlencode
import json

from .models import MenuItem, Category, Order

# Create your views here.
class Index(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,'customer/index.html')
    
class About(View):

    def get(self,request,*args,**kwargs):
        return render(request,'customer/about.html')

class OrderView(View):

    def get(self,request,*args,**kwargs):
        # get every item from each category
        # pass it to context
        # render the template

        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        main_course = MenuItem.objects.filter(category__name__contains='Main Course')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        context = {
            'appetizers': appetizers,
            'main_course': main_course,
            'desserts': desserts,
            'drinks': drinks,
        }

        return render(request, 'customer/order.html', context)
    
    def post(self,request,*args,**kwargs):

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {'id': menu_item.pk, 'name': menu_item.name, 'price': menu_item.price}

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = Order.objects.create(price=price)
        order.items.add(*item_ids)

       

        body = ('Thank you for your order! Your food is being prepared and will be delivered to you soon.\n')

        # send_mail(
        #     'Thank you for your order #{}'.format(order.pk),
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )

        

        return redirect(reverse("address") + '?orderid={}'.format(order.id))
    
class Address(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/address.html')
    
    def post(self, request, *args, **kwargs):

        fname = request.POST['firstname']
        lname = request.POST['lastname']
        address = request.POST['address']

        order_id = request.GET.get('orderid')
        order = Order.objects.get(pk=int(order_id))
        order.name = "{} {}".format(fname,lname)
        order.address = address
        order.save()

        order_items = list(order.items.values('name','price'))

        price = 0
        for item in order_items:
            price += item['price']
 
        context = {
            'order_id': order_id,
            'items': order_items,
            'price': price,
        }

        return render(request, 'customer/order_confirmation.html', context)

