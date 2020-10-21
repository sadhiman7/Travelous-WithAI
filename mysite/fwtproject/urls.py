"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('index', views.index, name='index'),
    path('tours', views.packages, name='tours'),
    path('tours/<int:id>', views.tourview, name='tourview'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('tours/book/<int:id>', views.book, name='book'),
    path('payment', views.payment, name="payment"),
    path('orders', views.orders, name='orders'),
    path('blog', views.blog, name='blog'),
    path('blog/<int:id>', views.blogview, name='blogview'),
    path('search', views.search, name='search'),
    path('searchblog', views.searchtour, name='searchtour'),
    path('aboutus', views.aboutus, name='aboutus')
]
