from django.shortcuts import render,redirect
from carts.models import Cart
from products.models import Product
from orders.models import Order
from billing.models import BillinigProfile
from accounts.forms import GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        "cart_obj" : cart_obj,
        "new_obj" : new_obj,
    }
    return render(request, 'carts/home.html', context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.all().count()

    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.all().count()==0:
        return redirect("cart:home")
    guest_form  = GuestForm()
    address_form = AddressForm()
    billing_profile , billing_profile_created = BillinigProfile.objects.new_or_get(request)
    shipping_address_id = request.session.get('shipping_address_id',None)
    billing_address_id = request.session.get('billing_address_id', None)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj , order_obj_created  = Order.objects.new_or_get(billing_profile,cart_obj)
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()
        # Test code
        #test_billing_address = Address.objects.filter(billing_profile=billing_profile,address_type="billing")
        #test_shipping_address = Address.objects.filter(billing_profile=billing_profile, address_type="shipping")


    if request.method == "POST" :   # To finalize checkout
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            del request.session['cart_items']
            return redirect("cart:success")



    context = {
        "object" : order_obj,
        "billing_profile":billing_profile,
        "guest_form":guest_form,
        "address_form": address_form,
        #"test_billing_address": test_billing_address,
        #"test_shipping_address": test_shipping_address,
        "address_qs" : address_qs,

    }
    return render(request,"carts/checkout.html",context)


def checkout_done_view(request):
    return render(request,"carts/checkout-done.html",{})