from django.urls import path
from . import views 
urlpatterns = [

    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('base/',views.base,name='base'),
    path('index/',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('save_info/',views.save_info,name='save_info'),
    path('accounts_list_user/',views.accounts_list_user,name='accounts_list_user'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('common/',views.common,name='common'),
    path('get_doc/',views.get_doc,name='get_doc'),
    path('get_face/',views.get_face,name='get_face'),
    path('compare_faces/',views.compare_faces,name='compare_faces'),

]



