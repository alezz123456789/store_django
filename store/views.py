from django.shortcuts import render,get_object_or_404
from category.models import Category
from .models import Product

# Create your views here.

def store(request,category_slug=None):
    categories=None
    products=None

    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_avaliable=True)
        products_count=products.count()
    else:
        products=Product.objects.all().filter(is_avaliable=True)
        products_count=products.count()

    context={
        "products":products,
        'products_count':products_count
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,products_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=products_slug)
        
        if single_product.stock <=0:
            stock_empty=1
        else:
            stock_empty=0


    except Exception as e:
        raise e
    
    context={
        "single_product":single_product,
        'stock_empty':stock_empty
    }
    return render(request,'store/product-detail.html',context)
