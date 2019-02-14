from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from .forms import SignUpForm,GuestForm
from django.contrib.auth.models import User
from .models import GuestEmail


def guest_register_view(request):
    form    = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email   = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            print("Safe URL")
            print(redirect_path)
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")


def get_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:

        next_=request.GET.get("next")
        next_post = request.POST.get("next")
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            redirect_path = next_ or next_post or None
            if username and password:
                auth = authenticate(request, username=username, password=password)
                if auth is not None:
                    login(request, auth)
                    try:
                        del request.session['guest_email_id']
                    except:
                        pass
                    print(redirect_path)
                    if is_safe_url(redirect_path,request.get_host()):
                        print("Safe URL")
                        print(redirect_path)
                        return redirect(redirect_path)
                    else:
                        return redirect("home")
                else:
                    return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


def get_register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username    = request.POST.get("username")
            email       = username = request.POST.get("email")
            password1    = request.POST.get("password1")
            password2    = request.POST.get("password2")
            if username and email and password1 and password2 and password1==password2:
                user = User.objects.create_user(username,email,password1)
                login(request, user)
                print(user)
                return redirect("home")
            else:
                return render(request, "accounts/register.html")
    return render(request, "accounts/register.html")


@login_required
def get_logout(request):
    logout(request)
    return redirect("login")
