from .models import Sponsor, News
from django.utils import timezone
import random

def inject_sponsors(request):
    sponsors = list(Sponsor.objects.filter(active=True))
    random.shuffle(sponsors)
    return {"sponsor_logos":sponsors}

def inject_news_count(request):
    count = News.objects.filter(visible_from__lte=timezone.now(), visible_up_to__gte=timezone.now()).count()
    return {"news_count" :count}
