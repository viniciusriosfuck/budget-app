class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
    
    def __str__(self):
        title = self.category.center(30, "*")
        transactions_str = '\n'
        for transaction in self.ledger:
            transactions_str = (
                transactions_str
                + transaction["description"][:23].ljust(23)
                + f'{transaction["amount"]:.2f}'.rjust(7)
                + '\n'
            )
        total_str = f'Total: {self.get_balance():.2f}'
        
        out_str = title + transactions_str + total_str

        return out_str

    def get_balance(self):
        return sum([x["amount"] for x in self.ledger])
    
    def check_funds(self, amount):
        return False if amount > self.get_balance() else True

    def deposit(self, amount, description=''):
        self.ledger.append(
            {
                "amount": amount, 
                "description": description
            }
        )
    
    def withdraw(self, amount, description=''):
        check = self.check_funds(amount)
        if check:
            self.ledger.append(
                {
                    "amount": -amount, 
                    "description": description
                }
            )
        return check
    
    def transfer(self, amount, category):
        check = self.check_funds(amount)
        if check:
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
        return check

    def get_spent(self):
        return sum([-x["amount"] for x in self.ledger if x["amount"]<0])

# print(create_spend_chart([food, clothing, auto]))
def create_spend_chart(categories):
    title = 'Percentage spent by category\n'

    lst_spent_by_category = [x.get_spent() for x in categories]
    lst_categories = [x.category for x in categories]
    
    total_spent = sum(lst_spent_by_category)
    lst_pct_spent_by_category = [
        int(x*10/total_spent)*10 
        for x in lst_spent_by_category
    ]
    x_axis = ' '*4 + '-'*(3*len(categories)+1) + '\n'

    y_axis_graph_area = ''

    y_ticks = [y for y in range(0,101,10)]

    for y_tick in y_ticks[::-1]:
        y_axis_graph_area = (
            y_axis_graph_area
            + str(y_tick).rjust(3)
            + '|'
        )
        for pct_spent_by_category in lst_pct_spent_by_category:
            y_axis_graph_area = (
                y_axis_graph_area
                + ' '
                + (
                    'o' 
                    if pct_spent_by_category >= y_tick
                    else ' '
                )
                + ' '
            )
        y_axis_graph_area = y_axis_graph_area + ' \n'
    
    x_ticks = ''
    for ii in range(len(max(lst_categories, key=len))):
        x_ticks = x_ticks + ' '*4
        for category in lst_categories:
            try:
                x_ticks = x_ticks + ' ' + category[ii] + ' ' 
            except:
                x_ticks = x_ticks + ' '*3
        x_ticks = x_ticks + ' ' + '\n'

    # remove linebreak from end
    x_ticks = x_ticks[:-1]

    out_str = title + y_axis_graph_area + x_axis + x_ticks

    return out_str