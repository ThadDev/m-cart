from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list, name="product_list"),
    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
    "cart/add/<slug:slug>/",
    views.add_to_cart,
    name="add_to_cart",
),
path(
    "cart/",
    views.cart,
    name="cart",
),
path(
    "cart/item/<int:item_id>/update/",
    views.update_cart_item,
    name="update_cart_item",
),
]