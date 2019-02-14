from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from carts.models import Cart


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "list.html"


class ProductFeaturedDetailSlugView(DetailView):
    model = Product
    template_name = "detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductFeaturedDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        print(context)
        return context