from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Card,CardItem
# Create your views here.
# from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _card_id(request):
    card=request.session.session_key
    if not card:
        card=request.session.create()
    return card

def add_card(request,product_id):
    current_user=request.user
    product=Product.objects.get(id=product_id)#get product
    # if the user is an auth 
    if current_user.is_authenticated:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                
                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # try:
        #     card=Card.objects.get(card_id=_card_id(request))# get the card using card_id present in the session
        # except Card.DoesNotExist:
        #     card=Card.objects.create(
        #         card_id=_card_id(request)
        #     )
        # card.save()

        is_card_item_exists=CardItem.objects.filter(product=product,user=current_user).exists()
        if is_card_item_exists:
            card_item=CardItem.objects.filter(product=product,user=current_user)
            ## 1- existing_variation -> Database
            ## 2- current variation -> product_variation
            ## 3- item_id -> Database

            #1
            ex_var_list=[]
            id=[]
            for item in card_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            #2
            if product_variation in ex_var_list:
                #increace the card item quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CardItem.objects.get(product=product,id=item_id)

                item.quantity +=1
                item.save()
            else:
                #create a new card_item
                item=CardItem.objects.create(product=product,quantity=1,user=current_user)
                ####
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            card_item=CardItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                card_item.variation.clear()
                card_item.variation.add(*product_variation)
            ####
            card_item.save()
        # return HttpResponse(card_item.quantity)
        # exit()
        return redirect('card')
    # if the user is not auth
    else:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                
                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            card=Card.objects.get(card_id=_card_id(request))# get the card using card_id present in the session
        except Card.DoesNotExist:
            card=Card.objects.create(
                card_id=_card_id(request)
            )
        card.save()

        is_card_item_exists=CardItem.objects.filter(product=product,card=card).exists()
        if is_card_item_exists:
            card_item=CardItem.objects.filter(product=product,card=card)
            ## 1- existing_variation -> Database
            ## 2- current variation -> product_variation
            ## 3- item_id -> Database

            #1
            ex_var_list=[]
            id=[]
            for item in card_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            #2
            if product_variation in ex_var_list:
                #increace the card item quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CardItem.objects.get(product=product,id=item_id)

                item.quantity +=1
                item.save()
            else:
                #create a new card_item
                item=CardItem.objects.create(product=product,quantity=1,card=card)
                ####
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            card_item=CardItem.objects.create(
                product=product,
                quantity=1,
                card=card,
            )
            if len(product_variation) > 0:
                card_item.variation.clear()
                card_item.variation.add(*product_variation)
            ####
            card_item.save()
        # return HttpResponse(card_item.quantity)
        # exit()
        return redirect('card')

def remove_card(request,product_id,card_item_id):
    
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            card_item=CardItem.objects.get(product=product,user=request.user,id=card_item_id)
        else:
            card=Card.objects.get(card_id=_card_id(request))
            card_item=CardItem.objects.get(product=product,card=card,id=card_item_id)
        if card_item.quantity > 1:
            card_item.quantity -=1
            card_item.save()
        else:
            card_item.delete()   
    except:
        pass
    return redirect('card')

def remove_card_item(request,product_id,card_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        card_item=CardItem.objects.get(product=product,user=request.user,id=card_item_id)
        card_item.delete()
    else:
        card=Card.objects.get(card_id=_card_id(request))
        card_item=CardItem.objects.get(product=product,card=card,id=card_item_id)
        card_item.delete()
    return redirect('card')


def card(request,total=0,quantity=0,card_item=None):
    try:
        if request.user.is_authenticated:
            card_items=CardItem.objects.filter(user=request.user,is_active=True)
        else:
            card=Card.objects.get(card_id=_card_id(request))
            card_items=CardItem.objects.filter(card=card,is_active=True)
        for card_item in card_items:     
            total += (card_item.product.price * card_item.quantity)  
            quantity += card_item.quantity
        tax=(2*total)/100
        grand_total=total+tax    
    except ObjectDoesNotExist:
        pass # just ignore
    # context_object_name={
    #     'card_item':card_item
    # }
    context={
        'total':total,
        'quantity':quantity,
        'card_items':card_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'store/card.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,card_item=None):
    try:     
        if request.user.is_authenticated:
            card_items=CardItem.objects.filter(user=request.user,is_active=True)
        else:
            card=Card.objects.get(card_id=_card_id(request))
            card_items=CardItem.objects.filter(card=card,is_active=True)
        for card_item in card_items:
            total += (card_item.product.price * card_item.quantity)
            quantity += card_item.quantity
        tax=(2*total)/100
        grand_total=total+tax    
    except ObjectDoesNotExist:
        pass # just ignore
    # context_object_name={
    #     'card_item':card_item
    # }
    context={
        'total':total,
        'quantity':quantity,
        'card_items':card_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'store/checkout.html',context)
