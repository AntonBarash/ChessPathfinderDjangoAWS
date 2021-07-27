from django import forms

class PlayerForm(forms.Form):
    player1id = forms.CharField(label='player1')
    player2id = forms.CharField(label='player2')
