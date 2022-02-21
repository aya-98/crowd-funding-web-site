from django.http import HttpResponse
from django.shortcuts import render , HttpResponseRedirect ,redirect
from .models import *
from django.db.models import Q, Avg, Sum
from .forms import *
from django.contrib import messages

def show_project(req, id):
    project = Projects.objects.get(id=id)
    user = req.user.id
    donations = project.project_donations_set.all().aggregate(Sum("donation"))
    user_rating_count = Project_rating.objects.filter(
        project_id=id, user_id=user).count()
    project_pics = project.project_pics_set.all()
    comments = Project_comments.objects.filter(project_id=id)
    if user_rating_count:
        user_rating = Project_rating.objects.get(
            project_id=id, user_id=user).rating
    else:
        user_rating = 0

    #avg_rate =project.project_rating_set.all().aggregate(Avg("rating"))["rating__avg"]

    if donations["donation__sum"]:
        project_donation = donations["donation__sum"]
        
    else:
        
        project_donation = 0

    tags = Project_tags.objects.filter(project_id=id)
    projects = []
    for tag in tags:
        p = Project_tags.objects.filter(tag_id=tag.tag_id).exclude(project_id = id)
        print( 'hello ', p)
        if len(p)>0 :
            for pr in p:                
                projects.append(pr)
    res={}
    pro=[]
    if len(projects)<4:
        for p in projects:
            fpic=p.project.project_pics_set.all()[0]
            if p.project.id not in res:
                pro.append(p.project)
                res[p.project.id] = fpic
        print(  "testeeeee" , res  )    
       
    else:
        for i in range (4):
            fpic=projects[i].project.project_pics_set.all()[0]
            if projects[i].project.id not in res:
                pro.append(projects[i].project)
                res[projects[i].project.id] = fpic
        
        print(  "testeeeee" , res  ) 
        
    print(pro , res)

    context = {'project': project,
               #'overall':avg_rate ,
               'user_rate': user_rating,
               'pics': project_pics,
               'donations': project_donation,
               'comments': comments,
               'report1': Report1(),
               'report2': Report2(),
               'donation_form': Donate(),
               'pro': pro , 
               'pho':res ,
               'tags':tags
               
               }

    return render(req, 'project_page.html', context)



def rate_project(req, id):

    project = Projects.objects.get(id=id)

    prev=Project_rating.objects.filter(project_id=id , user_id=req.user.id)

    if len(prev) >0:
        Project_rating.objects.filter(project_id=id , user_id=req.user.id).update(rating=req.POST['r'])
    
    else:
         Project_rating.objects.create(user=req.user , project= project ,rating=req.POST['r'] )
    

    avg_rate =project.project_rating_set.all().aggregate(Avg("rating"))["rating__avg"]

    Projects.objects.filter(id = id).update(rating=avg_rate)
    print(req.POST['r'])
    return redirect(f'/showproject/{id}')
    #return HttpResponseRedirect('/showproject/{id}')


def donate_proj(req , id):

    donating_value = int(req.POST['don'])
    project = Projects.objects.get(id=id)
    project.raised+=donating_value
    if  project.raised <= project.total_target :
        project.save()
        
        Project_donations.objects.create(
            project=project,
            user=req.user,
            donation=donating_value
        )
        messages.success(req, ' thank you for donation')
        return redirect(f'/showproject/{id}')
    else:
        messages.error(req, "Your Donation failed " )
        return redirect(f'/showproject/{id}')



def add_com(req , id):
    project = Projects.objects.get(id=id)
    Project_comments.objects.create(
            project=project,
            user=req.user,
            comment=req.POST['commt']
        )
    
    messages.success(req, ' Comment added successfully')
    return redirect(f'/showproject/{id}')


def add_repo(req , id):
    project = Projects.objects.get(id=id)
    ReportProj.objects.create(
            project=project,
            user=req.user,
            report=req.POST['report1']
        )
    
    messages.success(req, ' Report added successfully')
    return redirect(f'/showproject/{id}')



def home(req ):
    projectRates = Project_rating.objects.all().values('project').annotate(
        Avg('rating')).order_by('-rating__avg')[:5]
    print(projectRates)

    highRatedProjects = []
    project_pics2 = {}
    for p in projectRates:

        # project_pics = p.p_pics_set.all()
        print("id ?? ", p.get('project'))
        highRatedProjects.append(Projects.objects.get(id=p.get('project')))
        print(highRatedProjects)
        project_pics = Project_pics.objects.filter(project=p.get('project'))
        project_pics2[p.get('project')] = project_pics[0]
        print("project_pics2")

    print(highRatedProjects)

    latestFiveList = Projects.objects.extra(order_by=['-created_at'])[:5]
    for p in latestFiveList:
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]

    featuredList = Projects.objects.all().filter(featured='True')[:5]
    for p in featuredList:
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]
    categories = Categories.objects.all()
    context = {
        'lproj': latestFiveList,
        'fproj': featuredList,
        'hproj': highRatedProjects,
        'cate': categories,
        'pics': project_pics2

    }
    return render(req, 'home.html', context)

def show_cate(req , id):
    cate=Categories.objects.get(id=id)
    projs= cate.projects_set.all()
    project_pics2={}
    for p in projs:
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]

    
    return render(req , 'category.html' ,{'projs':projs , 'pics': project_pics2 , 'c': cate.title})



def cancel_project(req , id):

    Projects.objects.filter(id=id).delete()

    return HttpResponseRedirect('/listprojects')

    #return redirect(f'/listprojects')


def listdons(req ):
    user=req.user
    dons=user.project_donations_set.all()

    return render(req ,'listdons.html' ,{'dons':dons} )





def testdel(req):
    Projects.objects.filter(id=3).delete()
    return HttpResponse('hello')