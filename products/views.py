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


# ================= PRODUCTS BY STALL =================
def product_by_stall(request, stall_id):
    stall = get_object_or_404(Stall, id=stall_id)
    products = Product.objects.filter(stall=stall)

    return render(request, 'products/product_by_stall.html', {
        'stall': stall,
        'products': products
    })


# ================= ADD PRODUCT =================
def product_create(request):
    stalls = Stall.objects.all()

    if request.method == "POST":
        Product.objects.create(
            stall_id=request.POST.get('stall'),
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description') or ""
        )
        return redirect('product_list')

    return render(request, 'products/product_create.html', {
        'stalls': stalls
    })


# ================= EDIT PRODUCT (FIXED) =================
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    stalls = Stall.objects.all()

    if request.method == "POST":
        product.name = request.POST.get('name') or product.name
        product.price = request.POST.get('price') or product.price
        product.description = request.POST.get('description') or product.description
        product.stall_id = request.POST.get('stall') or product.stall_id

        product.save()
        return redirect('product_detail', id=product.id)

    return render(request, 'products/edit_product.html', {
        'product': product,
        'stalls': stalls
    })


# ================= DELETE PRODUCT =================
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.delete()
        return redirect('product_list')

    return redirect('product_detail', id=id)