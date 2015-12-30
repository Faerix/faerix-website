from .models import Sponsor
import random

def inject_sponsors(request):
    sponsors = list(Sponsor.objects.filter(active=True))
    random.shuffle(sponsors)
    return {"sponsor_logos":sponsors}
