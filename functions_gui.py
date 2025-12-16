

def calc_balance(income, expenses):
    balance = income - expenses
    return balance

def financial_status(balance):
    """
    Returns a status string instead of printing.
    This is necessary for a GUI.
    """
    if balance > 0:
        return "Great! You are saving money!"
    elif balance == 0:
        return "You are breaking even."
    else:
        return "**WARNING** You are overspending!"