
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistraionForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django import forms
from django.http import HttpResponse
from projects.forms import *
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.models import User
import datetime
from projects.models import *
# from projects.models import Categories, Projects, Project_donations, Tags
# from projects.forms import NewProject
from django.db.models import Q, Avg, Sum
from django.template.defaulttags import register
from django.contrib import messages
from .forms import UpdateUserForm

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.id) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()








def register_view(request):
    context = {}
    if request.method=='POST':
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            print('hello  register')
            user=form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to you'
            message = render_to_string('activate_msg.html', {
                'user': user,
                'domain': current_site.domain,
                'id': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        
            
            return HttpResponseRedirect("/")
        else:
            print('hello  register222222')
            context["form"] = form
    else:
        
        form = RegistraionForm()
        context["form"] = form
    return render(request, "register.html", context)


def activate(request, uidb64, token):
    try:
        user = User.objects.get(id=uidb64)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request , 'confirm_msg.html' , {'msg':'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request , 'confirm_msg.html' , {'msg':'Activation link is invalid!'})


def login_view(request):
    context = {}
    user = request.user
    msg=''

    if user.is_authenticated:
        return HttpResponseRedirect('/home')

    if request.method=='POST':
        #form = LoginForm(request.POST )
        usr=User.objects.filter(email=request.POST['email'],password=request.POST['password'])

        if len(usr)<1:            
            msg='invalid login data...'
            return render(request, "login.html" ,{'msg':msg})


        elif len(usr)>0 and usr.first().is_active == False:          
            msg='please confirm your email address to complete the registration'
            return render(request, "login.html" ,{'msg':msg})
            

        elif len(usr)>0 and usr.first().is_active == True:
            user=usr.first()
            login(request, user)
            return HttpResponseRedirect('/home')

   

    else:
        return render(request, "login.html")
        

    



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def send_email(user, current_site, email, email_body, email_subject):
    mail_subject = email_subject
    message = render_to_string(
        email_body,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "time": urlsafe_base64_encode(force_bytes(datetime.datetime.now())),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def list_projects(request):
    
    #tags = Tags.objects.all()
    user_projects = Projects.objects.filter(user_id=request.user.id)

    donations_flag = {}
    donations = {}
    for project in user_projects:
        donation = project.project_donations_set.all().count()
        total_raised = 0
        don_flag = 1

        if donation:
            total_raised = project.project_donations_set.all(
            ).aggregate(Sum("donation"))["donation__sum"]

            if total_raised >= (project.total_target*0.25):
                don_flag = 0
        donations_flag[project.id] = don_flag
        donations[project.id] = total_raised

    project_form = NewProject()
    context = {"user_projects": user_projects,
               
               "donations": donations,
               "donations_flag": donations_flag,
               
               }
    
    # print( user_projects , donations , donations_flag )
    # return HttpResponse('   list projects ')
    return render(request, "myprojects.html", context=context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



# @register.filter
# def get_val(lis, val):
#     return lis[val]



def user_profile(request):
   
    return render(request, "profile.html")



def update_profile(request):
    if request.POST:
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print("photo from form is :", form.cleaned_data["photo"])
            request.user.photo = form.cleaned_data["photo"]
            form.save()
            return  HttpResponseRedirect('/profile')   
    else:
        form = UpdateUserForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "date_birth": request.user.date_birth,
                "facebook_link": request.user.facebook_link,
                "country": request.user.country,
            }
        )
    context = {"form": form}
    return render(request, "update_prof.html", context=context)


def del_profile(req):
    user=req.user
    user.delete()
    logout(req)
    return HttpResponseRedirect("/")






def create_project(request):
    alltags=Tags.objects.all()
    if request.method == 'POST':
        project_form = NewProject(request.POST)
        if project_form.is_valid():
            tags = request.POST.getlist('tags')
            form = project_form.save(commit=False)
            form.user = request.user
            form.save()
            for file in request.FILES.getlist('images'):
                Project_pics(project_id=form.id, pic=file).save()

            if request.POST['new_tag']:
               
                new_tags = request.POST['new_tag'].split(',')
                for new_tag in new_tags:
                    tag = Tags(name=new_tag)
                    tag.save()
                    tags.append(tag.id)
                print(tags)
            for tag_id in tags:
                Project_tags(project_id=form.id, tag_id=tag_id).save()
            return HttpResponseRedirect('/listprojects')
        else:
            print(project_form.errors)
            messages.success(request,project_form.errors) 
            return render (request , 'newproject.html'  ,{'form':project_form  , 'tags':alltags} )
    else:
        project_form = NewProject()
        return render (request , 'newproject.html'  ,{'form':project_form   , 'tags':alltags} )



