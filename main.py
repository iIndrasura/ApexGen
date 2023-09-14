from functions import *

start()
amount = 1
while True:
    try:
        amount = int(input("How many accounts would you like to create?\n>"))
        
        mode = int(input('''\nSelect Gen Mode:
1. Outlook + Steam
2. Outlook + Steam + EA
3. Steam + EA Only
4. EA Only (Needs Steam User, Email and Password)

>'''))
        if amount > 0: break
        print("Please enter a valid amount.")
    except ValueError:
        print("Please enter a valid amount.")
        pass

for _ in range(amount):

    if mode == 1:
        email_address, password = createOutlook()
        steam_username = createSteam(email_address, password)

    elif mode == 2:
        email_address, password = createOutlook()
        steam_username = createSteam(email_address, password)
        createEA(email_address, steam_username, password)

    elif mode == 3:
        email_address = input('Enter Email (Outlook Only): ')
        password = input('Enter Password: ')
        steam_username = createSteam(email_address, password)
        createEA(email_address, steam_username, password)

    elif mode == 4:
        print('Password for Steam must be same as email password.')
        email_address = input('Enter Email: ')
        steam_username = input('Enter Steam Username: ')
        password = input('Enter Password: ')
        createEA(email_address, steam_username, password)

    else:
        print('Invalid Option')
