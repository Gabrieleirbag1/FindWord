# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models
from . import forms
import csv, random, os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import string
import random

class GameView(View):
    def __init__(self) -> None:
        self.words = self.open_csv()
        pass

    def get(self, request, room_name):
        if not self.check_room_exists(room_name):
            request.session['error'] = 'Game does not exist'
            return redirect('lobby')
        
        if self.update_name_player(room_name, request.user.username):
            game = models.GameModel.objects.filter(room_name=room_name).first()
            context = {
            'room_name': room_name,
            'word': game.word,
            'in_game_state': game.in_game_state,
            'player1': game.player1,
            'player2': game.player2,
            }
            if self.check_name_player(room_name, request.user.username):
                return render(request, 'room.html', context)
            else:
                request.session['error'] = 'You\'re not allowed to join this game'
                return redirect('lobby')
        else:
            request.session['error'] = 'You\'re not allowed to join this game'
            return redirect('lobby')

    def post(self, request, room_name):
        action = request.POST.get('action')
        game = models.GameModel.objects.filter(room_name=room_name).first()
        
        if action == "FINDWORD":
            word = self.findword()
            game.word = word
            game.in_game_state = True

        elif action == "RESULTS":
            game.in_game_state = False

        game.save()
        return redirect('room', room_name=room_name)


    def open_csv(self):
        csv_path = "dictionary/fr/noun.csv"
        full_path = os.path.join(os.path.dirname(__file__), csv_path)
        
        with open(full_path) as f:
            reader = csv.reader(f)
            words = list(reader)
        return words

    def findword(self):
        word = random.choice(self.words)[0]
        print(word)
        return word
    
    def check_room_exists(self, room_name):
        return models.GameModel.objects.filter(room_name=room_name).exists()
    
    def update_name_player(self, room_name, username):
        game = models.GameModel.objects.filter(room_name=room_name).first()
        if game.player1 is None:
            game.player1 = username
            game.save()
            return True
        elif game.player2 is None:
            if not game.player1 == username:
                game.player2 = username
                game.save()
                return True
            else:
                return False
        else:
            return True
        
    def check_name_player(self, room_name, username):
        game = models.GameModel.objects.filter(room_name=room_name).first()
        if game.player1 == username or game.player2 == username:
            return True
        return False
    
class LobbyView(View):
    def get(self, request):
        error = request.session.pop('error', None)
        return render(request, 'lobby.html', {'error': error})
    
    def post(self, request):
        action = request.POST.get('action')
        if action == 'CREATE':
            player1 = None
            player2 = None
            word = request.POST.get('word') or ''
            room_name = self.generate_random_url(10)
            while self.check_room_exists(room_name):
                room_name = self.generate_random_url(10)
            game = models.GameModel.objects.create(player1=player1, player2=player2, word=word, room_name=room_name)
            if game:
                return redirect('room', room_name=room_name)
            else:
                request.session['error'] = 'Error creating game'
                return redirect('lobby')
        else:
            room_name = request.POST.get('room_name')
            try:
                room_name = room_name.split('room/')[1].strip("/")
            except IndexError:
                pass
            game = models.GameModel.objects.filter(room_name=room_name).first()
            if game:
                return redirect('room', room_name=room_name)
            else:
                request.session['error'] = 'Error joining room'
                return redirect('lobby')
    
    def generate_random_url(self, length):
        characters = string.ascii_letters + string.digits + '_'
        url = ''.join(random.choice(characters) for _ in range(length))
        return url
    
    def check_room_exists(self, room_name):
        return models.GameModel.objects.filter(room_name=room_name).exists()
    
class RegisterView(View):
    def get(self, request):
        error = request.session.pop('error', None)
        return render(request, 'register.html', {'error': error})
    
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    request.session['error'] = 'Username already exists'
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return redirect('login')
            else:
                request.session['error'] = 'Passwords do not match'
                return redirect('register')
        else:
            request.session['error'] = 'Invalid request'
            return redirect('register')
    
class LoginView(View):
    def get(self, request):
        error = request.session.pop('error', None)
        return render(request, 'login.html', {'error': error})

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('lobby')
            else:
                request.session['error'] = 'Invalid credentials'
                return redirect('login')
            
def logout_user(request):
    logout(request)
    return redirect('lobby')