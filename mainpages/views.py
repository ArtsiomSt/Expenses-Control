import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import LoginForm, RegisrtaeForm, CreateCategory, CreateSpentForm
from .models import Categories, SpentModel, UserFromTg
from .serializers import UserFromTelegramSer, GetUserSpentSer



def homepage(request, time = datetime.datetime.now()):
    try:
        message = request.GET.get('message', '')
    except:
        message = ''
    if not request.user.is_authenticated:
        return redirect('login')
    allcats = Categories.objects.filter(user=request.user)
    users_spents = SpentModel.objects.filter(user=request.user).order_by('time_buyed')
    users_spents_day = SpentModel.objects.filter(Q(day_buyed__day=time.day) & Q(day_buyed__month=time.month) & Q(day_buyed__year=time.year) & Q(user=request.user))
    users_spents_month = SpentModel.objects.filter(Q(day_buyed__month=time.month) & Q(day_buyed__year=time.year) & Q(user=request.user))
    month_spents = count_price(users_spents_month)
    day_spents = count_price(users_spents_day)
    all_spents = count_price(users_spents)
    context = {
        'allcats':allcats,
        'users_spents': users_spents,
        'title': 'Mainpage',
        'message': message,
        'month_spents': month_spents,
        'day_spents':day_spents,
        'all_spents':all_spents,
    }
    return render(request, 'mainpages/HomePage.html', context)


def startlogin(request):
    message = '1'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            try:
                login(request,user)
                return redirect('home')
            except:
                message = 'Login is impossible'
    else:
        form = LoginForm()
    context = {
        'title': 'Вход',
        'form':form,
        'message': message,
    }
    return render(request, 'mainpages/Userlogin.html', context)


def registrate(request):
    message = ''
    if request.method == 'POST':
        form = RegisrtaeForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user = User.objects.create(username=username, password=password, email=email)
            login(request, user)
            print(user)
            default_cats = Categories.get_defoult_cats_list()
            for item in default_cats:
                Categories.objects.create(title=item, user=user)
            return redirect('home')
    else:
        form = RegisrtaeForm()
    context = {
        'message' : message,
        'form':form,
        'title': 'Registration',
    }
    return render(request, 'mainpages/UserReg.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


def addcat(request):
    message = ''
    if request.method == 'POST':
        form = CreateCategory(request.POST)
        if form.is_valid():
            title_for_cat:str = form.cleaned_data['title']
            user = request.user
            title_for_cat =title_for_cat.lower().capitalize()
            title_for_cat.capitalize()
            Categories.objects.create(title=title_for_cat, user=user)
            return redirect('home')
    else:
        form = CreateCategory()
    context = {
        'title': 'Addind Cat',
        'form':form,
    }
    return render(request, 'mainpages/addcategory.html', context)


def addspending(request):
    user = request.user
    if request.method == 'POST':
        form=CreateSpentForm(request.POST, q_id=user)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            price_for_unit = form.cleaned_data['price_for_unit']
            comment = form.cleaned_data['comment']
            category = form.cleaned_data['category']
            print(category)
            SpentModel.objects.create(title=title, amount=amount, price_for_unit=price_for_unit, comment=comment, category=Categories.objects.get(Q(title=category) & Q(user=user)), user=user)
            return redirect('home')
    else:
        form = CreateSpentForm(q_id=user)
    context = {
        'form':form,
        'title':'Adding Spendings',
    }
    return render(request, 'mainpages/addspending.html', context)


def spendings_by_cat(request, cat_name, time = datetime.datetime.now()):
    allcats = Categories.objects.filter(user=request.user)
    current_cat = get_object_or_404(Categories, Q(title=cat_name) & Q(user=request.user))
    users_spents = current_cat.spentmodel_set.all()
    day_spents_cat = current_cat.spentmodel_set.filter(Q(day_buyed__day=time.day) & Q(day_buyed__month=time.month) & Q(day_buyed__year=time.year) & Q(user=request.user))
    month_spents_cat = current_cat.spentmodel_set.filter(Q(day_buyed__month=time.month) & Q(day_buyed__year=time.year) & Q(user=request.user))
    all_spents = count_price(users_spents)
    day_spents = count_price(day_spents_cat)
    month_spents= count_price(month_spents_cat)
    context = {
        'allcats': allcats,
        'current_cat': current_cat,
        'users_spents': users_spents,
        'title': f'{current_cat} spents',
        'all_spents':all_spents,
        'day_spents':day_spents,
        'month_spents':month_spents,
    }
    return render(request, 'mainpages/HomePage.html', context)


def delete_spending(request, spending_pk):
    SpentModel.objects.filter(Q(user=request.user) & Q(pk=spending_pk)).delete()
    return redirect('home')


def delete_category(request, cat_pk):
    message = ''
    current_cat = Categories.objects.get(pk=cat_pk)
    try:
        Categories.objects.filter(pk=cat_pk).delete()
        message = f'Deleted category {current_cat.title}'
    except:
        message = 'Impossible to delete this category'
    return redirect(f'/?message={message}')


class LinkUserFromTg(APIView):
    def post(self, request):
        serializer = UserFromTelegramSer(data=request.POST)
        serializer.is_valid()
        print(serializer.data)
        user_for_linking = User.objects.get(username=serializer.data['username'])
        UserFromTg.objects.create(user=user_for_linking, tguserid=serializer.data['usertgid'])
        return Response({'answer':'success'})


class SendUserSpentsToTG(APIView):
    def get(self, request):
        print(request.query_params)
        if not 'usertgid' in request.query_params.keys():
            return Response({'answer':'You have to give users tgid'})
        try:
            user_from_tg = UserFromTg.objects.get(tguserid=request.query_params['usertgid'])
        except:
            return Response({'answer':'there is no such user'})
        serializer = GetUserSpentSer(SpentModel.objects.filter(user=user_from_tg.user), many=True)
        return Response({'answer':'success', 'spents':serializer.data})


def count_price(querysetSpent):
    spent = 0
    for item in querysetSpent:
        spent_on_that_item = item.amount*item.price_for_unit
        spent+=spent_on_that_item
    return spent
