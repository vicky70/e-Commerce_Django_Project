import datetime
from time import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Comic, Publisher, Reviews, CustomerDetail, Order, Cart, Rental_system
from .forms import AuthenticateForms, RegistrationForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.conf import settings
from django.urls import reverse
import uuid

from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.

# ()

# Landing page
def home(request):
    return render(request, 'core/base.html')

# Comic List page
def show_comic_list(request):
    cate_comics = Comic.objects.all()
    if cate_comics:
        return render(request, 'core/comic_list.html', {'cate_comics': cate_comics})
    else:
        return render(request, 'core/notFound.html')
    
# Comic Detail Page
def show_comic_details(request, id):
    comic_details = Comic.objects.get(id=id)
    # publisher_details = Publisher.objects.get(published_comic=id)
    get_reviews = Reviews.objects.filter(reviews_on_comic=id)
    return render(request, 'core/comic_detail.html', {'comic_details':comic_details, 'user_reviwes':get_reviews})

# Authorization and Authentications

def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST': 
            user_credential_fields = AuthenticateForms(request,request.POST)
            if user_credential_fields.is_valid():
                name = user_credential_fields.cleaned_data['username']
                password = user_credential_fields.cleaned_data['password']
                user = authenticate(username=name, password=password)
                if user is not None:
                    messages.success(request, 'Log in success...')
                    login(request, user)
                    return redirect('/')
        else:
            user_credential_fields = AuthenticateForms()
        return render(request,'core/login_page.html',{'user_credential_fields':user_credential_fields})
    else:
        return redirect('home')
    
