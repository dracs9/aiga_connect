from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.store_list, name="list"),
    path("<int:pk>/", views.product_detail, name="detail"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
]
