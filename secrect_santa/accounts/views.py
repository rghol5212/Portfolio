from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from .forms import RegisterForm, SantasListForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import get_user_model, authenticate, login, logout
import smtplib, ssl
import random

# Create your views here.
from django.http import HttpResponse

User = get_user_model()


def index(request):
    return render (request, 'accounts/home.html', {})


def login_user(request):
    if request.method == "GET":
        return render(request, "accounts/login_user.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
            )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('acc:index'))
        else:
            return HttpResponse("Invalid Username and or Password")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("acc:index")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/create_user.html",
        {"form": form}
        )


def logout_user(request):
    logout(request)
    return render(request, "accounts/logged_out.html")

def santas_list_signup(request):
    if request.method == "POST":
        form = SantasListForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, "accounts/santas_list_signup_succ.html")
    else:
        form = SantasListForm()
        return render(
            request,
            "accounts/santas_list_signup.html",
            {"form": form}
            )

def send_email(user, receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "python5212@gmail.com"  # Enter your address
    receiver_email = f"{receiver_email}"  # Enter receiver address
    password = 'ur8grwd8'
    message = f'''
                Your secrect santa is {user}..

                Merry Xmas!!


                '''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



def santascontrol(request):
    if request.method == "POST":
        avoid_pairs = {} #{'Ryan': 'a', 'Robert': 'z'}
        avoid_users = list(request.POST) #['csrfmiddlewaretoken', 'Ryan', 'Robert']
        avoid_users.remove('csrfmiddlewaretoken')
        santas_list = SantasList.objects.all()
        for avoid_user in avoid_users:
            avoid_pairs[avoid_user] = request.POST[f'{avoid_user}']


        pairs = {}

        while len(avoid_users) > 1:

            #Using the randomly created indices, respective elements are popped out
            r1 = random.randrange(0, len(avoid_users))
            elem1 = avoid_users.pop(r1)

            r2 = random.randrange(0, len(avoid_users))
            elem2 = avoid_users.pop(r2)

            if avoid_pairs[elem1] != avoid_pairs[elem2]:
            # now the selecetd elements are paired in a dictionary 
                pairs[elem1] = elem2
            else:
                avoid_users.append(elem1)
                avoid_users.append(elem2)

        print(pairs)

        for paired in pairs:
            user1 = paired
            user2 = pairs[paired]
            print(user1)
            print(user2)


#UNCOMMENT WHEN YOU WANT TO ACTUALLY SEND OUT EMAILS
            # obj_user1 = SantasList.objects.get(name = str(user1))
            # obj_user2 = SantasList.objects.get(name = str(user2))

            # send_email(user1, obj_user1.email)
            # send_email(user2, obj_user2.email)
            
        return render(request, "accounts/santas_list_signup_succ.html")


    else:
        santaslist = SantasList.objects.all()
        return render(request, "accounts/santas_list_view_admin.html", {"santaslist": santaslist})