"""fund URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from projects.views import *
from users.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),
    path('register/', register_view),
    path('home/', home),                          
    path('activate/<uidb64>/<token>',activate, name='activate'),
    path('logout/', logout_view),
    #path('user/', include('users.urls')),
    path('newproject/', create_project),
    path('showproject/<int:id>', show_project , name='project'),
    path('cancelproject/<int:id>', cancel_project , name='cancelproj'),
    path('rate/<id>', rate_project),
    path('listprojects', list_projects, name='projects'),
    path('listdons', listdons, name='listdons'),
    path('profile' , user_profile , name='profile') ,
    path('update_profile' , update_profile , name='update_prof') ,
    path('del_profile' , del_profile , name='del_prof') ,
    path('donate/<id>', donate_proj),
    path('report_proj/<id>', add_repo),
    path('comment/<id>', add_com),
    path('category/<int:id>', show_cate , name='category'),
    path('delete', testdel),
    #path('report_com/<id>', rep_comment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
