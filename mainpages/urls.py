from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', startlogin, name='logining'),
    path('register/', registrate, name='reg'),
    path('', homepage, name='home'),
    path('logout/', logoutuser, name='logout'),
    path('addcategory/', addcat, name='addcat'),
    path('addspending/', addspending, name='addspent'),
    path('spendings/<str:cat_name>', spendings_by_cat, name='spendings'),
    path('delspending/<int:spending_pk>', delete_spending, name='deletespending'),
    path('delcategory/<int:cat_pk>', delete_category, name='deletecat'),
]
