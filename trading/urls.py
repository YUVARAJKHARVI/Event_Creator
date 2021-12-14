from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('',views.home,name="home"),
    path('User',views.log, name="log"),
    path('signin/',views.signin, name="signin"),
    path('',views.add_idea, name="add_idea"),
    path('log_out/',views.log_out, name="log_out"),
    path('my_idea/',views.my_idea, name="my_idea"),
    #path('search/',views.youtube_search, name="search"),
    path('calendar/<delete_event_id>/',views.delete_event, name="delete_event"),
    path('calendar/update/<update_event_id>/',views.update_event, name="update_event"),

    path('calendar/',views.calender_view, name="calender"),
    ##

    path('calendar/my_events/',views.my_events, name="my_events"),
    path('log_in/',views.log_in, name="log_in"),
    path('sign_out/',views.sign_out, name="sign_out"),
    path('register/',views.register, name="register"),

    



]