def registration_form(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            usr_reg_form = RegistrationForm(request.POST)
            if usr_reg_form.is_valid():
                usr_reg_form.save()
                messages.success(request,'Registration Successfull !!')
                return redirect('home')
        else:
            usr_reg_form  = RegistrationForm()
        return render(request,'core/sign_up.html',{'usr_reg_form':usr_reg_form})
    else:
        return redirect('home')

# /Log Out
def log_out(request):
    messages.info(request, 'Log out...')
    logout(request)
    return redirect('home')

# address form
def address(request):
    if request.method == 'POST':
            af =CustomerForm(request.POST)
            if af.is_valid():
                user=request.user
                name= af.cleaned_data['name']
                address= af.cleaned_data['address']
                city= af.cleaned_data['city']
                state= af.cleaned_data['state']
                pincode= af.cleaned_data['pincode']
                CustomerDetail(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                messages.success(request, 'New Address Added...')
                return redirect('instant_buy')
    else:
        af = CustomerForm()
    return render(request,'core/address.html',{'af':af})


def edit_address(request, id):
    if request.method == 'POST':
        address = CustomerDetail.objects.get(pk=id)
        af = CustomerForm(request.POST, instance=address)
        if af.is_valid():
            af.save()
            messages.success(request, 'Address Updated...')
            return redirect('ready_to_pay')
    address = CustomerDetail.objects.get(pk=id)
    af = CustomerForm(instance=address)
    return render(request, 'core/address_page.html', {'af':af})


def delete_address(request, id):
    de = CustomerDetail.objects.get(pk=id)
    de.delete()
    messages.success(request, 'Address Deleted...')
    return redirect('ready_to_pay')


# purchase --- add to cart --- and rent system start here
def instant_buy(request, id):
    if request.user.is_authenticated:
        comic = Comic.objects.get(pk=id)
        total = comic.discounted_price
        print(total)
        final_price = 2000 + total
        print('final_price = ', final_price)
        address = CustomerDetail.objects.filter(user=request.user)
        return render(request, 'core/checkout.html', {'item': comic, 'is_single_product': True,'total':total,'final_price':final_price,'address':address})
    else:
        return redirect('login_page')
    
def instant_buy_payment(request, comic_id):
    add_id=-1
    if request.method == 'POST':
        add_id = request.POST.get('selected_address')

    if not add_id:
        messages.success(request, 'No Address Selected Please select an Address')
        return redirect('buy_comic', comic_id)
    print('selected address id = ', add_id)
    comic = Comic.objects.get(pk=comic_id)
    delivery_charge =2000
    final_price= delivery_charge + comic.discounted_price
    address = CustomerDetail.objects.filter(user=request.user)
    host = request.get_host() 
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Comic',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('instant_buy_payment_success', args=[add_id, comic_id])}",
        'cancel_url': f"http://{host}{reverse('payment_fail')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    return render(request, 'core/payment.html', {'final_price':final_price,'address':address,'comic':comic,'paypal':paypal_payment})

def instant_buy_payment_success(request,add_id,comic_id):
    try:
        print('payment sucess', add_id)
        user =request.user
        customer_data = CustomerDetail.objects.get(pk=add_id)
        comic = Comic.objects.get(pk=comic_id)
        Order(user=user,customer=customer_data,comic=comic,quantity=1).save()
    except Exception as e:
        print('error occured here---->', e)
    return render(request,'core/payment_success.html')

# common to all failed payments
def payment_failed(request):
    return render(request,'core/payment_failed.html')

# order view
def order(request):
    orders = Order.objects.filter()
    return render(request,'core/order.html',{'ord':orders})

def order_cancel(request, order_id, checker):
    odr = Order.objects.get(pk=order_id)
    odr.delete()
    orders = Order.objects.filter()
    print('order....checking...')
    if checker:
        messages.success(request, 'Order deleted Successfully...')
        return render(request, 'core/order.html', {'ord':orders})
    else:
        messages.success(request, 'Order deleted Successfully...')
        return render(request, 'core/profile.html', {'is_order':True, 'orders':orders})
    

# profiles
def profile(request):
    return render(request, 'core/profile.html', {'is_profile':True})

def profile_Cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total=0
    for item in cart_items:
        total += item.product.discounted_price * item.quantity
    return render(request, 'core/profile.html', {'is_cart': True, 'cart_items':cart_items, 'total':total})

def profile_order(request):
    orders = Order.objects.filter()
    messages.success(request, 'Order deleted Successfully...')
    return render(request, 'core/profile.html', {'is_order': True, 'orders':orders})

# @login_required(login_url='log_in')
def rented_comic(request):
    rented_comics = Rental_system.objects.filter(user = request.user)
    for ren_co in rented_comics:
        cur_date = datetime.now()
        tz_aware_dt = timezone.make_aware(cur_date, timezone.get_current_timezone())
        print("CHECKING TIME IN TZ AWARE DATE TIME ---->", tz_aware_dt)
        if ren_co.rent_end_date < tz_aware_dt:
            ren_co.rental_status = 'expired'
            ren_co.save()
    rent_comics = Rental_system.objects.filter(user = request.user)
    return render(request, 'core/profile.html', {'is_rented_comic': True, 'rented_comics': rent_comics})


def cart_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total =0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    address = CustomerDetail.objects.filter(user=request.user)
    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total=0
        delivery_charge=2000
        for item in cart_items:
            total+=(item.product.discounted_price*item.quantity)
        final_price =total+delivery_charge
        return render(request, 'core/cart.html', {'cart_items':cart_items, 'total':total,'final_price':final_price})
    else:
        return redirect('login')
    
def increase_quantity(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart,pk=id)
        product.quantity+=1
        product.save()
        return redirect('show_cart')
    else:
        return redirect('login')
    
def decrease_quantity(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart,pk=id)
        product.quantity-=1
        product.save()
        return redirect('show_cart')
    else:
        return redirect('login')
    
def delete_cart(request,id):
    pet_cart =Cart.objects.get(pk=id)
    pet_cart.delete()
    return redirect('show_cart')

def add_to_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        product = Comic.objects.get(pk=id)
        Cart(user=user, product=product).save()
        messages.success(request, 'Added to Cart Successfully...')
        return redirect('show_comic_details', id)
    else:
        return redirect('login_page')
    


# dummy view for testing 
def cart_checkout_payment(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
    
    print('No Address in payment Selected----->', selected_address_id)
    if not selected_address_id:
        messages.success(request, 'No Address Selected Please select an Address')
        return redirect('show_cart')
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    delhivery_charge =2000
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total

    address = CustomerDetail.objects.filter(user=request.user)
    host = request.get_host()
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Comic',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('cart_payment_success',args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('payment_fail')}",
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    return render(request,'core/payment.html',{'paypal':paypal_payment})

def cart_payment_success(request, selected_address):
    user= request.user
    address_data = CustomerDetail.objects.get(pk=selected_address)
    cart=Cart.objects.filter(user=request.user)
    for cart in cart:
        Order(user=user,customer=address_data,quantity=cart.quantity,comic=cart.product).save()
        cart.delete()
    return render(request,'core/payment_success.html')