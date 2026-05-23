import math

class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name
    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description' : description})
        
    def withdraw(self, amount, description=''):
        if not self.check_funds(amount):
            return False
        else:
            self.ledger.append({'amount': -amount, 'description' : description})
            return True

    def get_balance(self):
        return sum(entry['amount'] for entry in self.ledger)

    def transfer(self, amount, destination):
        if not self.check_funds(amount):
            return False
        else: 
            self.withdraw(amount, f"Transfer to {destination.name}")
            destination.deposit(amount, f"Transfer from {self.name}")
            return True
    
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True
        if amount < self.get_balance():
            return True
        else:
            return False

    def __str__(self):
        title = self.name.center(30, '*')
        balance = self.get_balance()
        lines = []
        for ledger in self.ledger:
            lines.append(f'{ledger["description"][:23]:<23}{ledger["amount"]:>7.2f}')
        items = '\n'.join(lines)
        return f'{title}\n{items}\nTotal: {balance:.2f}' 
        

def create_spend_chart(categories):
    title = "Percentage spent by category"
    total_spent = 0
    percentage_spent = []
    rows = []
    footer = '    ' + '-' * (len(categories)*3+1)
    max_name = max(len(category.name) for category in categories)
    row_name = '     '
    name_rows = []
    for category in categories:
        for entry in category.ledger:
            if entry['amount'] < 0:
                total_spent += abs(entry['amount'])
    for category in categories:
        withdrawal_total = 0
        
        for entry in category.ledger:
            if entry['amount'] < 0:
                withdrawal_total += abs(entry['amount'])
        percentage = math.floor(withdrawal_total/total_spent * 100/10) * 10
        percentage_spent.append(percentage)
    for i in range(100, -1, -10):
        row = f'{i:>3}|'
        for percent in percentage_spent:
            if percent >= i:
                row += ' o '
            else:
                row += '   '
        rows.append(row + ' ')
    for i in range(max_name):
        name_row = '     '
        for category in categories:
            if i < len(category.name):
                name_row += category.name[i] + '  '
            else:
                name_row += '   '
        name_rows.append(name_row)
    rows = '\n'.join(rows)
    name_rows = '\n'.join(name_rows)
    return f'{title}\n{rows}\n{footer}\n{name_rows}'

food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert' )
clothing = Category('Clothing')
food.transfer(50, clothing)
auto = Category('Auto')
auto.deposit(1000, 'initial deposit')
auto.withdraw(33.40, 'gasoline')
child_care = Category('Child care')
child_care.deposit(1000, 'initial deposit')
child_care.withdraw(100, 'day-care')

print(food)
print(create_spend_chart([food, clothing, auto, child_care]))