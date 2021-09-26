from django.shortcuts import render


def index(request):
    template = 'index.html'
    context = {
        'key': '123'
    }
    return render(request, template, context)
