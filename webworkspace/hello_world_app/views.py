from django.shortcuts import render

def index(request):
    return render(request, 'index_hello.html')

def about(request):
    return render(request, 'about_hello.html')
