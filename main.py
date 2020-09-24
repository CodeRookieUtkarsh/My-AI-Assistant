from basic_functions import wiki_process
from basic_functions import wolf_process_1
from basic_functions import wolf_process_2
from basic_functions import month_string
from basic_functions import definition
from basic_functions import thesaurus

# from GUI import UDA as Gui  # to use as a GUI for UDA

from sys import exit as end  # to quit from the loop after query returned is none
from time import sleep  # to put the computer on sleep for a while
from selenium import webdriver as wd  # to open web browser and different pages on the web
from time import sleep  # to put the chatbot on sleep for n seconds

import speech_recognition as sr  # to recognise speech via the microphone of the system

import pyttsx3  # to speak via the default speaker of the system
import datetime  # to tell the current date and time using the speak() function
import smtplib  # to send emails using your mail
import os  # to open apps available in the computer
import pyperclip  # to copy text to the clipboard
import pyautogui  # to take screenshots of the computer screen and to click buttons remotely
import psutil  # to tell the cpu and battery percentage
import pyjokes  # to tell jokes
import pywhatkit  # to send whatsapp message
import requests  # to fetch information from the news, such as news and definitions of words
import json  # to display data from websites


def speak(text: str):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)

    voice = engine.getProperty('voices')
    engine.setProperty('voices', voice[0].id)

    engine.say(text)
    engine.runAndWait()


def time_fn():
    current_time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(f"The current time is {current_time}")


def date_fn():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)

    speak(f"Today's date is {date} {month_string[month]} {year}")


def welcome():
    hour = int(datetime.datetime.now().hour)

    if 6 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    elif 18 <= hour < 22:
        speak("Good evening sir!")
    else:
        speak("Welcome back sir!")

    speak("UDA at your service!")
    speak('''I am a digital assistant that can do many things. I can answer questions about me, my creator, my purpose, and can be a great listener if you confess something to me.
    I can tell you the date, time, your cpu and battery percentage, calculate some math problems, tell you about celebrities, and search something in wikipedia.
    I can also send emails, search something on google, restart, hibernate, or shutdown your computer and remember things you tell me to remember.
    I am also capable of opening applications in my creator, Utkarsh's computer.
    Finally, I can also copy some text to the clipboard, play some songs, and tell you some jokes.''')
    date_fn()
    time_fn()
    speak("How can I help you?")


