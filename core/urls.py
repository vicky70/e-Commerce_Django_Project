from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

# ()
urlpatterns = [
    path('', views.home, name='home'),
    path('comic-list', views.show_comic_list, name='show_comic_list'),
    path('comic_detail/<int:id>/', views.show_comic_details, name='show_comic_details'),
    path('login_page/', views.login_page, name='login_page'),
    path('log_out', views.log_out, name='log_out'),
    path('sign_up', views.registration_form, name='registration'),
    # Address path
    path('Change_address', views.address, name='address'),
    path('edit_address<int:id>/', views.edit_address, name="edit_address"),
    path('delete_address<int:id>/', views.edit_address, name="delete_address"),
    # purchase --- rent --- add to cart
    path('instant_buy/<int:id>/', views.instant_buy, name='instant_buy'),
    path('instant_buy_payment/<int:comic_id>/', views.instant_buy_payment, name='instant_buy_payment'),
    path('instant_buy_payment_success/<int:add_id>/<int:comic_id>/', views.instant_buy_payment_success, name='instant_buy_payment_success'),
    path('payment_fail/', views.payment_failed, name='payment_fail'),
    # order urls
    path('orders/', views.order, name="order"),
    path('order_cancel/<int:order_id>/<int:checker>/', views.order_cancel, name='order_cancel'),

    # profile
    path('profile/', views.profile, name="profile"),
    path('profile_cart', views.profile_Cart, name='profile_cart'),
    path('profile_order/', views.profile_order, name="profile_order"),
    path('profile_rent/', views.rented_comic, name='profile_rented_comic'),

    # profile cart url
    path('profile_cart/', views.cart, name='cart'),

    # /add to cart
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('show_cart/', views.cart, name='show_cart'),
    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),

    # cart payment url
    path('cart_checkout_payment/', views.cart_checkout_payment, name='cart_checkout_payment'),
    path('cart_payment_success/<int:selected_address>/', views.cart_payment_success, name='cart_payment_success'),
]
# ()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)