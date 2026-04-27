from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing
from django.contrib.auth.decorators import login_required

# 🏠 Homepage
def listing_list(request):
    products = Listing.objects.filter(is_product=True)
    personal_listings = Listing.objects.filter(is_product=False)

    return render(request, 'listings/listing_list.html', {
        'products': products,
        'personal_listings': personal_listings
    })


# 📄 Detail page
def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    return render(request, 'listings/listing_detail.html', {
        'listing': listing
    })


# ➕ Create PERSONAL listing (user)
@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')

        Listing.objects.create(
            title=title,
            description=description,
            price=price,
            user=request.user,
            is_product=False
        )
        return redirect('listing_list')

    return render(request, 'listings/create_listing.html')


# 🛍️ Create PRODUCT (admin only)
@login_required
def create_product(request):
    if not request.user.is_staff:
        return redirect('listing_list')

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        Listing.objects.create(
            title=title,
            description=description,
            price=price,
            stock=stock,
            is_product=True,
            user=None
        )
        return redirect('listing_list')

    return render(request, 'listings/create_product.html')