import random

from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from .models import Duck, Auction, Player
from .serializers import DuckSerializer, AuctionSerializer

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods  # Ensure this line is present
from rest_framework.decorators import api_view


class DuckViewSet(viewsets.ModelViewSet):
    queryset = Duck.objects.all()
    serializer_class = DuckSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

def home(request):
    player = Player.objects.get(user=request.user)
    active_auctions = Auction.objects.filter(end_time__gt=timezone.now())
    return render(request, 'home.html', {'player': player, 'auctions': active_auctions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  
    
def profile(request):
   
    auctions = Auction.objects.filter(owner=request.user)
  
    ducks = Duck.objects.filter(auction__in=auctions).distinct()
    return render(request, 'profile.html', {'ducks': ducks, 'user': request.user})
@require_http_methods(["GET"])
def user_delete(request):
    user = request.user
    # Ensure the request is a POST request (assuming you are submitting form data)
    if request.method == 'POST':
        data = request.POST  # Use request.POST for form data
       

        allowed_fields = {'username', 'email'}
        updated_fields = {key: data[key] for key in data if key in allowed_fields}

        if updated_fields:
            for field, value in updated_fields.items():
                setattr(user, field, value)
            user.save()
    return redirect('login') 

# @api_view(['PUT'])
def modify_user(request):
    user = request.user
    # password=request.password
    print(user,
           'yesi papicho')

    # Ensure the request is a POST request (assuming you are submitting form data)
    # if request.method == 'POST':
    #     data = request.POST  # Use request.POST for form data

    #     allowed_fields = {'username', 'email'}
    #     updated_fields = {key: data[key] for key in data if key in allowed_fields}

    #     if updated_fields:
    #         for field, value in updated_fields.items():
    #             setattr(user, field, value)
    #         user.save()
        
    return render(request, 'userModify.html')
        
    
    
    
def spin_duck(request):
    if request.method == 'POST':
      
        ducks = Duck.objects.all()

       
        rarity_weights = {
            'C': 50,  
            'R': 30,  
            'SR': 15,  
            'UR': 4,  
            'SUR': 1   
        }

        
        weighted_ducks = []
        for duck in ducks:
            weighted_ducks.extend([duck] * rarity_weights[duck.rarity])

        # Выбираем случайную уточку
        selected_duck = random.choice(weighted_ducks)

        return render(request, 'spin_result.html', {'duck': selected_duck})

    return render(request, 'spin.html')

def place_bid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    player = Player.objects.get(user=request.user)
    bid_amount = float(request.POST['bid_amount'])
    
    if bid_amount <= auction.current_bid or player.currency < bid_amount:
        return JsonResponse({'error': 'Invalid bid'}, status=400)

    # Update highest bid and bidder
    auction.current_bid = bid_amount
    auction.highest_bidder = player
    auction.save()

    return JsonResponse({'success': 'Bid placed successfully!', 'current_bid': auction.current_bid})



def roll_gacha(request):
    player = Player.objects.get(user=request.user)
    if player.currency < 10:
        return JsonResponse({'error': 'Not enough currency'}, status=400)
    
    player.currency -= 10
    player.save()

    # Gacha logic based on rarity probabilities
    roll = random.random()
    if roll < 0.0005:
        rarity = 'SUR'
    elif roll < 0.005:
        rarity = 'UR'
    elif roll < 0.05:
        rarity = 'SR'
    elif roll < 0.40:
        rarity = 'R'
    else:
        rarity = 'C'

    gacha = gacha.objects.filter(rarity=rarity).order_by('?').first()
    player.collection.add(gacha)
    return JsonResponse({'result': f'You got a {gacha.name}!', 'currency': player.currency})