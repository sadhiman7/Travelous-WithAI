from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tours, PlaceToVisit, HowToReach, Bookings, blogs, comments
from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as signin, logout
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import numpy as np
import pandas as pd
import scipy.sparse
from scipy.spatial.distance import correlation

data=pd.read_csv('data_collaborative.csv')
placeInfo=pd.read_csv('data_content.csv')

data=pd.merge(data, placeInfo, left_on='itemId', right_on="itemId")
userIds=data.userId
userIds2=data[['userId']]

data.loc[0:10,['userId']]
data=pd.DataFrame.sort_values(data, ['userId','itemId'], ascending=[0,1])

metadata = pd.read_csv('data_content.csv', low_memory=False)
C = metadata['p_rating'].mean()
m = metadata['count'].quantile(0.75)

def weighted_rating(x, m=m, C=C):
    v = x['count']
    R = x['p_rating']
    return (v/(v+m) * R) + (m/(m+v) * C)

metadata['score'] = metadata.apply(weighted_rating, axis=1)

metadata = metadata.sort_values('score', ascending=False)

def favoritePlace(activeUser,N):
    topPlace=pd.DataFrame.sort_values(data[data.userId==activeUser],['rating'],ascending=[0])[:N]
    return list(topPlace.title)

userItemRatingMatrix=pd.pivot_table(data, values='rating', index=['userId'], columns=['itemId'])

def similarity(user1,user2):
    #print(user1, user2)
    try:
        user1=np.array(user1)-np.nanmean(user1)
        user2=np.array(user2)-np.nanmean(user2)
        commonItemIds=[i for i in range(len(user1)) if user1[i]>0 and user2[i]>0]
        #print(commonItemIds)
        if len(commonItemIds)==0:
           return 0
        else:
           user1=np.array([user1[i] for i in commonItemIds])
           user2=np.array([user2[i] for i in commonItemIds])
           #print(user1, user2)
           #print(correlation(user1, user2))
           return correlation(user1,user2)

    except ZeroDivisionError:
        print("You can't divide by zero!")

def nearestNeighbourRatings(activeUser,K):
    try:
        similarityMatrix=pd.DataFrame(index=userItemRatingMatrix.index,columns=['Similarity'])
        for i in userItemRatingMatrix.index:
            similarityMatrix.loc[i]=similarity(userItemRatingMatrix.loc[activeUser],userItemRatingMatrix.loc[i])
        #print(similarityMatrix)
        similarityMatrix=pd.DataFrame.sort_values(similarityMatrix,['Similarity'],ascending=[0])
        #print(similarityMatrix)
        nearestNeighbours=similarityMatrix[:K]
        #print(nearestNeighbours)
        neighbourItemRatings=userItemRatingMatrix.loc[nearestNeighbours.index]
        #print(neighbourItemRatings)
        predictItemRating=pd.DataFrame(index=userItemRatingMatrix.columns, columns=['Rating'])
        #print(predictItemRating)
        for i in userItemRatingMatrix.columns:
            predictedRating=np.nanmean(userItemRatingMatrix.loc[activeUser])
            #print(predictedRating)
            for j in neighbourItemRatings.index:
                if userItemRatingMatrix.loc[j,i]>0:
                   predictedRating += (userItemRatingMatrix.loc[j,i]-np.nanmean(userItemRatingMatrix.loc[j]))*nearestNeighbours.loc[j,'Similarity']
            predictItemRating.loc[i,'Rating']=predictedRating
    except ZeroDivisionError:
        print("You can't divide by zero!")
    return predictItemRating


def topNRecommendations(activeUser,N):
    try:
        predictItemRating = nearestNeighbourRatings(activeUser,10)
        placeAlreadyWatched = list(userItemRatingMatrix.loc[activeUser].loc[userItemRatingMatrix.loc[activeUser]>0].index)
        predictItemRating = predictItemRating.drop(placeAlreadyWatched)
        topRecommendations = pd.DataFrame.sort_values(predictItemRating, ['Rating'],ascending=[0])[:N]
        topRecommendationTitles = (placeInfo.loc[placeInfo.itemId.isin(topRecommendations.index)])
    except ZeroDivisionError:
        print("You can't divide by zero!")
    return list(topRecommendationTitles.title)

def index(request):
    user = request.user
    print(user.id)
    recommended = topNRecommendations(user.id,3)
    tours = Tours.objects.filter(destination__in = recommended)
    print(tours)
    n = len(tours)
    print(tours[0].destination)
    nCards = n // 4 + ceil((n / 4) - (n // 4))
    print(tours[0].image)
    blog=blogs.objects.all()
    params = {'tours': tours, 'no_of_slides': nCards, 'nPages':range(nCards), 'blog':blog }
    return render(request, "index.html", params)

