from .models import Sponsor, News, currentConv
from django.utils import timezone
from django.conf import settings
import random

def inject_sponsors(request):
    print(list(request.GET))
    year=request.GET.get("year",currentConv())
    sponsors = list(Sponsor.objects.filter(active=True,conv=year))
    random.shuffle(sponsors)
    return {"sponsor_logos":sponsors}

def inject_news_count(request):
    count = News.objects.filter(visible_from__lte=timezone.now(), visible_up_to__gte=timezone.now()).count()
    return {"news_count" :count}

def inject_static_url(request):
    # for django-front
    return {"STATIC_URL": settings.STATIC_URL}
