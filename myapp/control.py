from django.urls import path
from . import views
app_name="myapp"
urlpatterns=[
    path("",views.Home.as_view(),name='home'),
    path('login',views.Logins.as_view(),name='signin'),
path('signup',views.Signup.as_view(),name='signup'),
    path("home",views.myhome,name='userhome'),
    path("home/post",views.Addpost.as_view(),name='post'),
    path("home/post/<slug:slug>", views.Updatepost.as_view(), name='update'),
path("home/post/<int:pk>/remove", views.Delpost.as_view(), name='delete'),
path("home/package",views.Addpack.as_view(),name='package'),
    path("home/package/<int:pk>", views.Updatepack.as_view(), name='updatepack'),
path("home/package/<int:pk>/remove", views.Delpack.as_view(), name='deletepack'),
path("package",views.Pack.as_view(),name="packdisplay"),
path("search",views.Plannerpost.as_view(),name='search')

]