def packages(request):
    tours = Tours.objects.all()
    nPages = tours.count()//6 + 1
    paginator = Paginator(tours, 6)
    page=request.GET.get('page')
    tours = paginator.get_page(page)
    print(tours)
    n = len(tours)
    print(tours[0].destination)
    nCards = n // 4 + ceil((n / 4) - (n // 4))
    print(tours[0].image)
    params = {'tours': tours, 'no_of_slides': nCards, 'nPages': range(nPages)}
    return render(request, "packages.html", params)


def tourview(request, id):
    tour = Tours.objects.filter(id=id)
    tour = tour[0]
    dest = tour.destination
    ptv = PlaceToVisit.objects.filter(destination=dest)
    print(ptv)
    print(tour)
    htr = HowToReach.objects.filter(destination=dest)
    temp = tour.category
    simtours = Tours.objects.filter(Q(category=temp) & ~Q(destination=tour.destination))
    print(simtours)
    return render(request, "single-tour.html", {'tour':tour, 'ptv':ptv, 'htr':htr, 'stour': simtours})


def login(request):
    user = request.user
    print(user.id)
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user:
            signin(request, user)
            return redirect(index)
        else:
            return render(request, 'login.html', {'error': "Invalid Credentials!"})
    else:
        return render(request, 'login.html')


def signout(request):
    logout(request)
    return redirect(login)


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username = request.POST['email'])
            return render(request, 'signup.html', {'error': "User Already Exists!"})
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['email'], email=request.POST['email'],
                                            password=request.POST['password'], first_name=request.POST['fname'], last_name=request.POST['lname'])
            return redirect(login)

    else:
        return render(request, 'signup.html')


def book(request, id):
    if request.method == "POST":
        tour = Tours.objects.filter(id=id)
        tour = tour[0]
        user=request.user
        date = request.POST['bookingdate']
        na = request.POST['na']
        nc = request.POST['nc']
        email = user.email
        currdate = datetime.now()

        booking_instance = Bookings.objects.create(email=email, destination=tour.destination, bookingdate=date, dob=currdate, adults=na, children=nc)

        return redirect(payment)

    else:
        tour = Tours.objects.filter(id=id)
        tour = tour[0]
        user=request.user
        params= {'tour':tour, 'User':user}
        return render(request, "book.html", params)

def payment(request):

    user=request.user
    email = user.email
    booking = Bookings.objects.last()
    print(booking)
    #booking = booking[-1]
    tour = Tours.objects.filter(destination=booking.destination)
    tour = tour[0]
    print(booking.adults)
    tprice = booking.adults*tour.price + (booking.children*tour.price)/2


    return render(request, 'payment.html', {'price':tprice})


def orders(request):
    email =request.user.email
    bookings = Bookings.objects.filter(email=email)
    params = {'bookings':bookings}
    return render(request, 'orders.html', params)

def blog(request):
    blog = blogs.objects.all()
    nPages = blog.count()//5 + 1
    paginator = Paginator(blog, 5)
    top4blogs = blogs.objects.order_by('-nViews')[:4]
    page = request.GET.get('page')
    blog = paginator.get_page(page)
    params = {'blogs':blog, 'nPages': range(nPages), 't4b':top4blogs}
    return render(request, 'blog.html', params)


def blogview(request, id):
    blog = blogs.objects.get(id=id)
    if request.method == "POST":
        name = request.user.first_name + " " + request.user.last_name
        message = request.POST['message']
        commentadd = comments.objects.create(body=message, author=name, blogid=blog)

    blogid = blog.id
    blog.nViews = blog.nViews + 1
    blog.save()
    comment = comments.objects.filter(blogid=blogid)
    nComm = comment.count()
    top4blogs = blogs.objects.order_by('-nViews')[:4]
    return render(request, "single-blog.html", {'blog':blog, 'comment':comment,  't4b':top4blogs, 'nComm':nComm})

def search(request):
    query = request.GET.get('a')
    print(query)
    params= {}

    tourresults = Tours.objects.filter(Q(destination__icontains=query) | Q(about__icontains=query))
    print(tourresults)
    if tourresults:
        temp=tourresults[0].category
        simtours = Tours.objects.filter(Q(category=temp) & ~Q(destination=tourresults[0].destination))
        print(simtours)
        params['stour']=simtours

    params['tour']=tourresults
    print(params)
    return render(request, 'search.html', params)


def searchtour(request):
    query = request.GET.get('query')
    blog = blogs.objects.filter(Q(title__icontains=query) | Q(destination__icontains=query))
    nPages = blog.count() // 5 + 1
    paginator = Paginator(blog, 5)
    top4blogs = blogs.objects.order_by('-nViews')[:4]
    page = request.GET.get('page')
    blog = paginator.get_page(page)
    params = {'blogs': blog, 'nPages': range(nPages), 't4b': top4blogs}
    return render(request, 'searchtour.html', params)

def aboutus(request):
    return render(request, 'about-us.html')

