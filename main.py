# pyinstaller --onefile --add-data "settings.json;." --icon=generator.ico main.py

from functions import *
import os

def create_proxy_file():
    proxy_file_path = 'proxy.txt'
    if not os.path.isfile(proxy_file_path):
        print("proxy.txt not found. Creating a new one.")
        print("Please edit SOCKS5 proxy list in .txt file in this Format: ip:port:username:password\n")
        
        open(proxy_file_path, 'a').close()
        # with open('proxy.txt', 'w') as f:
        #     f.write('# Format: ip:port:username:password\n')

# Check and create proxy.txt if needed
create_proxy_file()

try:
    # Load SOCKS5 proxies from proxy.txt file
    with open('proxy.txt', 'r') as f:
        proxy_lines = f.read().splitlines()

    start()
    amount = 1
    while True:
        try:
            amount = int(input("How many accounts would you like to create?\n>"))
            
            print("NOTE: If you want to create account without outlook then you will have to provide account ID and Password")
            print("      If using proxy please edit SOCKS5 proxy list in .txt file in this Format: ip:port:username:password")
            mode = int(input('''\nSelect Gen Mode:
    1. Outlook Only
    2. Outlook + Steam
    3. Outlook + Steam + EA
    4. Steam + EA Only
    5. EA Only (Needs Steam User, Email and Password)

    >'''))
            if amount > 0: break
            print("Please enter a valid amount.")
        except ValueError:
            print("Please enter a valid amount.")
            pass

    # Create accounts using proxies
    proxy_index = 0  # Initialize the proxy index

    def split_proxy_info(proxy_info):
        ip, port, username, password = proxy_info.split(':')
        return ip, port, username, password

    for _ in range(amount):
        # Check if there are proxies available
        if not proxy_lines:
            print("No proxies found. Running without a proxy.\n")
            context_options = None
        else:
            # Ensure proxy_index stays within bounds
            if proxy_index >= len(proxy_lines):
                print("Ran out of proxies. Exiting.\n")
                break

        # Split the proxy info from the current line
            proxy_info = proxy_lines[proxy_index]
            ip, port, username, password = split_proxy_info(proxy_info)

            # Configure Chrome to use the SOCKS5 proxy
            proxy_url = f'{username}:{password}@{ip}:{port}'
            # proxy_url = f'socks5://{username}:{password}@{ip}:{port}'
            context_options = {
                'proxy': {
                    'server': proxy_url,
                    'username': username,
                    'password': password
                }
            }

        chrome_args = [
            '--disable-infobars',
            # '--headless',
            # '--disable-gpu',
            # '--disable-dev-shm-usage',
            # '--no-sandbox',
            '--undetected-playwright'
        ]

        if mode == 1:
            email_address, password = createOutlook(chrome_args, context_options)
            
        elif mode == 2:
            email_address, password = createOutlook(chrome_args, context_options)
            steam_username = createSteam(email_address, password, chrome_args, context_options)

        elif mode == 3:
            email_address, password = createOutlook(chrome_args, context_options)
            steam_username = createSteam(email_address, password, chrome_args, context_options)
            createEA(email_address, steam_username, password, chrome_args, context_options)

        elif mode == 4:
            email_address = input('Enter Email (Outlook Only): ')
            password = input('Enter Password: ')
            steam_username = createSteam(email_address, password, chrome_args, context_options)
            createEA(email_address, steam_username, password, chrome_args, context_options)

        elif mode == 5:
            print('Password for Steam must be same as email password.')
            email_address = input('Enter Email: ')
            steam_username = input('Enter Steam Username: ')
            password = input('Enter Password: ')
            createEA(email_address, steam_username, password, chrome_args, context_options)

        else:
            print('Invalid Option')
        
        # Increment the proxy index or cycle back to the beginning if all proxies were used
        proxy_index = (proxy_index + 1) % len(proxy_lines)
        
except Exception as e:
    print(f"An error occurred: {e}")
    
input("Press Enter to exit...")
