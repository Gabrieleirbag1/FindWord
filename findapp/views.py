# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from . import forms
from unidecode import unidecode
import csv, random, os, string
from django.db.models import Q

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
            'player1_text': game.player1_text,
            'player2_text': game.player2_text,
            'note': game.note,
            'player_note': game.player1_note if game.player1 == request.user.username else game.player2_note,
            'player_ready': game.player1_ready if game.player1 == request.user.username else game.player2_ready,
            'score': round(game.score * 2, 3)
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
        username = request.user.username
        action = request.POST.get('action')
        game = models.GameModel.objects.filter(room_name=room_name).first()
        
        if action == "FINDWORD":
            word = self.findword()
            game.word = word
            game.in_game_state = True
            RateGame(username, game, word)

        elif action == "RESULTS":
            game.in_game_state = False
            input_text = request.POST.get('input-text')
            if game.player1 == username:
                game.player1_text = input_text
            else:
                game.player2_text = input_text
            print("input_text", input_text)

        game.save()
        print("draco")
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
    
class RateGame():
    def __init__(self, username, game, word):
        self.username = username
        self.game = game
        self.word = unidecode(word).lower()

        self.note: int = 0
        self.player1 = User.objects.filter(username=self.game.player1).first()
        self.player2 = User.objects.filter(username=self.game.player2).first()

        self.local_rating()
        self.first_rating()

    def first_rating(self):
        if not self.game.player1_note or not self.game.player2_note:
            self.game.player1_note = 3
            self.game.player2_note = 3
            self.note = (self.game.player1_note + self.game.player2_note) // 2
            self.game.note = self.note
    
    def local_rating(self):
        if self.game.player1_note and self.game.player2_note:
            self.note = (self.game.player1_note + self.game.player2_note) // 2
            self.game.note = self.note
            if self.game.note:
                if not self.check_relationship_exists():
                    self.create_relationship()
                self.friend_rating()
            self.game.score = self.note / 2
            print("note", self.note, self.username)
        else:
            return

    def check_relationship_exists(self):
        relation1 = models.FriendsModel.objects.filter(user1=self.player1, user2=self.player2)
        relation2 = models.FriendsModel.objects.filter(user1=self.player2, user2=self.player1)
        if relation1.exists() or relation2.exists():
            return True
        return False
    
    def create_relationship(self):
        models.FriendsModel.objects.create(user1=self.player1, user2=self.player2)

    def friend_rating(self):
        if models.FriendsModel.objects.filter(user1=self.player1, user2=self.player2).exists():
            relationship = models.FriendsModel.objects.filter(user1=self.player1, user2=self.player2).first()
        elif models.FriendsModel.objects.filter(user1=self.player2, user2=self.player1).exists():
            relationship = models.FriendsModel.objects.filter(user1=self.player2, user2=self.player1).first()
        else:
            print("Relationship does not exists")
        if self.caclulate_score():
            relationship.score += self.note
            relationship.save()
            print("relationship", relationship.score)

    def caclulate_score(self) -> bool:
        player1_text: list[str] = unidecode(self.game.player1_text).lower().split()
        player2_text: list[str] = unidecode(self.game.player2_text).lower().split()

        if self.word in player1_text or self.word in player2_text:
            self.note = -1
            return False
        
        elif not self.game.player1_text or not self.game.player2_text:
            self.note = -1
            return False
        
        elif self.game.player1_text.isspace() or self.game.player2_text.isspace():
            self.note = -1
            return False
        
        elif unidecode(self.game.player1_text).lower() == self.word or unidecode(self.game.player2_text).lower() == self.word:
            self.note = -1
            return False
        
        else:
            total_bonus = 0
            if self.note < 3:
                bonus = 0.2
            elif self.note < 5:
                bonus = 0.25
            else:
                bonus = 0.35 

            for word in player1_text:
                if word in player2_text:
                    total_bonus += bonus
            
            self.note += total_bonus * self.note

            if player1_text == player2_text:
                self.note += len(player1_text)
            
            print("note", self.note, "AAAAAAAAAAAAAAAAAAAAAA", total_bonus, len(player1_text))
            return True
        
class LobbyView(View):
    def get(self, request):
        self.get_best_friend(request)
        error = request.session.pop('error', None)
        context = {
            'error': error,
            'best_friend': request.session.get('best_friend')
        }
        return render(request, 'lobby.html', context)
    
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
            room_name = request.POST.get('name')
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
            
    def get_best_friend(self, request):
        if request.user.is_authenticated:
            best_friend = models.FriendsModel.objects.filter(
                Q(user1=request.user) | Q(user2=request.user)
            ).order_by('-score').first()
            
            if best_friend:
                request.session['best_friend'] = best_friend.user1.username if best_friend.user1 != request.user else best_friend.user2.username
            else:
                request.session['best_friend'] = None
        else:
            request.session['best_friend'] = None
    
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
        if request.user.is_authenticated:
            return redirect('lobby')
        else:
            error = request.session.pop('error', None)
            return render(request, 'login.html', {'error': error})

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'lobby')
                return redirect(next_url)
            else:
                request.session['error'] = 'Invalid credentials'
                return redirect('login')
            
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('lobby')

def bug_report(request):
    if request.method == 'POST':
        form = forms.BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.user = request.user
            bug.save()
            referer = request.META.get('HTTP_REFERER', "/")
            return redirect(referer)
    else:
        form = forms.BugForm()
    referer = request.META.get('HTTP_REFERER', "/")
    return redirect(referer)

def friends(request):
    colors = ["blue", "red", "cyan", "green", "yellow", "purple", "pink", "dark-blue", "fuchsia", "dark-green", ""]
    friends = models.FriendsModel.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by('-score')
    for friend in friends:
        friend.color = random.choice(colors)
    return render(request, 'friends.html', {'friends': friends})

