from django.shortcuts import render

# Create your views here.


def card(request):
    return render(request,'store/card.html')
