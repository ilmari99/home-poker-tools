from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PokerTransactionForm

def calculate_poker_transactions(start_blinds, end_blinds):
    # (The function remains unchanged)
    assert len(start_blinds) == len(end_blinds), "The number of players must be the same"
    assert sum(start_blinds) == sum(end_blinds), "The total number of blinds must be the same"
    
    net_blinds = [end - start for start, end in zip(start_blinds, end_blinds)]
    creditors = [(i, net) for i, net in enumerate(net_blinds) if net > 0]
    debtors = [(i, -net) for i, net in enumerate(net_blinds) if net < 0]
    
    transactions = []
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor_index, credit_amount = creditors[i]
        debtor_index, debt_amount = debtors[j]
        transaction_amount = min(credit_amount, debt_amount)
        transactions.append((debtor_index, creditor_index, transaction_amount))
        
        creditors[i] = (creditor_index, credit_amount - transaction_amount)
        debtors[j] = (debtor_index, debt_amount - transaction_amount)
        
        if creditors[i][1] == 0:
            i += 1
        if debtors[j][1] == 0:
            j += 1
    return transactions

def index(request):
    if request.method == 'POST':
        form = PokerTransactionForm(request.POST)
        if form.is_valid():
            bought_blinds = [float(x) for x in form.cleaned_data['bought_blinds'].split(',')]
            end_blinds = [float(x) for x in form.cleaned_data['end_blinds'].split(',')]
            player_names = form.cleaned_data['player_names'].split(',') if form.cleaned_data['player_names'] else [f'Player{i}' for i in range(len(bought_blinds))]
            if len(player_names) != len(bought_blinds):
                form.add_error(None, "The number of player names must match the number of blinds.")
                return render(request, 'debt_setter/index.html', {'form': form})
            big_blind = form.cleaned_data['big_blind']
            
            try:
                transactions = calculate_poker_transactions(bought_blinds, end_blinds)
                request.session['transactions'] = transactions
                request.session['player_names'] = player_names
                request.session['big_blind'] = float(big_blind) if big_blind else None
                return redirect(reverse('results'))
            except AssertionError as e:
                form.add_error(None, str(e))
    else:
        form = PokerTransactionForm()
    
    return render(request, 'debt_setter/index.html', {'form': form})

def results(request):
    transactions = request.session.get('transactions', [])
    player_names = request.session.get('player_names', [])
    big_blind = request.session.get('big_blind', None)
    
    formatted_transactions = []
    for debtor, creditor, amount in transactions:
        transaction = {
            "from": player_names[debtor],
            "to": player_names[creditor],
            "amount_in_blinds": amount
        }
        if big_blind:
            transaction["amount_in_euros"] = round(amount * float(big_blind), 2)
        formatted_transactions.append(transaction)
    
    return render(request, 'debt_setter/results.html', {'transactions': formatted_transactions})
