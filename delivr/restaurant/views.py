from django.shortcuts import render
from django.views import View
from django.utils.timezone import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from customer.models import Order


# Create your views here.

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # get current date
        # loop through orders and add price value
        # pass total number of orders and total revenue into template

        today = datetime.today()
        orders = Order.objects.filter(created__year=today.year, created__month=today.month, created__day=today.day)

        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders),
        }

        return render(request, 'restaurant/dashboard.html', context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
