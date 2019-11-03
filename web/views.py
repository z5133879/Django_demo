from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist

from web import mongoDB
from web.models import User,UserType
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
import re
import pymongo
from bson.objectid import ObjectId
import json
import random
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

def listing(request):

    def get_connection():
        client = pymongo.MongoClient('mongodb://47.74.87.45:27017/')
        db = client['airtan']
        collection = db['accomodation']
        return client, db, collection

    def query_doc_by_id(id):
        mongodb, db, collection = get_connection()
        doc = collection.find_one({'_id': ObjectId(id)})
        print(doc)
        return doc

    def query_doc_by_index(query, page_size, page_num):
        skip = page_size * (page_num - 1)
        mongodb, db, collection = get_connection()
        pages = collection.find(query).limit(page_size).skip(skip)

        print(f'querying page {page_num}')
        # for r in pages:
        #     print(r)
        return pages

    def query_doc_by_name(name, page_size, page_num):
        query = {"Name": {"$regex": name, "$options": "$i"}}
        pages = query_doc_by_index(query, page_size, page_num)
        return pages

    def query_doc_by_location(location, page_size, page_num):
        query = {"Location": {"$regex": location, "$options": "$i"}}
        pages = query_doc_by_index(query, page_size, page_num)
        # for r in pages:
        #     print(r)
        return pages

    def insert_doc():
        mongodb, db, collection = get_connection()

    def delete_doc_by_id(id):
        mongodb, db, collection = get_connection()
        query = {'_id': ObjectId(id)}
        x = collection.delete_many(query)
        print(id)
        print(x.deleted_count, "个文档已删除")

    def query_doc():
        mongodb, db, collection = get_connection()
        dblist = collection.list_database_names()
        if "airtan" in dblist:
            print("airtan")
        c = 0
        for x in collection.find():
            c += 1
            print(x)
        print(c)

    abc = query_doc_by_location('coogee', 12, 1)
    ddd = []
    print("============")
    #print(abc)
    index = 0
    for e in abc:
        ##e.pop("_id")
        e["page_id"] = "1"
        e["number"] = str(index)
        e["_id"] = str(e["_id"])
        lat,lng = e["Coordinates"].split(",")
        e["lat"] = float(lat)
        e["lng"] = float(lng)
        e["rating"] = round(random.uniform(3.0,5.0),1)
        index += 1
        print(e)
        ddd.append(json.dumps(e))
    print("dddddddedd")
    print(ddd)

    return render(request,'listing.html',{
        'abc':json.dumps(ddd),
        'page_id':"1",

    })
def more_listing(request,page_id='1'):
    if page_id != "2":

        a= mongoDB.MongoDb('coogee', 12, 1)
        abc = a.get_result()
    else:
        a = mongoDB.MongoDb('coogee', 12, 2)
        abc = a.get_result()
    ddd = []
    print("============")
    #print(abc)
    index = 0
    for e in abc:
        ##e.pop("_id")
        e["page_id"] = "1"
        e["number"] = str(index)
        e["_id"] = str(e["_id"])
        lat,lng = e["Coordinates"].split(",")
        e["lat"] = float(lat)
        e["lng"] = float(lng)
        e["rating"] = round(random.uniform(3.0,5.0),1)
        print(e["rating"])
        index += 1
        print(e)
        ddd.append(json.dumps(e))
    print("dddddddedd")
    print(ddd)
    if page_id == "undefined":
        page_id = 1
    return render(request, 'listing.html', {
        'abc': json.dumps(ddd),
        'page_id':page_id,

    })

    #return HttpResponse(page_id)
def single_page(request):
    id = request.GET.get('id')
    page = request.GET.get('page')
    mongon =     mongoDB.MongoDb('coogee', 12, int(page))
    Json_data = mongon.get_result()
    for e in Json_data:
        if str(e["_id"]) == id:
            e["O_id"] = id
            lat, lng = e["Coordinates"].split(",")
            e["lat"] = float(lat)
            e["lng"] = float(lng)
            e["page_id"] = page
            e["rating"] = round(random.uniform(3.0, 5.0), 1)
            Json = e
            break

    Photos = Json["Photos"]
    photo_1 = Photos[0]
    photo_2 = Photos[1]
    photo_3 = Photos[2]
    photo_4 = Photos[3]
    photo_5 = Photos[4]
    #print(page,id)
    print(Photos)

    return render(request,'listing-single.html',{
        "json_date":Json,"photo_1":photo_1,"photo_2":photo_2,"photo_3":photo_3,"photo_4":photo_4,
        "photo_5": photo_5,


    })
def dashboard(request):
    return render(request,'dashboard.html')

def dashboard_add(request):
    return render(request,'dashboard-add-listing.html')

def dashboard_myprofile(request):
    return render(request,'dashboard-myprofile.html')

def review(request):
    return render(request,'dashboard-review.html')

def easy_single(request):
    return render(request,'listing-single2.html')

def booking(request):
    id = request.GET.get('id')
    page = request.GET.get('page')
    print(id,page)
    return render(request,'booking-single.html')
