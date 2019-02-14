from django.shortcuts import render,get_object_or_404,Http404,redirect
from django.views.generic import ListView,DetailView
from products.models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def home_view(request):
    print(request.session.get("first_name","Unknown"))
    print(request.session.get("user", "Unknown"))
    context = {
        'object_list': None,
    }
    return render(request,'home.html',context)



'''
def Product_list_view(request):
    object_list = Product.objects.all()
    context = {
        'object_list': object_list,
    }
    return render(request,'list.html',context)


class ProductFeaturedListView(ListView):
    queryset = Product.objects.features()
    template_name = "list.html"


class ProductFeaturedDetailView(DetailView):
    #model = Product
    template_name = "featured_detail.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.features()


class ProductDetailView(DetailView):
    model = Product
    template_name = "detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        print(args)
        print(kwargs)
        return context


def Product_detail_view(request,id=None,*args,**kwargs):
    #object = get_object_or_404(Product,pk=id)
    {This is equivalent code of below block}
    [------
    try:
        object = Product.objects.get(id=id)

    except Product.DoesNotExist:
        raise Http404("Product doesnt exist")
        print("No product here")
    except:
        print("Something error happend")

    query = Product.objects.filter(id=id)
    if query :
        object = query.first()
    else:
        raise Http404("Product doesnt exist")
    -------]
        
    object = Product.objects.get_by_id(id=id)
    if object == None:
        raise Http404("Product doesnt exist")
    print(id)
    print(args)
    print(kwargs)

    context = {
        'object': object,
    }
    print(context)
    return render(request,'detail.html',context)



'''
