import telebot
from telebot import types
import os
import time 
from datetime import date, timedelta, datetime
from googletrans import Translator
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
translator = Translator()
bot = telebot.TeleBot("secret1")
scope = []
spreadsheet_id = 'secret2'
languages = ["en", "ru", "es", "zh"]
language_dict = {"🇺🇲":"en", "🇷🇺":"ru"}

response = requests.get('https://www.googleapis.com/auth/spreadsheets', timeout=10) 
scope.append(response.url)

def main():
    a_list = []
    link =[]
    date_list = []
    credentials =None
    if os.path.exists('token.json'):
        credentials=Credentials.from_authorized_user_file('token.json', scope)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh.token:
            credentials.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file("GOOGLE.json", scope)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    try:
        print("starting bot ...")
        #bot logic goes here
        
        
        service =build("sheets", "v4", credentials=credentials)
        sheets =service.spreadsheets()
        
        
        @bot.message_handler(commands=['start'])
        def start(message):
            today = date.today()
            three_days_ago = today - timedelta(days = 3)
            user_id = message.from_user.id
            username = message.from_user.username
            link.append(f"https://t.me/{username}")
            date_list.append(today.strftime("%Y-%m-%d"))
            date_list.append(three_days_ago.strftime("%Y-%m-%d"))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            russian = types.KeyboardButton("🇷🇺")
            enlish = types.KeyboardButton("🇺🇲")
            markup.row(russian, enlish)
            bot.send_message(message.chat.id, 'Please select your language', reply_markup=markup)
            a_list.clear()
            print(date_list)
            return link





        @bot.message_handler(func=lambda message: message.text == "🇷🇺")
        def lang(message):
            a_list.append(language_dict["🇷🇺"])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'I am a shopper 🛍️', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'I am a flight attendant 👩‍✈️', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Please choose what best describes you', src ="en", dest = a_list[0]).text, reply_markup=markup)
            return a_list
    
        @bot.message_handler(func=lambda message: message.text == "🇺🇲")
        def lang(message):
            a_list.append(language_dict["🇺🇲"])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'I am a shopper 🛍️', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'I am a flight attendant 👩‍✈️', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Please choose what best describes you', src ="en", dest = a_list[0]).text, reply_markup=markup)
            return a_list
        
        
        
        
        
        
        
        
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = 'I am a shopper 🛍️', src ="en", dest = a_list[0]).text)
        def shopper(message):
            a_list.append('I am a shopper 🛍️')
            #a_list.append(message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'ready 👍', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'not ready 👎', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Hello Shopper !!! We will start by asking you a few questions, ready ?', src ="en", dest = a_list[0]).text, reply_markup=markup)
            return a_list
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = 'I am a flight attendant 👩‍✈️', src ="en", dest = a_list[0]).text)
        def flightattendant(message):
            a_list.append('I am a flight attendant 👩‍✈️')
            #a_list.append(message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'ready 👍', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'not ready 👎', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Hello flight attendant !!! We will start by asking you a few questions, ready ? ', src ="en", dest = a_list[0]).text, reply_markup=markup)
            print(a_list)
            return a_list
        
        
        
        
        
        
        
        
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = 'ready 👍', src ="en", dest = a_list[0]).text and a_list[1]=='I am a shopper 🛍️')
        def ready(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            submit = types.KeyboardButton(translator.translate(text = 'submit', src ="en", dest = a_list[0]).text)
            markup.row(submit)
            for row in range(2,20):
                if sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!B{row}").execute().get('values')!=None:
                    row = row+1
                else:
                                        
                    
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!B{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{a_list[1]}']]}).execute()
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!C{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{link[0]}']]}).execute()
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!E{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{date_list[0]}']]}).execute()
                    #time.sleep(5)
                
                    print("recorded ✅")
                    break
            #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #yes_button = types.KeyboardButton('YES ✅')
            #no_button = types.KeyboardButton('NO ❌')
            #markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Please provide the following information about you: \n\n 1. Your Name 👋\n\n 2. Your Location (Country and City) 📍\n\n 3. Total Value of the Item 💲\n\n 4. Link to the item 🔗\n\n 5. Delivery quota 💰', src ="en", dest = a_list[0]).text, reply_markup=markup)
       
            return a_list
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = 'ready 👍', src ="en", dest = a_list[0]).text and a_list[1]== 'I am a flight attendant 👩‍✈️')
        def ready(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            submit = types.KeyboardButton(translator.translate(text = 'submit', src ="en", dest = a_list[0]).text)
            markup.row(submit)
            for row in range(2,20):
                if sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!B{row}").execute().get('values')!=None:
                    row = row+1
                else:
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!B{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{a_list[1]}']]}).execute()
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!C{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{link[0]}']]}).execute()
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!E{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{date_list[0]}']]}).execute()
                    #time.sleep(5)
                    
                    print("recorded ✅")
                    break
            #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #yes_button = types.KeyboardButton('YES ✅')
            #no_button = types.KeyboardButton('NO ❌')
            #markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = 'Please provide the following information about you: \n\n 1. Your Name 👋\n\n 2. Where are You Flying from and To \n\n (example:🇪🇸 > 🇷🇺 ) \n\n 3. Preferred quota for your service. 💰', src ="en", dest = a_list[0]).text, reply_markup=markup)
       
            return a_list
        
        
        
        
        
        
        
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = "not ready 👎", src ="en", dest = a_list[0]).text)
        def notready(message):
            a_list.clear()
            print("list has been cleared", a_list)
            bot.send_message(message.chat.id, translator.translate(text = "Nevermind, let's start again", src ="en", dest = a_list[0]).text)
    
             
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = "YES ✅", src ="en", dest = a_list[0]).text)
        def yes(message):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'Find Deals 😎', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'Come Back ⬅️', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            bot.send_message(message.chat.id, translator.translate(text = "your entry has been recorded ✅", src ="en", dest = a_list[0]).text, reply_markup=markup)
            
            print(a_list)
            for row in range(2,20):
                if sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{row}").execute().get('values')!=None:
                    row = row+1
                else:
                    sheets.values().update(spreadsheetId=spreadsheet_id, range = f"Sheet1!A{row}", valueInputOption="USER_ENTERED", body={"values":[[f'{a_list[2]} \n\n Start chat: {link[0]}']]}).execute()
                    #photo=bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
                    #sheets.insert_row([message.chat.id, message.date, photo], 2)
                    print("recorded ✅")
                    break
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = "Come Back ⬅️", src ="en", dest = a_list[0]).text)
        def comeback(message):
            start(message)
        
        '''
        @bot.message_handler(func=lambda message: message.text == translator.translate(text="Find Deals 😎", src="en", dest=a_list[0]).text)
        def FindDeals(message):
            # Retrieve the spreadsheet values once
            sheet_values = sheets.values().get(spreadsheetId=spreadsheet_id, range="Sheet1").execute().get('values')
            

            for row in range(2, 20):
                if sheet_values[row - 1]:
                    cell_B_value = sheet_values[row - 1][1][0]
                    global cell_E_value
                    cell_E_value = sheet_values[row - 1][4][0]
                    #print(datetime.strptime(cell_E_value, "%Y-%m-%d").date())
                    
                    #if cell_B_value != a_list[1] and date_list[0] > datetime.strptime(cell_E_value, "%Y-%m-%d").date() > date_list[1]:
                        #bot.send_message(message.chat.id, str(sheet_values[row - 1][0][0]))
                
        '''
        
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = "Find Deals 😎", src ="en", dest = a_list[0]).text)
        def FindDeals(message):
            for row in range(2,20):

                if sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{row}").execute().get('values')!=None and sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!B{row}").execute().get('values')[0][0]!=a_list[1]:
                    
                    bot.send_message(message.chat.id, str(sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{row}").execute().get('values')[0][0]))
     
        @bot.message_handler(func=lambda message: message.text == translator.translate(text = "NO ❌", src ="en", dest = a_list[0]).text)
        def no(message):
            a_list.clear()
            print("list has been cleared", a_list)
            bot.send_message(message.chat.id, translator.translate(text = "Nevermind, let's start again. Click /start command to relaunch the bot.", src ="en", dest = a_list[0]).text)
    
    
    
    
    
        @bot.message_handler(func=lambda message: message.text !=None)
        def record_messages(message):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes_button = types.KeyboardButton(translator.translate(text = 'YES ✅', src ="en", dest = a_list[0]).text)
            no_button = types.KeyboardButton(translator.translate(text = 'NO ❌', src ="en", dest = a_list[0]).text)
            markup.row(yes_button, no_button)
            if len(a_list)<1:
                bot.send_message(message.chat.id, translator.translate(text = "please start the bot with the start command", src ="en", dest = a_list[0]).text)
                
            else:
                a_list.append(message.text)
                print("waiting for confirmation...")
                bot.send_message(message.chat.id, translator.translate(text = f"Does this info look correct to you: \n\n {a_list[2]} ?", src ="en", dest = a_list[0]).text, reply_markup=markup)
                

        bot.polling()
    except HttpError as error:
        print(error)
    #except HttpError as error:
        #print(error)

    
        #USE LIST OR DICTIONARY TO SAVE THE ROW
if __name__ == '__main__':
    main()    
        
    '''
    @bot.message_handler(func=lambda message: message.text =="last message")
    def record_messages(message):
            print("getting last message...")
            data_row = record_messages(message)
            response = sheets.values().get(spreadsheetId=spreadsheet_id, range=f"Sheet1!A{data_row}").execute().get('values')
            print(response)
            return response

'''
'''
# Replace the placeholders with your own values
bot_token = '6675782241:AAGmcs9g2euKj89gmJJXl26LHspCWgV8xyQ'
google_sheet_name = 'telebot'
google_sheet_tab_name = 'Sheet1'
google_sheet_credentials_file = 'GOOGLE.json'

# Authenticate with Google Sheets API


creds = ServiceAccountCredentials.from_json_keyfile_name(google_sheet_credentials_file, scope)
client = gspread.authorize(creds)

# Open the Google Sheet and select the tab
sheet = client.open(google_sheet_name).worksheet(google_sheet_tab_name)

# Initialize the Telegram bot
bot = telebot.TeleBot(bot_token)

# Define a function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Get the message text and chat ID
    message_text = message.text
    chat_id = message.chat.id
    
    # Append the message to the Google Sheet
    sheet.append_row([message_text, chat_id])
    
    # Send a confirmation message back to the user
    bot.send_message(chat_id, 'Your message has been recorded!')
def handle_photo(message):
    # Download the photo
    photo = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)

    # Upload the photo to Google Sheets
    sheet.insert_row([message.chat.id, message.date, photo], 2)

    # Send a confirmation message
    bot.reply_to(message, 'Photo saved to Google Sheets!')

# Start the bot
bot.polling()

# Start the bot
bot.polling()
'''