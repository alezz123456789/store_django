from .models import Card,CardItem
from .views import _card_id

# from django.contrib.auth.models import User

def counter(request):
    card_count=0
    if 'admin' in request.path:
        return{}
    else:
        try:
            card=Card.objects.filter(card_id=_card_id(request))
            if request.user.is_authenticated:
                carditems=CardItem.objects.all().filter(user=request.user)
            else:
                carditems=CardItem.objects.all().filter(card=card[:1])
            for carditem in carditems:
                card_count += carditem.quantity
        except Card.DoesNotExist:
            card_count=0
    return dict(card_count=card_count)