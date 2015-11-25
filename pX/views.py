from datetime import datetime
from django.shortcuts import render


def home(request):
    return render(
        request,
        'loginpartials.html',
        context={
            'title': 'Home Page',
            'year': datetime.now().year,
            'request': request,
            'user': request.user,
        })
