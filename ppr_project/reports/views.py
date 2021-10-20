from django.shortcuts import render


def index(request):
    template = 'reports/index.html'
    return render(request, template)
