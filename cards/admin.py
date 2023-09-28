from django.contrib import admin
from .models import Card,CardItem
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display=('card_id','date_added')

admin.site.register(Card,CardAdmin)

class CardItemAdmin(admin.ModelAdmin):
    list_display=('product','card','quantity','is_active')

admin.site.register(CardItem,CardItemAdmin)

