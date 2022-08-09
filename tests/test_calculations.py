import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, Insufficient

@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(1000)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (5, 3, 8),
    (-8, -3, -11)
    ])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 1),
    (5, 3, 2),
    (-8, -3, -5)
    ])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 6),
    (5, 3, 15),
    (-8, -3, 24)
    ])
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 1.5),
    (15, 3, 5),
    (-9, -3, 3)
    ])
def test_divide(num1, num2, expected):
    assert divide(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    print("Testing my bank initial amount")
    assert bank_account.balance == 1000

def test_bank_default_amount(zero_bank_account):
    print("Testing my bank default amount")
    assert zero_bank_account.balance == 0

def test_amount_after_deposit(bank_account):
    bank_account.deposite(100)
    assert bank_account.balance == 1100

def test_amount_after_withdraw(bank_account):
    bank_account.withdraw(100)
    assert bank_account.balance == 900

def test_collected_intrest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 1050


@pytest.mark.parametrize("deposite, withdraw, expected", [
    (3000, 2000, 1000),
    (1500, 300, 1200),
    (900, 650, 250)
    ])
def test_bank_transaction(zero_bank_account, deposite, withdraw, expected):
    zero_bank_account.deposite(deposite)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_balance(bank_account):
    with pytest.raises(Insufficient):
        bank_account.withdraw(1500)