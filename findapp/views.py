# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models
import csv, random, os

class Game(View):
    def __init__(self) -> None:
        self.words = self.open_csv()
        pass

    def get(self, request, id):
        word = request.session.pop('word', None)
        game_instance = get_object_or_404(models.GameModel, id=id)
        return render(request, 'game.html', {'word': word})

    def post(self, request, id):
        word = self.findword()
        request.session['word'] = word
        return redirect('game', id=id)
    
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

class Lobby(View):
    def get(self, request):
        return render(request, 'lobby.html')
    
    def post(self, request):
        player1 = request.POST.get('player1') or ''
        player2 = request.POST.get('player2') or ''
        word = request.POST.get('word') or ''

        game = models.GameModel.objects.create(player1=player1, player2=player2, word=word)

        return redirect('game', id=game.id)