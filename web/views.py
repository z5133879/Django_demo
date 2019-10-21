from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from web.models import User,UserType
from django.contrib.auth import authenticate,login
import re
# Create your views here.
def hello_view(request):
    return render(request, 'my-account.html',{
        #'data':"Hello Django"
    })
def index(request):
    if request.method == 'POST':
        if 'search_button' in request.POST:

            location = request.POST['location']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            print(location,start_date,end_date)
            return render(request, "search_content.html",{})

    # print("aaaaa")
    # print(request.user.is_authenticated())
    # print("aaaaa")
    # if request.user.is_authenticated():
    #     print("bbbb")
    # login_register = request.POST['login_register']
    #
    # if login_register:
    #     return render(request, 'login.html',{
    #
    # })
    return render(request,'index.html')
def login(request):
    if request.method == 'POST':
        re_match = re.compile('^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$')
        if 'register' in request.POST:
            register_name = request.POST['name']
            register_email = request.POST['email']
            register_password = request.POST['reg_password']
            register_comPassword = request.POST['comf_password']
            register_type = request.POST['user_type']
            cerifi_email = re_match.match(register_email)
            ## whether the email is existed.
            try:
                User.objects.get(Email=register_email)
                return render(request, "login.html", {"register_msg": "email address already exist!",
                                                      "register_color": "text-dark-red"})
            except:
                pass
            ## to define whether the email is valid
            if not cerifi_email:
                return render(request,"login.html",{"register_msg":"Please input valid email address!",
                                                    "register_color":"text-dark-red"})
            ## to define whether the two password is same
            elif register_comPassword != register_password:
                return render(request,"login.html",{"register_msg":"Password not match",
                                                    "register_color":"text-dark-red"})
            # to define whether the usertype is selected
            elif register_type != "user" and register_type != "provider":
                return render(request, "login.html", {"register_msg": "Please select your user type!",
                                                      "register_color": "text-dark-red"})

            else:
                usertype = UserType.objects.get(TypeName=register_type)
                user = User(Account=register_name,Email=register_email,Password=register_password,Type=usertype)
                user.save()
                return render(request, "index.html")
        elif 'login' in request.POST:
            username = request.POST['username']
            userPassword = request.POST['password']
            user = authenticate(username=username,password=userPassword)
            #print(username,userPassword)
            #print(user)
            if user is not None:
                login(request, user)

            try:
                username = User.objects.get(Email=username)
                if username.Password != userPassword:
                    return render(request,"login.html",{"login_msg":"wrong password/username,please try again!",
                                                        "login_color":"text-dark-red"})
            except ObjectDoesNotExist:
                return render(request,"login.html",{"login_msg":"username does not exist!",
                                                    "login_color":"text-dark-red"})
            ## login success

            return render(request,"index.html")


    return render(request, 'login.html',{"register_msg":"If you have an account with us, Please login!",
                                         "login_msg":"If you have an account with us, Please login!",
                                         "login_color": "text-gray"
    })
def order(request):
    return  render(request,'order.html',{

    })
def shop(request):
    return render(request,'shop.html',{

    })
def search_content(request):
    return render(request,'search_content.html',{

    })