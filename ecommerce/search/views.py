from django.shortcuts import render
from django.views.generic import ListView,DetailView
from products.models import Product
from django.db.models import Q


class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        query = request.GET.get('q')
        print(query)
        if query:
            query = request.GET.get("q")
            return Product.objects.search(query)
        else:
            return Product.objects.features()