from django.urls import path
#from users.views import  list_projects, donations_list,user_profile,user_profile_update
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from users.views import  list_projects


# app_name = 'users'

# urlpatterns = [
    
#     path('projects', list_projects, name='projects'),
#     # path('donations', donations_list, name='donations'),
#     # path('profile',user_profile,name="profile"),
#     # path('profile/update',user_profile_update,name="profile_update"),
#     # #path('profile/delete/request',send_delete_email,name="delete_request"),
    
# ]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)