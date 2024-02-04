import pytest
from app.calculations import add,subtract,multiply,divide, BankAccount, InsufficientFunds  #importing an add function from calculations.py
#first test

@pytest.fixture                # fixture is a function that is provided by pytest tool just to minimize the code
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()
  
@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5,),
                                           (7, 1, 8), (12, 4, 16)]) # here we are passing certain set values that we want to test or code through pytest
def test_add(num1, num2, expected):
    print("test add function")
    #sum = add(5,3)   #if sum=8 then pytest will consider it as passing other wise it asserts test failed
    assert add(num1, num2) == expected  # what an assert function will do when ever you set an true ok(or returning a true value) if you assert a false value then it will throw you an error

def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divde():
    assert divide(20, 5) == 4


def test_bank_set_initial_amount(bank_account):  # bankaccount this calls the bank account fixture
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):

    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):

    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):

    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)

])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)


