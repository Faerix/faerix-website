from .models import Sponsor, News, currentConv
from django.utils import timezone
from django.conf import settings
import random

def inject_sponsors(request):
	path=getattr(request,"path","")
	year=currentConv()
	try :
	#Extremly dirty but I can't find why the request.GET is always empty
	#otherwise request.GET.get("year",currentConv()) would have worked
		if (path[:5])=="/old/":
			year = int(path[5:9])
	except:
		pass
	sponsors = list(Sponsor.objects.filter(active=True,conv=year))
	random.shuffle(sponsors)
	return {"sponsor_logos":sponsors,"year":1111111}

def inject_news_count(request):
	count = News.objects.filter(visible_from__lte=timezone.now(), visible_up_to__gte=timezone.now()).count()
	return {"news_count" :count}

def inject_static_url(request):
	# for django-front
	return {"STATIC_URL": settings.STATIC_URL}