def speech_recognition(dialog1: str = 'Listening...', dialog2: str = "Recognizing...", print_command: str = 'Human'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(dialog1)
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print(dialog2)
            query = r.recognize_google(audio, language="en-IN")
            print(f'{print_command}: {query.capitalize()}')
        except Exception as e:
            print(e)
            speak("I am sorry but could you please repeat that")

            return "None"
        return query


def email_sender(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('malaiya.utkarsh@gmail.com', 'I went to the beach and played')
    server.sendmail('malaiya.utkarsh@gmail.com', to, content)
    server.close()


def google_search(command):
    driver = wd.Chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in command:
        youtube_index = command.lower().split().index('youtube')
        query = command.split()[youtube_index + 1:]
        driver.get(
            'https://www.youtube.com/results?search_query=' + '+'.join(query))
    elif 'google' in command:
        speak("What should I search?")
        search = speech_recognition()

        query = search.split()
        driver.get("https://www.google.com/search?q =" + '+'.join(query))


def cpu_and_battery_data():
    usage = str(psutil.cpu_percent())
    print(f"\n\nYour CPU is at {usage}%")
    speak(f"Your CPU is at {usage} percent")

    battery_percent = psutil.sensors_battery()

    print(f"You have {battery_percent}% battery left")
    speak(f"You have {battery_percent} percent battery left")


def send_whatsapp_message(message):
    speak("Please now enter the details as they appear on your screen and please be very sincere in doing so")
    while True:
        to = int(input("Pls enter the receiver's mobile number[No need to enter the country code]: "))
        if len(str(to)) != 10:
            raise Exception('How is your receiver\'s phone number more than 10 digits!!')
        else:
            break

    while True:
        time_minute = int(input("At what minute do you want to send the message?: "))
        if time_minute not in range(60):
            raise IndexError('Minutes cannot be more than 59!! To denote 60, type 00 and the next hour!')
        else:
            break

    while True:
        time_hour = int(input('At what hour [in 24-hour format] do you want to send the message?: '))
        if time_hour not in range(25):
            raise KeyError("What the fork man! How is your hour more than 24!")
        else:
            break
        
    if time_hour == 24 and time_minute != 00:
        raise BaseException("What crazy world do you live in! How is your time more than 12 AM in the morning!")
    else:
        pass

    pywhatkit.sendwhatmsg(phone_no=to, message=message, time_hour=time_hour, time_min=time_minute, wait_time=2)


def tell_news():
    api_key = '03ffdd5a26394f30915006fd90f2eaa3'
    sources = {'bbc-news': 'BBC News', 'al-jazeera-english': 'AlJazeera News', 'reuters': 'Reuters News'}

    for source_key in sources.keys():
        speak(f"from {sources[source_key]}")
        print(f"=====================TOP HEADLINES FROM {sources[source_key].upper()}=====================")
        url = f'http://newsapi.org/v2/top-headlines?sources={source_key}&apiKey={api_key}'

        response = requests.get(url)

        articles = response.json()['articles']

        for news in articles:
            print(f"Title: {news['title']}")
            print(f"Description: {news['description']}")
            print(f"URL to read more: {news['url']}\n")
            speak(news['title'])
            sleep(2)

        speak('Take your time to read the news and I\'ll start with another source in 8 seconds')

        sleep(8)
        print('\n'*3)


def uda():
    command = 'define'

    while True:
        try:
            if command == 'none':
                break
            elif 'who are you' in command or 'what are you' in command:
                print("I am UDA, Utkarsh's Digital Assistant.\nI am under-development virtual assistant that is required to cater to all your needs.")
                speak("I am UDA, Utkarsh's Digital Assistant.\nI am under-development virtual assistant that is required to cater to all your needs.")
                break
            elif 'who created you' in command or 'who made you' in command or 'who coded you' in command:
                print("I have been created by a rookie programmer who goes by the name CodKie Utkarsh.")
                speak("I have been created by a rookie programmer who goes by the name CodKie Utkarsh.")
                break
            elif 'what can you do' in command:
                print('''I am a digital assistant that can do many things. I can answer questions about me, my creator, my purpose, and can be a great listener if you confess something to me.
                I can tell you the date, time, your cpu and battery percentage, calculate some math problems, tell you about celebrities, and search something in wikipedia.
                I can also send emails, search something on google, restart, hibernate, or shutdown your computer and remember things you tell me to remember
                Finally, I can also copy some text to the clipboard, play some songs, and tell you some jokes.''')
                speak('''I am a digital assistant that can do many things. I can answer questions about me, my creator, my purpose, and can be a great listener if you confess something to me.
                I can tell you the date, time, your cpu and battery percentage, calculate some math problems, tell you about celebrities, and search something in wikipedia.
                I can also send emails, search something on google, restart, hibernate, or shutdown your computer and remember things you tell me to remember
                Finally, I can also copy some text to the clipboard, play some songs, and tell you some jokes.''')
                break
            elif 'who is codkie utkarsh' in command or 'who is codkie' in command or 'who is utkarsh' in command:
                print("CodKie Utkarsh is a 15-year old young, Indian programmer who loves to code in python programming language")
                speak("CodKie Utkarsh is a 15-year old young, Indian programmer who loves to code in python programming language")
                break
            elif 'why are you in this world' in command or 'why are you here' in command:
                print("I don't know much about it but mainly because of CodKie Utkarsh")
                speak("I don't know much about it but mainly because of CodKie Utkarsh")
                break
            elif 'can you tell if I am a human or not' in command:
                print("Since you are speaking without a predefined set of instructions, I am gonna say you are a human")
                speak("Since you are speaking without a predefined set of instructions, I am gonna say you are a human")
                break
            elif 'I love you' in command:
                print("I am so sorry but I am not entitled to human emotions such as love.")
                speak("I am so sorry but I am not entitled to human emotions such as love.")
                break
            elif 'I have a confession' in command:
                print("Sure, go ahead!")
                speak("Sure, go ahead!")

                speech_recognition()

                print("I understand")
                speak("I understand")
                break
            elif 'time' in command:
                time_fn()
                break
            elif 'date' in command:
                date_fn()
                break
            elif 'calculate' in command:
                wolf_process_2(command)
                break
            elif 'open' in command:
                if 'Microsoft edge'.casefold() in command or 'edge' in command:
                    filepath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                    os.startfile(filepath)
                    break
                elif 'word' in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"
                    os.startfile(filepath)
                    break
                elif 'powerpoint' in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"
                    os.startfile(filepath)
                    break
                elif 'excel' in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"
                    os.startfile(filepath)
                    break
                elif 'One Note'.casefold() in command or 'Microsoft One Note'.casefold() in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OneNote.lnk"
                    os.startfile(filepath)
                    break
                elif 'outlook' in command or 'Microsoft Outlook'.casefold() in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook.lnk"
                    os.startfile(filepath)
                    break
                elif 'control panel' in command or 'control' in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Immersive Control Panel.lnk"
                    os.startfile(filepath)
                    break
                elif 'Visual Studio'.casefold() in command or 'Microsoft Visual Studio'.casefold() in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2019.lnk"
                    os.startfile(filepath)
                    break
                elif 'code' in command or 'VS Code'.casefold() in command or 'Visual Studio Code'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
                    os.startfile(filepath)
                    break
                elif 'cmd' in command or 'command prompt' in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\Command Prompt.lnk"
                    os.startfile(filepath)
                    break
                elif 'Windows Powershell'.casefold() in command or 'power shell' in command or "powershell".casefold() in command:
                    speak("I am sorry but I am not able to open Windows Powershell. So, I am opening an alternative, which is Windows Command Prompt")
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\Command Prompt.lnk"
                    os.startfile(filepath)
                    break
                elif 'chrome' in command or 'Google chrome'.casefold() in command:
                    filepath = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                    os.startfile(filepath)
                    break
                elif 'AVG' in command or 'anti virus' in command:
                    filepath = "C:\Program Files\AVG\Antivirus\AVGUI.exe"
                    os.startfile(filepath)
                    break
                elif 'dashlane'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Dashlane\Dashlane.exe"
                    os.startfile(filepath)
                    break
                elif 'bluestacks'.casefold() in command:
                    filepath = "C:\ProgramData\BlueStacks\Client\Bluestacks.exe"
                    os.startfile(filepath)
                    break
                elif 'pycharm'.casefold() in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2020.1.2.lnk"
                    os.startfile(filepath)
                    break
                elif 'virtualbox'.casefold() in command or 'Oracle VM Virtualbox'.casefold() in command or 'oracle virtualbox'.casefold() in command:
                    filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Oracle VM VirtualBox\Oracle VM VirtualBox.lnk"
                    os.startfile(filepath)
                    break
                elif 'nord VPN'.casefold() in command or 'nord'.casefold() in command or 'VPN'.casefold() in command:
                    filepath = "C:\Program Files\\NordVPN\\NordVPN.exe"
                    os.startfile(filepath)
                    break
                elif 'discord'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"
                    os.startfile(filepath)
                    break
                elif 'whatsapp'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\WhatsApp\WhatsApp.lnk"
                    os.startfile(filepath)
                    break
                elif 'GIT'.casefold() in command:
                    if 'Bash'.casefold() in command:
                        filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Git\Git Bash.lnk"
                        os.startfile(filepath)
                    elif 'CMD'.casefold() in command:
                        filepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Git\Git CMD (Deprecated).lnk"
                        os.startfile(filepath)
                    elif 'Hub'.casefold() in command:
                        filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\GitHub, Inc\GitHub Desktop.lnk"
                        os.startfile(filepath)
                    break
                elif 'spider'.casefold() in command or 'spider anaconda 3'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Spyder (anaconda3).lnk"
                    os.startfile(filepath)
                    break
                elif 'jupyter notebook'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Jupyter Notebook (anaconda3).lnk"
                    os.startfile(filepath)
                    break
                elif 'anaconda prompt'.casefold() in command:
                    filepath = "C:\\Users\\utkar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Anaconda Prompt (anaconda3).lnk"
                    os.startfile(filepath)
                    break
                else:
                    print("App not available in your computer. Check back with me later when you have installed it.")
                    speak("The application you have requested me to order is not installed in your computer. Please install the app and try again later.")
                    break
            elif 'what is' in command or 'who is' in command:
                wolf_process_1(command)
                break
            elif 'wiki' in command or 'wikipedia' in command or 'search in wikipedia'.casefold() in command:
                print("Searching...")
                if 'wikipedia' in command:
                    command = command.replace('wikipedia', '')
                elif 'wiki' in command:
                    command = command.replace('wiki', '')
                elif 'search on wikipedia' in command:
                    command = command.replace('search on wikipedia', '')
                wiki_process(command)
                break
            elif 'define' in command:
                word = str(input("Enter the word whose dictionary details you want to find out: "))

                definition(word)
                thesaurus(word)
                break
            elif 'send' and 'whatsapp message' in command:
                speak("Please speak the content of the message: ")
                content = speech_recognition('Go on...', 'Stop please...\nProcessing...', 'Content:')
                send_whatsapp_message(content)
            elif 'send email' in command or 'send an email' in command:
                try:
                    speak("Please type the email address of the one you have to send this email to")
                    to = input("Email receiver: ")
                    speak("Please tell me what would the email say")
                    content = speech_recognition()
                    email_sender(to, content)
                    speak("The mail was successful sent!")
                except Exception as e:
                    print(e)
                    speak("There was a problem in sending the email. The problem has been displayed on the screen")
                break
            elif 'search in chrome' in command or 'search in google' in command or 'search in web browser' in command:
                google_search(command)
                break
            elif 'search on youtube'.casefold() in command:
                google_search(command)
                break
            elif 'logout' in command:
                os.system('shutdown - l')
                break
            elif 'restart' in command:
                os.system('shutdown - /s /t 1')
                break
            elif 'shut down' in command:
                os.system('shutdown - /r /t 1')
                break
            elif 'hibernate' in command or 'sleep' in command:
                os.system('shutdown - /h')
                break
            elif 'play songs' in command:
                music_dir = 'C:/Users/utkar/Music'
                music = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, music[0]))
                break
            elif 'click picture' in command or 'take my selfie' in command or 'open camera' in command or 'take a photo' in command or 'take my photo' in command or 'click selfie' in command:
                os.startfile('"C:\\Users\\utkar\OneDrive\Desktop\Camera.lnk"')
                pyautogui.click(x='1861', y='537')
                break
            elif 'remember' and 'that' in command:
                speak("Please tell me what to remember")
                data = speech_recognition()
                speak(f'You told me to remember {data}')

                remember = open('Remember.txt', 'w')
                remember.write(data)
                remember.close()
                break
            elif 'what do you know' in command or 'what did I tell you to remember' in command or 'did I tell you to remember something' in command:
                remember = open('Remember.txt', 'r')
                speak(f"You told me to remember {remember.read()}")
                print(f"You told me to remember {remember.read()}")
                break
            elif 'take a screenshot' in command:
                speak("I'll wait for 5 seconds, do not close the terminal and on the foreground, put the screen whose screenshot you want to take")
                sleep(5)
                speak("Taking screenshot")
                img = pyautogui.screenshot()
                img.save("C:/Users/utkar/OneDrive/Pictures/UDA photos and screenshots")
                speak('Screenshot saved to the UDA screenshots folder in Pictures')
                break
            elif 'copy' and 'clipboard' in command:
                speak("What text would you like me to copy to the clipboard")
                text = speech_recognition()

                print(f'Text to be copied: {text}')
                pyperclip.copy(text)

                print("Text copied!")
                speak("Text copied!")
                break
            elif 'tell me news' in command:
                tell_news()
                break
            elif 'cpu and battery usage' in command or 'cpu usage' in command or 'battery usage' in command:
                cpu_and_battery_data()
                break
            elif 'joke' in command:
                joke = pyjokes.get_joke(category='general')
                print(joke)
                speak(joke)
                break
            elif 'offline' in command or 'there is nothing' in command:
                print("Thank you for using UDA\nRegards,\nCodkieUtkarsh")
                end()
            else:
                speak('Sorry, but I do not understand that!')
                print('Sorry, but I do not understand that!')
                uda()
        except:
            print("I am still under development so I am unable to process your request at the moment. Developments in me happen every week, so maybe check back with me next time.")
            speak("I am still under development so I am unable to process your request at the moment. Developments in me happen every week, so maybe check back with me next time.")
            break
    
    if command == 'none'.casefold():
        print("Could you say that again please")
        speak("Could you say that again please")
        uda()
    else:
        speak(f"Please tell me if I can do something else for you. Say go offline to turn me off")
        print("\n\nHow can I help you? Say 'go offline' to shut me down")
        uda()


if __name__ == '__main__':
    welcome()
    uda()
