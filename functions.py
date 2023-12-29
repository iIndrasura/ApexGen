from playwright.sync_api import Playwright, sync_playwright
import random, time, imaplib, email, string, quopri, requests, json, sys
from bs4 import BeautifulSoup
import playwright.sync_api as sync_api
from discord_webhook import DiscordWebhook, DiscordEmbed
# from captcha import recaptchav2
from settings import get_webhooks_url, get_prefix       # from settings import *

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_passw(length):
    uppercase_letter = random.choice(string.ascii_uppercase)                                            # Ensure at least one uppercase letter
    remaining_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length - 1))     # Generate the remaining characters with lowercase letters and digits
    password = uppercase_letter + remaining_chars
    password_chars = list(password)                                                                     # Shuffle the characters to randomize the order
    random.shuffle(password_chars)
    return ''.join(password_chars)


#######################################################################
##                     OUTLOOK START                                 ##
#######################################################################

def createOutlook(chrome_args=None, context_options=None):
    with sync_api.sync_playwright() as playwright:
        
        # Generate a random email address and password
        prefix = get_prefix()
        email = f"{prefix}{generate_random_string(8)}@outlook.com"
        password = f"{generate_random_passw(9)}#$@"
        
        # proxy = requests.get('https://proxyelite.info/api/getproxy/')
        # decoded_proxy = proxy.content.decode('utf-8')
        # print(decoded_proxy)
        # browser = playwright.chromium.launch(headless=False,channel="chrome", args=chrome_args)        # args=['--disable-infobars', '--undetected-playwright']      #proxy={"server": f"http://{decoded_proxy}"}
        
        # If context_options is None, launch the browser without a proxy
        if context_options is not None:
            browser = playwright.chromium.launch(headless=False, channel="chrome", args=chrome_args, proxy=context_options["proxy"])
            context = browser.new_context(**context_options)    # Create a context with the configured options
        else:
            browser = playwright.chromium.launch(headless=False, channel="chrome", args=chrome_args)
            context = browser.new_context()                     # Create a context without proxy options
        
        #page = browser.new_page()
        page = context.new_page()   # Perform your tasks using the 'page' object
        page.set_default_timeout(timeout=120000)
        page.set_default_navigation_timeout(5000000)
        page.goto("https://signup.live.com/?lic=1")

        # Wait for the email form to load and fill in the email address
        page.wait_for_selector('#MemberName')
        page.fill('#MemberName', email)

        # Click "Next"
        page.click('#iSignupAction')

        # Wait for the password form to load and fill in the password
        page.wait_for_selector('#PasswordInput')
        page.fill('#PasswordInput', password)

        # Click "Next"
        page.click('#iSignupAction')

        # Wait for the name form to load
        page.wait_for_selector('#FirstName')

        # Generate a random first and last name
        first_name = generate_random_string(5)
        last_name = generate_random_string(4)

        # Fill in the name and click "Next"
        page.fill('#FirstName', first_name)
        page.fill('#LastName', last_name)
        page.click('#iSignupAction')

        # Wait for the DOB form to load
        page.wait_for_selector('#BirthMonth')

        # Generate a random DOB
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        year = str(random.randint(1988, 2005))

        # Select the month, day, and year from the dropdown menus
        page.select_option('#BirthMonth', month)
        page.select_option('#BirthDay', day)
        page.fill('#BirthYear', year)

        # Click "Next"
        page.click('#iSignupAction')

        time.sleep(2)
        # Wait for the CAPTCHA form to load
        page.wait_for_selector('#identityBanner')

        # Have a human solve the CAPTCHA and enter the solution manually
        print('Waiting for Captcha to be Solved!')
        
        # ////////////////////////////////////////////////////////////////////
        # CSS selector for the element with the text
        page.wait_for_selector(f'span.css-105:has-text("{"Your Microsoft account brings everything together"}")')
        print("Captcha Solved")

        # Click on the "Continue" button
        page.click('span.ms-Button-label.label-117')
        print("Continue")

        # Wait for the account creation success page to load
        try:
            page.locator('#idBtn_Back').click()
            print("Stay Logged in: No")
        except:
            pass

        try:
            page.locator('#iCancel').click()
            print("No Thanks to auth")
        except:
            pass

        try:
            page.locator('#home.banner.alta-column.cta')
            print("1")
            page.locator('a[aria-label="Your info"]')
            print("2")
            page.locator('a[aria-label="Privacy"]')
            print("3")
            page.locator('span#id__33')
            print("4")
        except:
            pass

        page.locator('#home.banner.alta-column.cta')
        # ////////////////////////////////////////////////////////////////////
        
        # # Wait for the account creation success page to load
        # try:
        #     page.locator('#idBtn_Back').click()
        #     print("Stay Logged in: No")
        # except:
        #     pass
        
        # page.locator('#home.banner.alta-column.cta')

        # Save the username and password to a file
        with open('credentials.txt', 'a') as f:
            f.write(f"\nEmail: {email}\nPass: {password}\n")
            f.close()
            print('Account Saved!')

        time.sleep(2)
        # input("Press Enter When Done (Wait for it to login Completely!)")
    discordSend('Email', email, password)
    return email, password

