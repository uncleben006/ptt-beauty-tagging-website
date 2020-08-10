from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    a = 1
    return render(request, 'app/index.html', {'key': a})
