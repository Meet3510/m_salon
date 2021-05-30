from django.urls import path,include
from django.contrib import admin
from . import views
from gallery import views as gallery_views
from contact import views as contact_views
from services import views as services_views
from home import views as home_views

urlpatterns = [
       path('appoinment/', views.appoinment ,name='appoinment'),
       path('handlerequst/', views.handlerequest, name='handlerequest'),
       path('bill/', views.bill, name='bill'),
       path('payment/', views.payment, name='payment')

]
