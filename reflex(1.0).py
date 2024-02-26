from __future__ import print_function
import datetime
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pyttsx3                      #text to speech library.
import datetime                     #date and time library.
import speech_recognition as sr     #speech recognition library.
import webbrowser as wb             #Web Browser library.
import wikipedia as wk              #Wikipedia library.
import smtplib as sl                #smtp protocal is to send emails.
# from email.message import EmailMessage
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

from wikipedia import exceptions
receiver={"juglal":"boddu.jugalbhaskarnagaganesh.20cse@bmu.edu.in", 
"bhanu":"naga.bhanukoushikreddyavuthu.20cse@bmu.edu.in ",
"yashika":"yashika.mittal.20cse@bmu.edu.in","payas":"payas.gakhar.20cse@bmu.edu.in" }

engine = pyttsx3.init('sapi5') # Microsoft speech API(sapi5).
voices = engine.getProperty('voices')  # this is used to get the voices in machine.
engine.setProperty('voice',voices[1].id) # setting a voice to our relfex

def wishMe():                   #wish Me
    hour=int(datetime.datetime.now().hour) #taking present hour in 24 hour clock.
    if hour>=0 and hour<12:                #conditional statements for wishing me.
        speech("Good Morning sir!")
    elif hour>=12 and hour <17:
        speech("Good Afternoon sir!")
    else :
        speech("Good Evening sir!")
    speech("I am reflex, Tell me what to do?")  #telling about itself.

def speech(audio):              #speech function (will speak out the input)
    engine.say(audio)
    engine.runAndWait()

def takeCommand(a):             #speech recognition and takes an input as 'a'
    r=sr.Recognizer()           # r is recognizer class of speech recognition library
    with sr.Microphone() as source: # using microphone  as input
        if a==1:
            print("listening..")
        r.adjust_for_ambient_noise(source,duration=1)  #remove the noise in source
        r.pause_threshold=1
        audio = r.listen(source)    #input is stored in audio
    try:                        #here we will recognize the audio by google recognizer
        if a==1:
            print("Recognizing..")
            query = r.recognize_google(audio,language="en-in") #recognition when it is "cm" 
            print(f"recognized: {query}")
        elif a==0:
            query = r.recognize_google(audio,language="en-in") #recognition when it is "first"
            print(f"recognized: {query}")

    except Exception:        # if speech recognizer doesnot work
        #print(Exception)    #uncomment if you want to know the exception
        if a==1:             # speaks "say that again" if it is "cm" 
            speech("Say that again")
        return "none"        #returns none
    return query            #returns the query if all went well!!...

def sendEmail(to,content):
    server= sl.SMTP("smtp.google.com",587)
    server.ehlo()
    server.starttls()
    login_mail = "reflexthecommonfrnd@gmail.com"  #email ID
    login_password = "121231234" #login password
    server.login(login_mail,login_password)
    server.sendmail(login_mail,to,content)
    server.close()
def aut_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(service):
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])




if __name__== "__main__":       #main function
    wishMe()                #reflex wishes me. 
    service=aut_google()

    while (1):              #enters the while loop for listening all the time.
        a=0                 #'a' is introduced because if speaker says "reflex",then only it start reacting to the logics queries.
        first=takeCommand(a).lower()   #takes the query returned by takeCommand function and converts into small alphabets.
        if "exit reflex" in first:   #here if we say "exit reflex" the code terminates
            exit() 
        if "reflex" in first:       #if reflex is in first, it reacts to the conditional commands
            a=1             #here 'a'
            cm=takeCommand(a).lower()
            if "wikipedia" in cm:       #wikipedia
                speech("searching in wikipedia") #speaks out "searching in wikipedia".
                cm=cm.replace("wikipedia",'') #Prabhas wikipedia ==> Prabhas 
                speech("Acording to Wikipedia..") #speaks out "Acording to Wikipedia.."
                speech(wk.summary(cm, sentences=2)) #speaks out the sentences 
                print(wk.summary(cm,sentences=2))
            elif cm == "open youtube" : #youtube
                wb.open("youtube.com")  #it will open youtube in Web Browser
            elif cm == "open google":
                wb.open("google.com")
            elif "the time" in cm:
                timeStr=datetime.datetime.now().strftime("%H:%M:%S")
                speech(f"the time is {timeStr}")
            # elif "send a mail" in cm:
            #     try:
            #         speech("To whom do you want to send the mail?")
            #         to=takeCommand(a).lower()
            #         speech("What should I write?")
            #         content=takeCommand(a)
            #         sendEmail(receiver[to],content)
            #         speech("email is sent!")
            #     except Exception as e:
            #         print(e)
            #         speech("email not sent!!")
            elif cm=="set an remainder":
                pass
            elif 'play music' in cm:
                music_dir="C:\\Users\\91868\\OneDrive\\Desktop\\Everything\\music"
                song=os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,song[0]))