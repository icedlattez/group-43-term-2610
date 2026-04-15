from django.shortcuts import render

def vendor_list(request):
    return render(request, 'vendor/vendor_list.html')