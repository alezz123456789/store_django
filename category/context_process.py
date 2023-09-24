from .models import Category

def menulinkes(request):
    links=Category.objects.all()
    return dict(links=links)