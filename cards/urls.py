"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.conf import settings
# from django.conf.urls.static import static

# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.card ,name="card"),
    path('/add_card/<int:product_id>', views.add_card ,name="add_card"),
    path('/remove_card/<int:product_id>/<int:card_item_id>', views.remove_card ,name="remove_card"),
    path('/remove_card_item/<int:product_id>/<int:card_item_id>', views.remove_card_item ,name="remove_card_item"),

    path('checkout/', views.checkout ,name="checkout"),
    # path('/<slug:category_slug>', views.store ,name="products_by_category"),
    # path('/<slug:category_slug>/<slug:products_slug>', views.product_detail ,name="product_detail"),
]
