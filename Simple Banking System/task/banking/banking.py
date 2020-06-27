import random
import sqlite3


def create_account():
    digits = [int(i) for i in str(random.randint(4000000000000000, 4000009999999999))]
    number = ''.join([str(i) for i in digits])
    digits = [digits[i] if i % 2 else digits[i] * 2 for i in range(15)]
    s = sum([digit if digit < 10 else digit - 9 for digit in digits])
    number = number[:-1] + str(10 - s % 10) if s % 10 else number[:-1] + '0'
    pin = random.randint(1000, 9999)
    print(f'Your card has been created\nYour card number:\n{number}\nYour card PIN:\n{pin}')

    cursor.execute('''INSERT INTO card (number, pin) VALUES (?, ?)''', (number, pin))
    conn.commit()


def luhn_generator(number):
    number = [int(i) for i in number]
    digits = [number[i] if i % 2 else number[i] * 2 for i in range(15)]
    s = sum([digit if digit < 10 else digit - 9 for digit in digits]) + number[15]
    return s % 10 == 0


def menu():
    choice = int(input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n'))
    while choice != 0:
        if choice == 1:
            balance()
        elif choice == 2:
            add_income()
        elif choice == 3:
            transfer()
        elif choice == 4:
            close_account()
        elif choice == 5:
            return
        choice = int(input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n'))
    return 0


def balance():
    cursor.execute('''SELECT balance FROM card WHERE number = ?''', (card_number,))
    print(f'Balance: {cursor.fetchone()[0]}')


def add_income():
    income = int(input('Enter income:\n'))
    cursor.execute('''UPDATE card SET balance = balance + ? WHERE number = ?''', (income, card_number))
    conn.commit()
    print('Income was added!\n')


def transfer():
    transfer_card = input('Transfer\nEnter card number:\n')
    if card_number != transfer_card:
        if luhn_generator(transfer_card):
            cursor.execute('''SELECT id FROM card WHERE number=?''', (transfer_card,))
            if len(cursor.fetchall()) != 0:
                income = int(input('Enter how much money you want to transfer:\n'))
                cursor.execute('''SELECT balance FROM card WHERE number=?''', (card_number,))
                if cursor.fetchone()[0] >= income:
                    cursor.execute('''UPDATE card SET balance = balance + ? WHERE number = ?''', (income, transfer_card))
                    cursor.execute('''UPDATE card SET balance = balance - ? WHERE number = ?''', (income, card_number))
                    conn.commit()
                    print('Success!')
                else:
                    print('Not enough money!')
            else:
                print('Such a card does not exist.')
        else:
            print('Probably you made mistake in the card number. Please try again!')
    else:
        print("You can't transfer money to the same account!")


def close_account():
    cursor.execute('''DELETE FROM card WHERE number = ?''', (card_number,))
    conn.commit()
    print('The account has been closed!')


conn = sqlite3.connect("card.s3db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS card
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
conn.commit()

action = int(input('1. Create an account\n2. Log into account\n0. Exit\n'))
while action != 0:
    if action == 1:
        create_account()
    elif action == 2:
        card_number = input('Enter your card number:\n')
        card_PIN = input('Enter your PIN:\n')
        cursor.execute('''SELECT id FROM card WHERE number=?''', (card_number,))
        if len(cursor.fetchall()) != 0:
            cursor.execute('''SELECT pin FROM card WHERE number=?''', (card_number,))
            if cursor.fetchone()[0] == card_PIN:
                print('You have successfully logged in!\n')
                action = menu()
            else:
                print('Wrong card number or PIN!\n')
        else:
            print('Wrong card number or PIN!\n')
    if action:
        action = int(input('1. Create an account\n2. Log into account\n0. Exit\n'))
print('Bye!')
