from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Cart, CartItem, Product


def product_list(request):
    query = request.GET.get("q","")
    products = Product.objects.filter(is_active=True)
    category = request.GET.get("category")
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        products = products.filter(category=category)
    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
            "query": query,
            "category": category,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
        },
    )

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f"{product.name} added to your cart."
    )

    return redirect("cart")

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related("product")

    return render(
        request,
        "store/cart.html",
        {
            "cart": cart,
            "items": items,
        },
    )

@login_required
def update_cart_item(request, item_id):
    cart = get_object_or_404(
        Cart,
        user=request.user,
    )

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart,
    )

    action = request.POST.get("action")

    if action == "increase":
        if item.quantity < item.product.stock:
            item.quantity += 1
            item.save(update_fields=["quantity"])
        else:
            messages.error(
                request,
                f"Only {item.product.stock} units of {item.product.name} are available.",
            )

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save(update_fields=["quantity"])
        else:
            item.delete()

    elif action == "remove":
        item.delete()

    return redirect("cart")