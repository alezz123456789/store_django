from django.shortcuts import render,get_object_or_404
from category.models import Category
from .models import Product
from cards.views import _card_id
from cards.models import CardItem
from django.db.models import Q
# Create your views here.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse

def store(request,category_slug=None):
    categories=None
    products=None

    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_avaliable=True)
        #######paginator start
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        ########paginator end
        products_count=products.count()
    else:
        products=Product.objects.all().filter(is_avaliable=True).order_by('id')
        #######paginator start
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        ########paginator end
        products_count=products.count()

    context={
        # "products":products,
        "products":paged_products,
        'products_count':products_count
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,products_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=products_slug)
        in_card=CardItem.objects.filter(card__card_id=_card_id(request),product=single_product).exists()
        if single_product.stock <=0:
            stock_empty=1
        else:
            stock_empty=0


    except Exception as e:
        raise e
    
    context={
        "single_product":single_product,
        'stock_empty':stock_empty,
        'in_card':in_card
    }
    return render(request,'store/product-detail.html',context)

def search(request):
    if 'Keyword' in request.GET:
        Keyword=request.GET['Keyword']
        if Keyword:
            products=Product.objects.order_by('created_date').filter(Q(description__icontains=Keyword) | Q(product_name__icontains=Keyword))
            products_count=products.count()
    context={
        'products':products,
        'products_count':products_count
    }
    return render(request,'store/store.html',context)
