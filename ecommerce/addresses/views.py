from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillinigProfile


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillinigProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get("address_type","shipping")
            instance.billing_profile = billing_profile
            instance.address_type    = address_type
            instance.save()
            request.session[address_type+"_address_id"] = instance.id
        else:
            return redirect("cart:checkout")
        print(request.POST)
        if is_safe_url(redirect_path, request.get_host()):
            print(redirect_path)
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")
    return redirect("cart:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            next_ = request.GET.get("next")
            next_post = request.POST.get("next")
            redirect_path = next_ or next_post or None
            address_id = request.POST.get("address_id")
            address_type = request.POST.get("address_type", "shipping")
            print(address_id)
            billing_profile, billing_profile_created = BillinigProfile.objects.new_or_get(request)
            if billing_profile is not None and address_id is not None:
                qs = Address.objects.filter(id=address_id, billing_profile=billing_profile)
                if qs.exists():
                    print("hello")
                    request.session[address_type + "_address_id"] = address_id
                if is_safe_url(redirect_path, request.get_host()):
                    print(redirect_path)
                    return redirect(redirect_path)
    return redirect("cart:checkout")