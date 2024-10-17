from django import forms

class PokerTransactionForm(forms.Form):
    start_blinds = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 100, 150, 200'}))
    end_blinds = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 90, 160, 200'}))
    player_names = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alice, Bob, Charlie'}), required=False)
    big_blind = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Big Blind (Optional)'}), required=False)