#######################################################################
##                         OUTLOOK END                               ##
#######################################################################
def start():
    author = '''

    88                      88                                                                  
    88                      88                                                                  
    88                      88                                                                  
    88 8b,dPPYba,   ,adPPYb,88 8b,dPPYba, ,adPPYYba, ,adPPYba, 88       88 8b,dPPYba, ,adPPYYba,
    88 88P'   `"8a a8"    `Y88 88P'   "Y8 ""     `Y8 I8[    "" 88       88 88P'   "Y8 ""     `Y8
    88 88       88 8b       88 88         ,adPPPPP88  `"Y8ba,  88       88 88         ,adPPPPP88
    88 88       88 "8a,   ,d88 88         88,    ,88 aa    ]8I "8a,   ,a88 88         88,    ,88
    88 88       88  `"8bbdP"Y8 88         `"8bbdP"Y8 `"YbbdP"'  `"YbbdP'Y8 88         `"8bbdP"Y8
                                                                                                                                                                                             
        DISCORD: indrasura                                                                              
                '''
    print(author)
#######################################################################
##                     MAIL READING START                            ##
#######################################################################
def read(username, passw):

    try:
        # Connect to the Outlook IMAP server
        server = imaplib.IMAP4_SSL('outlook.office365.com')
        server.login(username, passw)

        # Select the inbox folder
        server.select('INBOX')

        # Search for messages from a specific sender
        result, data = server.search(None, f'FROM "EA@e.ea.com"')

        # Loop through the search results and looks for Ban Email
        for msg_id in data[0].split():
            result, data = server.fetch(msg_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            # Check the message body for the desired string
            if 'Your EA Security Code is' in msg['Subject']:
                code = msg['Subject'][-6:]
                break

            else:
                code = None

        if code != None:
            print(code)
            return code

        elif code == None:
            return None

        # Log out of the server
        server.logout()

    except:
        print(f'Failed to login: {username}')

#######################################################################
##                       MAIL READING END                            ##
#######################################################################

#######################################################################
##                          STEAM START                              ##
#######################################################################


def process_payload(payload):
    body = quopri.decodestring(payload)
    try:
        body = body.decode()
    except UnicodeDecodeError:
        body = body.decode('cp1252')
 
    return body
    
def extract_emails_for_verification_link(username, email_password):
    # use your email provider's IMAP server: For hotmail, outlook and office 365, it's this:
    imap_server = "outlook.office365.com"
 
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(imap_server)
 
    # authenticate
    imap.login(username, email_password)
 
    # check if the connection was successful
    if imap.state == 'AUTH':
        verification_link = None
        # select messages folder
        imap.select('Inbox')
        # search for UNSEEN messages
        (resp_code, messages) = imap.search(None, '(UNSEEN)')
        # if there are emails
        if resp_code == 'OK':
            # get the emails
            emails = messages[0].split()
 
            # if there are emails
            if len(emails) > 0:
                # for each email
                for email_id in emails:
                    # fetch the email
                    (resp_code, data) = imap.fetch(email_id, '(RFC822)')
 
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            # convert the email to a string
                            msg = email.message_from_bytes(response_part[1])
 
                            # get the email subject
                            subject = msg['subject']
 
                            if str(subject).lower() == ("New Steam Account Email Verification".lower()):
                                # get the email body
                                email_body = msg.get_payload()
 
                                html_string = process_payload(email_body[1].as_bytes())
 
                                soup = BeautifulSoup(html_string, 'html.parser')
 
                                verification_link = soup.find('span', {'class': 'link c-grey4'}).parent.get('href')
                            else:
                                verification_link = None
            else:
                verification_link = None
        else:
            verification_link = None
    else:
        verification_link = None
 
    return verification_link

def createSteam(email, password, chrome_args=None, context_options=None):

    with sync_api.sync_playwright() as playwright:
 
        # browser = playwright.chromium.launch(headless=False,channel="chrome", args=chrome_args)              # args=['--disable-infobars', '--undetected-playwright']
        
        # If context_options is None, launch the browser without a proxy
        if context_options is not None:
            browser = playwright.chromium.launch(headless=False, channel="chrome", args=chrome_args, proxy=context_options["proxy"])
            context = browser.new_context(**context_options)    # Create a context with the configured options
        else:
            browser = playwright.chromium.launch(headless=False, channel="chrome", args=chrome_args)
            context = browser.new_context()                     # Create a context without proxy options
        
        # viewport={ 'width': 500, 'height': 400 },device_scale_factor=2,
        # page = browser.new_page()
        page = context.new_page()   # Perform your tasks using the 'page' object
            
        page.set_default_navigation_timeout(5000000)
        print('Started Steam Gen')
        page.goto("https://store.steampowered.com/join", wait_until="networkidle")
        time.sleep(0.1)
        print('Putting Email')
        page.locator("//input[@id='email']").type(email,delay = 1)
        time.sleep(0.1)
        page.locator("//input[@id='reenter_email']").type(email,delay = 1)     
        time.sleep(0.1)
        page.locator("//input[@id='i_agree_check']").click()

        time.sleep(0.1)
        # page.click("//button[@id='createAccountButton']//span[contains(text(),'Continue')]")

        try:
            with recaptchav2.SyncSolver(page) as solver:
                token = solver.solve_recaptcha()
                print('Captcha Solved!')

        except:
            input('Solve Captcha and Press Enter.')

        # wait for click
        time.sleep(0.1)
        page.locator('//*[@id="createAccountButton"]').click()
        
        # wait for the email to be sent
        time.sleep(5)
        # read the email and extract the verification link from it
        while True:
            verification_link = extract_emails_for_verification_link(email, password)
            if verification_link is not None:
                break
            else:
                time.sleep(5)
     
        # send response to the server to verify the account by extracted verification link
        verification_response = requests.get(verification_link)
     
        if verification_response.status_code == 200:
            custom_username1 = email.split("@")[0]
            # Next page after email verification
            page.locator('//*[@id="accountname"]').type(custom_username1,delay = 10)
            print('Setting Username')
            time.sleep(0.1)
            page.locator('//*[@id="password"]').type(password,delay = 10)
            print('Setting Password')
            time.sleep(0.1)
            page.locator('//*[@id="reenter_password"]').type(password,delay = 10)
            time.sleep(2)
            page.locator('//*[@id="createAccountButton"]').click()
            print('Creating...')
            time.sleep(6)
        data_list = [email, custom_username1, password]
        with open("SteamAccounts.txt", "a") as f:
            json.dump(data_list, f, indent=4)
            f.write("\n")
        f.close
    print('Successfully Created Steam')
    discordSend('Steam', email, password, custom_username1)
    return custom_username1

#######################################################################
##                          STEAM END                                ##
#######################################################################


#######################################################################
##                         EA GEN START                              ##
#######################################################################

def createEA(email, steam_username, steam_password, chrome_args=None, context_options=None):
    with sync_playwright() as p:
        # browser: Playwright = p.chromium.launch(headless=False, channel="chrome", args=chrome_args)         # args=['--disable-infobars', '--undetected-playwright']
        
        if context_options is not None:
            browser: Playwright = p.chromium.launch(headless=False, channel="chrome", args=chrome_args, proxy=context_options["proxy"])
            context = browser.new_context(**context_options)    # Create a context with the configured options
        else:
            browser: Playwright = p.chromium.launch(headless=False, channel="chrome", args=chrome_args)
            context = browser.new_context()                     # Create a context without proxy options
        
        page = context.new_page()
        page.set_default_navigation_timeout(5000000)
        # Go to the EA account creation page
        page.goto('https://www.ea.com/login')

        # Click the "Sign up with Steam" button
        page.click('.btn-steam-login')

        # Switch to the Steam login popup
        with page.expect_popup() as popup_info:
            print('Steam Link Opened')
            popup = popup_info.value
            # Fill in the Steam login form
            popup.fill("input.newlogindialog_TextInput_2eKVn[type='text']", steam_username)
            print('Sending Username')
            popup.fill("input.newlogindialog_TextInput_2eKVn[type='password']", steam_password)
            print('Sending Password')
            # passw_element = popup.locator("'newlogindialog_TextInput_2eKVn']").type(
            #     steam_password, delay=10)
            popup.click('button[class="newlogindialog_SubmitButton_2QgFE"]')

            popup.locator('#imageLogin[type="submit"]').click()
            popup.locator('#authForm > button:nth-child(9)[type="submit"]').click()

        # Wait for the Steam login to complete and redirect back to EA
        print('Steam Link Closed')
        # Generate a random DOB
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        year = str(random.randint(1990, 2005))

        try:
            #emailVerifyCode ##btnSendCode #continueDoneBtn
            page.select_option('#clientreg_dobmonth-selctrl', month)
            page.select_option('#clientreg_dobday-selctrl', day)
            page.select_option('#clientreg_dobyear-selctrl', year)
            print('Selecting DOB')
            page.click('#countryDobNextBtn')
            page.locator('#email[type="text"]').type(email,delay = 10)
            print('Putting Email Address')
            time.sleep(1)
            page.click('#basicInfoNextBtn')
            page.locator('#read-accept-container > span').click()
            print('Accepting Terms')
            page.click('#submitBtn')

        except:
            pass

        code = None
        while code == None:
            print('Trying to Fetch EA Code...')
            time.sleep(2)
            code = read(email, steam_password)

        page.fill("#emailVerifyCode", code)
        page.click("#btnSendCode")
        page.locator('#continueDoneBtn').click()

        print('Account created and logged in successfully!')
        data_list = [email, steam_username, steam_password]
        with open("EAccounts.txt", "a") as f:
            json.dump(data_list, f, indent=4)
            f.write("\n")
        f.close
        browser.close()
        discordSend('EA', email, steam_password, steam_username)
#######################################################################
##                          EA GEN END                               ##
#######################################################################

def discordSend(title, email, password, accname=None):
    webhooks_url = get_webhooks_url()
    webhook = DiscordWebhook(url=webhooks_url, username="ApexGen")
    
    if 'EA' in title and accname != None:
        embed = DiscordEmbed(title=f'{title} Linked to Steam Account', color='fc1303')
        embed.add_embed_field(name=f'Email', value=f'{email}')
        embed.add_embed_field(name=f'Steam', value=f'{accname}')
        embed.add_embed_field(name=f'Password', value=f'{password}')
        embed.set_footer(text='Discord: indrasura')
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()

    elif 'Email' in title and accname == None:
        embed = DiscordEmbed(title=f'{title} Account Generated', color='42f581')
        embed.add_embed_field(name=f'Email', value=f'{email}')
        embed.add_embed_field(name=f'Password', value=f'{password}')
        embed.set_footer(text='Discord: indrasura')
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()

    elif 'Steam' in title and accname != None:
        embed = DiscordEmbed(title=f'{title} Account Generated', color='038cfc')
        embed.add_embed_field(name=f'Email', value=f'{email}')
        embed.add_embed_field(name=f'Steam', value=f'{accname}')
        embed.add_embed_field(name=f'Password', value=f'{password}')
        embed.set_footer(text='Discord: indrasura')
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()

# 130200ms restart router