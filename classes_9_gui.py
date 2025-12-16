
class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.expenses = []
        self.categories = []

    def add_expenses(self, expense_data):
        """
        Adds a list of (category, cost) tuples.
        This simple method is PERFECT for a GUI.
        """
        for cat, cost in expense_data:
            self.categories.append(cat)
            self.expenses.append(float(cost))

    def get_expenses(self):
        # This just returns the number, no printing!
        return sum(self.expenses)

    def get_expenses_list(self):
        # This just returns the list, no printing!
        return list(zip(self.categories, self.expenses))
    





    def save_to_file(self, filename):
        with open(filename, "a") as f:
            for cat, cost in zip(self.categories, self.expenses):
             f.write(f"{self.expense_type},{cat},{cost}\n")

def load_from_file(self, filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                exp_type, cat, cost = line.strip().split(",")
                if exp_type == self.expense_type:
                    self.categories.append(cat)
                    self.expenses.append(float(cost))
    except FileNotFoundError:
        pass
