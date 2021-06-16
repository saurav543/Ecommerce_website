from ecommerce.apps.checkout.views import delivery_address
from django.contrib import messages
from ecommerce.apps.inventory.models import Product
from ecommerce.apps.account.models import Customer,Address
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import RegistrationForm, UserEditForm,UserAddressForm
from .token import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from ecommerce.apps.orders.views import add, user_orders

# Create your views here.

@login_required
def wishList(request):
    product = Product.objects.filter(user_wishlist=request.user)
    return render(request,"account/dashboard/user_wish_list.html",{'wishlist':product})

@login_required
def wish_list(request,id):
    product = get_object_or_404(Product,id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request,'Remove '+product.title+' from your Wishlist. ')
    else:
        product.user_wishlist.add(request.user)
        messages.success(request,'Added '+product.title+' in your Wishlist. ')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
@login_required
def dashboard(request):
    order = user_orders(request)
    return render(request, 'account/dashboard/dashboard.html', {'orders': order})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/dashboard/edit_details.html', {'form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_registration(request):
    if request.method == "POST":
        registerform = RegistrationForm(request.POST)
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password1'])
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('You register successfully now click on send link to activate your account')
    else:
        registerform = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerform})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registraion/activation_invalid.html')

#address
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request,"account/dashboard/addresses.html",{'addresses':addresses})

@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer=request.user
            address_form.save()
            return redirect("account:addresses")
    else:
        address_form = UserAddressForm()
    return render(request,'account/dashboard/edit_addresses.html',{'form':address_form})

@login_required
def edit_address(request,id):
    if request.method == "POST" :
        address = Address.objects.get(pk=id,customer=request.user)
        address_form = UserAddressForm(instance=address,data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return redirect('account:address')
    else:
        address = Address.objects.get(pk=id,customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request,'account/dashboard/edit_addresses.html',{'form':address_form})

@login_required
def delete_address(request,id):
    address = Address.objects.get(pk=id,customer=request.user)
    address.delete()
    return redirect('account:addresses')

@login_required
def set_default(request,id):
    Address.objects.filter(customer=request.user,default=True).update(default=False)
    address = Address.objects.filter(pk=id,customer=request.user).update(default=True)
    previous_url = request.META.get("HTTP_REFERER")
    print(previous_url)
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address") 
    return redirect('account:addresses')
