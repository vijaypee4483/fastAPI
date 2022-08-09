def add(num1: int, num2: 2):
    return num1 + num2

def subtract(num1: int, num2: 2):
    return num1 - num2

def multiply(num1: int, num2: 2):
    return num1 * num2

def divide(num1: int, num2: 2):
    return num1 / num2

class Insufficient(Exception):
    pass


class BankAccount:
    def __init__(self, balence = 0):
        self.balance = balence

    def deposite(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise Insufficient("Insufficient balance in the account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.05
