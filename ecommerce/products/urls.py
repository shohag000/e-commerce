from django.urls import path,re_path
from .views import (ProductListView,
                    ProductFeaturedDetailSlugView)
'''from ecommerce.views import (Product_list_view,
                             Product_detail_view,
                             ProductDetailView,
                             ProductFeaturedListView,
                             ProductFeaturedDetailView)'''

urlpatterns = [
    path('',ProductListView.as_view(),name='list'),
    re_path(r'^(?P<slug>[\w-]+)/$',ProductFeaturedDetailSlugView.as_view(),name='details'),

    ]

'''
path('products-fbv/',Product_list_view),
path('products/<int:pk>/',ProductDetailView.as_view()),
path('products-fbv/<int:id>/', Product_detail_view),
path('featured/',ProductFeaturedListView.as_view()),
path('featured/<int:pk>/',ProductFeaturedDetailView.as_view()),
'''