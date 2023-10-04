from django.db import models
from store.models import Product,Variation
from accounts.models import Account
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
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation,blank=True)
    card=models.ForeignKey(Card,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name="CardItem" 
        verbose_name_plural="CardItems"

    def sub_total(self):
        return self.product.price * self.quantity
    def __unicode__(self):
        return self.product