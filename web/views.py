from django.shortcuts import render

# Create your views here.
def hello_view(request):
    return render(request, 'my-account.html',{
        #'data':"Hello Django"
    })
def hotel_add(request):
    return render(request, 'index.html',{

    })
def login(request):
    return render(request, 'login.html',{

    })
def order(request):
    return  render(request,'order.html',{

    })
def shop(request):
    return render(request,'shop.html',{

    })