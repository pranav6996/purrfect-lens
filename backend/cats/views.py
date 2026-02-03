import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CatBreed
from .ml_utils import predict_breed_from_image

CAT_FACTS = [
    "Cats spend 70% of their lives sleeping.",
    "A cat's ear has 32 muscles.",
    "Cats can rotate their ears 180 degrees.",
    "The hearing of the average cat is at least five times keener than that of a human adult.",
    "In the largest cat breed, the average male weighs approximately 20 pounds.",
    "Domestic cats spend about 70 percent of the day sleeping and 15 percent of the day grooming.",
    "Cats cannot taste sweetness.",
    "A group of kittens is called a kindle, and a group of cats is called a clowder.",
    "Cats have a third eyelid called the 'haw' to protect their eyes.",
    "The first cat in space was a French cat named Felicette (a.k.a. 'Astrocat') in 1963.",
    "They walk like camelsBoth right legs move, then both left. It’s called a pacing gait. Super quiet stalking mode.",
    "If a cat slow-blinks at you, that’s a love signal. Return it.",
]

def index(request):
    fact = random.choice(CAT_FACTS)
    return render(request, 'index.html', {'fact': fact})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def breed_list(request):
    breeds = CatBreed.objects.all().order_by('name')
    return render(request, 'breeds_list.html', {'breeds': breeds})

@api_view(['POST'])
@permission_classes([AllowAny]) 
def predict_breed(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)
    
    image_file = request.FILES['image']
    result = predict_breed_from_image(image_file)
    
    if result:
        try:
            breed_info = CatBreed.objects.get(name=result['breed'])
            result['details'] = {
                'origin': breed_info.origin,
                'description': breed_info.description,
                'health': breed_info.health_info,
                'habits': breed_info.habits,
                'food': breed_info.food_recommendations
            }
        except CatBreed.DoesNotExist:
            result['details'] = None
            
        return Response(result)
    else:
        return Response({'error': 'Prediction failed'}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_random_fact(request):
    return Response({'fact': random.choice(CAT_FACTS)})
