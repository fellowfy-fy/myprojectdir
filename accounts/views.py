from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from authentication.models import User
from django.contrib import messages
from django.http import Http404, HttpResponse
from .forms import OrderCreateForm, UserCreateForm, LoginForm, CarCreateForm, AnswerCreateForm
from .models import Car, Order, Answer
import logging

logger = logging.getLogger(__name__)

def get_list_or_default(klass, *args, **kwargs):
    try:
        return get_list_or_404(klass, *args, **kwargs)
    except Http404:
        return [] 

def start_page(request):
    return render(request, 'start.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_phone_number = form.cleaned_data['phone_number']
            user_password = form.cleaned_data['password1']

            #Create user
            user = User.objects.create_user(phone_number=user_phone_number, password=user_password)

            user.is_active = True
            
            
            return redirect("/user-login")
    else:
        form = UserCreateForm()
    return render(request, 'user_register.html', {'form': form})



def user_login(request):
    
    form = LoginForm()
    
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        
        phone_number = request.POST.get('username', False)
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else: 
            messages.info(request, 'Username or password is incorrect')
            return redirect('/user-login')
    
    context = {
        'form': form
    }
    
    return render(request, 'user_login.html', context)


def logout_user(request):
    logout(request)
    return redirect('accounts:dashboard')


@login_required(login_url="accounts:user-login")
def dashboard(request):
    cars = get_list_or_default(Car, user = request.user)
    return render(request, 'dashboard.html', {'cars': cars})

@login_required(login_url="accounts:user-login")
def add_order(request):
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('accounts:add-order-confirm')
    else:
        cars = get_list_or_default(Car, user=request.user)
        first_car = cars[0] if cars else None
        form = OrderCreateForm(user=request.user, initial={'car': first_car.id if first_car else None})
        
    context = {
        'form': form,
        'cars': cars
    }
    
    return render(request, 'add_order.html', context)

@login_required(login_url="accounts:user-login")
def add_car(request):
    
    form = CarCreateForm()
    
    if request.method == 'POST':
        form = CarCreateForm(request.POST, request.FILES)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = request.user
            Car.objects.create(user = owner.user, brand=owner.brand, model=owner.model, vin=owner.vin, car_image=owner.car_image)
            return redirect('accounts:add-car-confirm')
    
    return render(request, 'add_car.html', {'form': form})

@login_required(login_url="accounts:user-login")
def list_orders(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, 'list_orders.html', {'orders': orders})

@permission_required('accounts.view_order')
@login_required(login_url="accounts:user-login")
def answer_to_orders(request):
    orders = Order.objects.filter(answer=None)
    return render(request, 'answer_to_orders.html', {'orders': orders})

def add_car_confirm(request):
    return render (request, 'add_car_confirm.html')
    
def add_order_confirm(request):
    return render (request, 'add_order_confirm.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')


@permission_required('accounts.view_order')
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    form = AnswerCreateForm()
    
    if request.method == 'POST':
        form = AnswerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.order = order
            answer.user = request.user
            answer.save()
            order.answer = answer
            order.save()
            return redirect('accounts:answer-to-orders')
    
    
    return render(request, 'order_detail.html', {'order': order, 'form': form})

def tuning(request):
    return render(request, 'tuning.html')