from django.db import models
from store.models import Product
# Create your models here.

class Card(models.Model):
    card_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name="Card" 
        verbose_name_plural="Cards"
    
    def __str__(self):
        return self.card_id


class CardItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    card=models.ForeignKey(Card,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name="CardItem" 
        verbose_name_plural="CardItems"

    def __str__(self):
        return self.product