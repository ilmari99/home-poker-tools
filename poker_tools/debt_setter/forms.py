from django import forms
from django.core.validators import MinValueValidator

class PokerTransactionForm(forms.Form):
    bought_blinds = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g. 100, 150, 200',
            'title': 'The total number of big blinds bought. This includes all the big blinds the player has bought during the game, buy-ins, and re-buys.'
        })
    )
    end_blinds = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g. 90, 160, 200',
            'title': 'The total number of big blinds each player has at the end of the game.'
        })
    )
    player_names = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g. Alice, Bob, Charlie',
            'title': 'The names of the players. Separate the names with commas. If left empty, the players will be named Player1, Player2, ...'
        }),
        required=False
    )

    big_blind = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Big Blind (Optional)',
            'title': 'The value of the big blind. If left empty, the transactions will only be calculated in terms of big blinds.'
            }),
        required=False,
        validators=[MinValueValidator(0)]
    )
