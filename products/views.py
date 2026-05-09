from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from owner.models import Stall


# ================= PRODUCT LIST =================
def product_list(request):
    products = Product.objects.select_related('stall').all()

    return render(request, 'products/product_list.html', {
        'products': products
    })


# ================= PRODUCT DETAIL =================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'products/product_detail.html', {
        'product': product
    })


# ================= ADD PRODUCT =================
def product_create(request):
    stalls = Stall.objects.all()

    if request.method == "POST":
        Product.objects.create(
            stall_id=request.POST.get('stall'),
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description')
        )
        return redirect('product_list')

    return render(request, 'products/product_create.html', {
        'stalls': stalls
    })