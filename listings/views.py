from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing
from django.contrib.auth.decorators import login_required


# Homepage
def listing_list(request):
    products = Listing.objects.filter(is_product=True)
    personal_listings = Listing.objects.filter(is_product=False)

    return render(request, 'listings/listing_list.html', {
        'products': products,
        'personal_listings': personal_listings
    })


# Detail page
def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)

    return render(request, 'listings/listing_detail.html', {
        'listing': listing
    })


# Create PERSONAL listing
@login_required
def create_listing(request):
    if request.method == "POST":
        Listing.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            user=request.user,
            is_product=False
        )
        return redirect('listing_list')

    return render(request, 'listings/create_listing.html')


# Create PRODUCT (admin only)
@login_required
def create_product(request):
    if not request.user.is_staff:
        return redirect('listing_list')

    if request.method == "POST":
        Listing.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            user=None,
            is_product=True
        )
        return redirect('listing_list')

    return render(request, 'listings/create_product.html')


# Edit listing
@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if listing.user and listing.user != request.user:
        return redirect('listing_list')

    if request.method == "POST":
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.price = request.POST.get('price')
        listing.save()
        return redirect('listing_detail', id=listing.id)

    return render(request, 'listings/edit_listing.html', {
        'listing': listing
    })


# DELETE LISTING (FIXED — YOU WERE MISSING THIS)
@login_required
def delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if listing.user and listing.user != request.user:
        return redirect('listing_list')

    if request.method == "POST":
        listing.delete()
        return redirect('listing_list')

    return redirect('listing_detail', id=id)